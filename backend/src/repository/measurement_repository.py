from .models import DeviceMeasurement, MeasurementStatus, Device
from datetime import datetime
from typing import List


async def get_measurements_by_device(device_id: str) -> List[DeviceMeasurement]:
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        return []
    return await DeviceMeasurement.filter(device=device).order_by("-requested_at")


async def get_latest_measurement(device_id: str) -> DeviceMeasurement | None:
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        return None
    return (
        await DeviceMeasurement.filter(device=device).order_by("-requested_at").first()
    )


async def create_measurement(
    request_id: str, device_id: str, requested_at: datetime
) -> DeviceMeasurement:
    device = await Device.get(device_id=device_id)
    return await DeviceMeasurement.create(
        request_id=request_id,
        device=device,
        requested_at=requested_at,
        status=MeasurementStatus.pending,
    )


async def get_measurement_by_request_id(request_id: str) -> DeviceMeasurement | None:
    return await DeviceMeasurement.get_or_none(request_id=request_id)
