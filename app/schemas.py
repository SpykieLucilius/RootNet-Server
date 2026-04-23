from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ReadingCreate(BaseModel):
    """Payload posted by a sensor module."""
    mac_address: str = Field(..., min_length=17, max_length=17)
    soil_moisture: Optional[int] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    light_lux: Optional[float] = None
    light_red: Optional[int] = None
    light_green: Optional[int] = None
    light_blue: Optional[int] = None
    battery_voltage: Optional[float] = None


class ReadingCreateResponse(BaseModel):
    status: str
    reading_id: int


class ReadingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    module_id: int
    timestamp: datetime
    soil_moisture: Optional[int]
    temperature: Optional[float]
    humidity: Optional[float]
    light_lux: Optional[float]
    battery_voltage: Optional[float]


class ReadingsListOut(BaseModel):
    count: int
    readings: List[ReadingOut]


class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mac_address: str
    name: str
    created_at: datetime
    last_seen_at: Optional[datetime]


class ModuleUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
