from typing import Optional, List
from pydantic import BaseModel


class ContractSchema(BaseModel):
    active: bool
    start_odometer: Optional[float] = None
    payday_odometer: Optional[float] = None
    state: str = "TX"
    name: str
    nickname: str

    # document_photos: List[str] = []
    car_photos: List[str] = []
    car_close_photos: List[str] = []
    price: float = 0.0
    start_price: Optional[float] = None
    deposit: Optional[float] = None
    # discount: Optional[float] = None
    # promo_code: Optional[str] = None
    mil_limit: Optional[int] = None
    # saldo: Optional[float] = None

    # renter: dict = {}
    # insurance: dict = {}
    # license: dict = {}
    timestamps: dict = {}

    class Config:
        from_attributes = True
