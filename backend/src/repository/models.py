from tortoise import fields, models
from enum import Enum


class MeasurementStatus(str, Enum):
    pending = "pending"
    acknowledged = "acknowledged"
    completed = "completed"
    failed = "failed"
    delayed = "delayed"
    rejected = "rejected"


class Device(models.Model):
    id = fields.IntField(primary_key=True)
    device_id = fields.CharField(max_length=255, unique=True, db_index=True)
    name = fields.CharField(max_length=255)
    site_id = fields.CharField(max_length=255)
    site_name = fields.CharField(max_length=255)

    measurements: fields.ReverseRelation["DeviceMeasurement"]

    class Meta:
        table = "devices"


class DeviceMeasurement(models.Model):
    id = fields.IntField(primary_key=True)
    request_id = fields.CharField(max_length=255, unique=True, db_index=True)

    # Notice we link to the device's internal pk (id) typically, but the user spec specifies linking to device_id.
    # We can just use standard FK to Device and then query it.
    device: fields.ForeignKeyRelation[Device] = fields.ForeignKeyField(
        "models.Device", related_name="measurements"
    )

    status = fields.CharEnumField(MeasurementStatus, default=MeasurementStatus.pending)

    requested_at = fields.DatetimeField()
    completed_at = fields.DatetimeField(null=True)

    ph = fields.FloatField(null=True)
    temperature_c = fields.FloatField(null=True)
    turbidity_ntu = fields.FloatField(null=True)
    dissolved_oxygen_mg_l = fields.FloatField(null=True)

    class Meta:
        table = "device_measurements"
