from base_model import BaseModel
from peewee import BigIntegerField, ForeignKeyField, TextField, FloatField, BooleanField
from powertag import PowerTag


class DataPoint(BaseModel):
    node_id = BigIntegerField(null=False, unique=True)
    power_tag = ForeignKeyField(PowerTag)
    tags = TextField()
    # timestamp = TimestampField()
    latitude = FloatField()
    longitude = FloatField()
    downloaded = BooleanField(default=False)