from typing import Optional

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
    reading_date: str
    reading_value: float


# from sqlmodel import SQLModel, Field
# class Address(SQLModel):
#     id: int = Field(primary_key=True)
#     address_text: str


# class Meter(SQLModel):
#     id: int = Field(primary_key=True)
#     meter_name: str
#     address_id: int


# class Reading(SQLModel):
#     id: int = Field(primary_key=True)
#     meter_id: int
#     reading_date: str
#     reading_value: float
