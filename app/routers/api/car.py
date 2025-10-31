from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.enums import CarType, CarMake, CarSorting
from app.schemas.car import Car
from app.services.firestore import fetch_cars, fetch_car

router = APIRouter()


@router.get("/", response_model=List[Car])
def api_get_cars(
    type: Optional[CarType] = Query(None, description="Filter by car type"),
    active: Optional[bool] = Query(None, description="Filter by status: True=rent, False=free"),
    make: Optional[CarMake] = Query(None, description='Filter by car make/vehicle'),
    sort: CarSorting = Query(CarSorting.MODEL, description='Sorting type - year/price-asc/price-desc/model'),
    limit: Optional[int] = Query(None, description="Limit number of results"),
):
    """Return list of cars with optional filters."""
    cars: List[Car] = fetch_cars(type=type, active=active, make=make, sort=sort, limit=limit)
    return cars


@router.get("/{nickname}", response_model=Car)
def api_get_car(nickname: str):
    """Return single car by nickname."""
    car = fetch_car(nickname)
    if car is None:
        return JSONResponse(
            content={
                "status": "fail",
                "detail": f"Car '{nickname}' not found",
            },
            status_code=404
        )

    return car
