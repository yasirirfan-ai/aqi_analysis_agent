"""
Data models for the AQI Analysis Agent.
Author: Hazbilal3
"""
from typing import Dict, Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field

class AQIResponse(BaseModel):
    success: bool
    data: Dict[str, float]
    status: str
    expiresAt: str

class ExtractSchema(BaseModel):
    aqi: float = Field(description="Air Quality Index")
    temperature: float = Field(description="Temperature in degrees Celsius")
    humidity: float = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in kilometers per hour")
    pm25: float = Field(description="Particulate Matter 2.5 micrometers")
    pm10: float = Field(description="Particulate Matter 10 micrometers")
    co: float = Field(description="Carbon Monoxide level")

@dataclass
class UserInput:
    city: str
    state: str
    country: str
    medical_conditions: Optional[str]
    planned_activity: str
