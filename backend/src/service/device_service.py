import httpx
import logging
from src.repository import device_repository
import os

logger = logging.getLogger(__name__)

SIMULATOR_URL = os.getenv("SIMULATOR_URL", "http://simulator:9000")


async def sync_devices():
    """Fetches devices from the simulator and upserts them into the database."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SIMULATOR_URL}/api/devices")
            response.raise_for_status()
            devices_data = response.json()

            for d in devices_data:
                await device_repository.create_or_update_device(
                    device_id=d["device_id"],
                    name=d["name"],
                    site_id=d["site_id"],
                    site_name=d["site_name"],
                )
            logger.info(
                f"Successfully synced {len(devices_data)} devices from simulator."
            )
    except Exception as e:
        logger.error(f"Failed to sync devices from simulator: {e}")
