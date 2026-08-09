from pydantic import BaseModel, ConfigDict


class DeviceSchema(BaseModel):
    id: int
    device_id: str
    name: str
    site_id: str
    site_name: str

    model_config = ConfigDict(from_attributes=True)
