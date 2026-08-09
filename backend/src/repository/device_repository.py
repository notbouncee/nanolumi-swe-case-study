from .models import Device
from typing import List


async def get_all_devices() -> List[Device]:
    return await Device.all()


async def get_device_by_device_id(device_id: str) -> Device | None:
    return await Device.get_or_none(device_id=device_id)


async def create_or_update_device(
    device_id: str, name: str, site_id: str, site_name: str
) -> Device:
    device, created = await Device.update_or_create(
        device_id=device_id,
        defaults={"name": name, "site_id": site_id, "site_name": site_name},
    )
    return device
