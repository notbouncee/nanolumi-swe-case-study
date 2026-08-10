from pydantic import BaseModel
from typing import List, Optional


class MeasurementRequest(BaseModel):
    device_id: str
    parameters: List[str]


class MeasurementResponse(BaseModel):
    device_id: str
    status: str
    request_id: str


class MeasurementResults(BaseModel):
    ph: Optional[float] = None
    temperature_c: Optional[float] = None
    turbidity_ntu: Optional[float] = None
    dissolved_oxygen_mg_l: Optional[float] = None


class WebhookPayload(BaseModel):
    request_id: str
    event_id: str
    status: str
    readings: Optional[MeasurementResults] = None
