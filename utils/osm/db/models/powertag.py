from peewee import TextField
from base_model import BaseModel


class PowerTag(BaseModel):
    tag = TextField(unique=True)