from fastapi import APIRouter
from typing import List
from src.repository import device_repository
from src.api.schema.device_schema import DeviceSchema

router = APIRouter()


@router.get("/devices", response_model=List[DeviceSchema])
async def list_devices():
    devices = await device_repository.get_all_devices()
    return devices
