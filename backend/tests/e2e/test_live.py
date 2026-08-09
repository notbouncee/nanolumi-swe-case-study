import pytest
import httpx
import asyncio

BACKEND_URL = "http://localhost:8000/api"

@pytest.mark.asyncio
async def test_live_devices():
    """Verify we can fetch the synced devices from the live database."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/devices")
        assert response.status_code == 200
        devices = response.json()
        assert len(devices) > 0
        assert any(d["device_id"] == "device-001" for d in devices)

@pytest.mark.asyncio
async def test_live_measurement_request():
    """Verify the backend successfully proxies a measurement request to the live simulator."""
    payload = {
        "device_id": "device-001",
        "parameters": ["ph", "temperature_c"]
    }
    async with httpx.AsyncClient() as client:
        # Request a measurement
        response = await client.post(f"{BACKEND_URL}/devices/device-001/measurements", json=payload)
        
        # Due to our idempotency safeguard, if a previous run happened within 5 seconds, 
        # we might get a 429 Too Many Requests. Or the simulator might return 409 Conflict. Wait and retry if so.
        if response.status_code in (429, 409):
            await asyncio.sleep(5)
            response = await client.post(f"{BACKEND_URL}/devices/device-001/measurements", json=payload)
            
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "acknowledged"
        assert "request_id" in data
        assert data["device_id"] == "device-001"
