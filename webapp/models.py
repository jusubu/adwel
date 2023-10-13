from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Address(BaseModel):
    id: Optional[int] = None
    address_text: str


class Meter(BaseModel):
    id: Optional[int] = None
    meter_name: str
    address_id: int


class Reading(BaseModel):
    id: Optional[int] = None
    meter_id: int
    reading_date: datetime
    reading_value: float
