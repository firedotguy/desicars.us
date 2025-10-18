from pydantic import BaseModel
from datetime import datetime

class VehicleInfo(BaseModel):
    color: str | None
    make: str | None
    model: str | None
    year: int | None
    name: str | None

class Car(BaseModel):
    nickname: str
    odometer: int
    vehicle: VehicleInfo
    vin: str | None
    plate: str | None
    status: str
    fuel: float
    engine: float
    timestamps: dict[str, datetime]