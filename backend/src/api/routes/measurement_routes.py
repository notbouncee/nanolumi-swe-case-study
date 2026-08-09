from fastapi import APIRouter
from src.api.schema.measurement_schema import (
    MeasurementRequest,
    MeasurementResponse,
    WebhookPayload,
)
from src.service import measurement_service

from typing import List

router = APIRouter()

@router.get("/devices/{device_id}/measurements")
async def get_device_measurements(device_id: str):
    measurements = await measurement_service.get_device_measurements(device_id)
    return measurements


@router.post("/devices/{device_id}/measurements", response_model=MeasurementResponse)
async def request_device_measurement(device_id: str, request: MeasurementRequest):
    return await measurement_service.request_measurement(device_id, request.parameters)


@router.post("/webhooks/simulator")
async def simulator_webhook(payload: WebhookPayload):
    results_dict = payload.readings.model_dump() if payload.readings else None
    await measurement_service.process_webhook(
        request_id=payload.request_id, status=payload.status, results=results_dict
    )
    return {"event_id": payload.event_id, "status": "received"}
