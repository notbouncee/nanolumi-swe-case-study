import pytest
import respx
from httpx import AsyncClient, Response
from src.repository.models import DeviceMeasurement, MeasurementStatus, Device
import os

SIMULATOR_URL = os.getenv("SIMULATOR_URL", "http://simulator:9000")


@pytest.fixture
async def setup_device(async_client: AsyncClient):
    # Tests require a device in DB since sync_devices is skipped in testing
    await Device.create(
        device_id="device-001", name="Test Device", site_id="site-1", site_name="Site 1"
    )
    return "device-001"


@pytest.mark.asyncio
@respx.mock
async def test_request_measurement(async_client: AsyncClient, setup_device):
    respx.post(f"{SIMULATOR_URL}/api/devices/device-001/measurements").mock(
        return_value=Response(202, json={"status": "accepted"})
    )

    payload = {"device_id": "device-001", "parameters": ["ph"]}

    response = await async_client.post(
        "/api/devices/device-001/measurements", json=payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == "device-001"
    assert data["status"] == "acknowledged"
    assert "request_id" in data

    request_id = data["request_id"]

    db_measurement = await DeviceMeasurement.get_or_none(request_id=request_id)
    assert db_measurement is not None
    assert db_measurement.status == MeasurementStatus.acknowledged


@pytest.mark.asyncio
@respx.mock
async def test_request_measurement_idempotency(async_client: AsyncClient, setup_device):
    respx.post(f"{SIMULATOR_URL}/api/devices/device-001/measurements").mock(
        return_value=Response(202, json={"status": "accepted"})
    )

    payload = {"device_id": "device-001", "parameters": ["ph"]}

    resp1 = await async_client.post(
        "/api/devices/device-001/measurements", json=payload
    )
    assert resp1.status_code == 200

    resp2 = await async_client.post(
        "/api/devices/device-001/measurements", json=payload
    )
    assert resp2.status_code == 429


@pytest.mark.asyncio
@respx.mock
async def test_webhook_callback(async_client: AsyncClient, setup_device):
    respx.post(f"{SIMULATOR_URL}/api/devices/device-001/measurements").mock(
        return_value=Response(202)
    )

    resp = await async_client.post(
        "/api/devices/device-001/measurements",
        json={"device_id": "device-001", "parameters": ["ph"]},
    )
    request_id = resp.json()["request_id"]

    webhook_payload = {
        "request_id": request_id,
        "event_id": "evt-123",
        "status": "completed",
        "readings": {"ph": 7.5, "temperature_c": 22.1},
    }

    webhook_resp = await async_client.post(
        "/api/webhooks/simulator", json=webhook_payload
    )
    assert webhook_resp.status_code == 200

    db_measurement = await DeviceMeasurement.get_or_none(request_id=request_id)
    assert db_measurement is not None
    assert db_measurement.status == MeasurementStatus.completed
    assert db_measurement.ph == 7.5
    assert db_measurement.temperature_c == 22.1
