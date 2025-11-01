from typing import Optional, List
from pydantic import BaseModel
from app.enums import CarColor, CarType, CarStatus, CarMake


class Vehicle(BaseModel):
    color: Optional[CarColor] = None
    make: Optional[CarMake] = None
    model: Optional[str] = None
    year: Optional[int] = None
    name: Optional[str] = None
    type: Optional[CarType] = None


class Car(BaseModel):
    nickname: str
    vehicle: Vehicle

    # changeoil: dict = {}
    # odometer: int = 0
    plate: Optional[str] = None
    # vin: str
    engine: Optional[str] = None
    fuel: float = 0.0
    # renter: Optional[str] = None
    price: Optional[float] = None
    status: CarStatus = CarStatus.FREE
    # relay_id: Optional[str] = None
    # relay_block: Optional[bool] = None
    # gps_phone: Optional[int] = None
    photos: List[str] = []
    web_photos: List[str] = []
    # tolltag: Optional[str] = None
    # imei: Optional[int] = None
    # timestamps: dict = {}

    class Config:
        from_attributes = True
