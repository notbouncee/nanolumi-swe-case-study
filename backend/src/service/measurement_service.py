import httpx
import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import cast
from fastapi import HTTPException
from src.repository import measurement_repository, device_repository
from src.repository.models import MeasurementStatus
import os

logger = logging.getLogger(__name__)

SIMULATOR_URL = os.getenv("SIMULATOR_URL", "http://simulator:9000")

async def get_device_measurements(device_id: str) -> list[dict]:
    measurements = await measurement_repository.get_measurements_by_device(device_id)
    return [
        {
            "id": m.id,
            "request_id": m.request_id,
            "status": m.status.value,
            "requested_at": m.requested_at,
            "completed_at": m.completed_at,
            "ph": m.ph,
            "temperature_c": m.temperature_c
        }
        for m in measurements
    ]


async def request_measurement(device_id: str, parameters: list[str]) -> dict:
    device = await device_repository.get_device_by_device_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    latest_measurement = await measurement_repository.get_latest_measurement(device_id)
    if latest_measurement:
        if latest_measurement.status in ["pending", "acknowledged"]:
            # Need to ensure requested_at is timezone aware for comparison
            # Tortoise might return naive depending on DB driver. So let's handle that.
            req_time = latest_measurement.requested_at
            if req_time.tzinfo is None:
                req_time = req_time.replace(tzinfo=timezone.utc)

            time_since_request = datetime.now(timezone.utc) - req_time
            if time_since_request < timedelta(seconds=5):
                raise HTTPException(
                    status_code=429,
                    detail="A measurement request is already pending for this device. Please wait.",
                )

    request_id = str(uuid.uuid4())
    now_utc = datetime.now(timezone.utc)

    measurement = await measurement_repository.create_measurement(
        request_id=request_id, device_id=device_id, requested_at=now_utc
    )

    payload = {
        "request_id": request_id,
        "requested_at": now_utc.isoformat(),
        "callback_url": "http://backend:8000/api/webhooks/simulator",
        "parameters": parameters
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SIMULATOR_URL}/api/devices/{device_id}/measurements", json=payload
            )
    except Exception as e:
        logger.error(f"Failed to request measurement from simulator: {e}")
        measurement.status = MeasurementStatus.failed
        measurement.completed_at = datetime.now(timezone.utc)
        await measurement.save()
        raise HTTPException(
            status_code=503, detail="Failed to communicate with simulator"
        )

    if response.status_code in (200, 202):
        measurement.status = MeasurementStatus.acknowledged
        await measurement.save()
        return {
            "device_id": device_id,
            "status": "acknowledged",
            "request_id": request_id,
        }
    elif response.status_code == 409:
        measurement.status = MeasurementStatus.delayed
        await measurement.save()
        raise HTTPException(status_code=409, detail="Device is busy. Please try again later.")
    elif response.status_code == 503:
        measurement.status = MeasurementStatus.delayed
        await measurement.save()
        raise HTTPException(status_code=503, detail="Service temporarily unavailable.")
    else:
        measurement.status = MeasurementStatus.rejected
        measurement.completed_at = datetime.now(timezone.utc)
        await measurement.save()
        raise HTTPException(status_code=400, detail="Request rejected by simulator.")


async def process_webhook(request_id: str, status: str, results: dict | None) -> dict:
    measurement = await measurement_repository.get_measurement_by_request_id(request_id)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement request not found")

    try:
        measurement.status = MeasurementStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    measurement.completed_at = datetime.now(timezone.utc)

    if results:
        measurement.ph = cast(float, results.get("ph"))
        measurement.temperature_c = cast(float, results.get("temperature_c"))

    await measurement.save()
    return {"message": "Webhook processed successfully"}
