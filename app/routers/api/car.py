from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.enums import CarType
from app.schemas.car import CarSchema
from app.services.firestore import fetch_cars, fetch_car

router = APIRouter()


@router.get("/", response_model=List[CarSchema])
def api_get_cars(
    type: Optional[CarType] = Query(None, description="Filter by car type"),
    active: Optional[bool] = Query(None, description="Filter by status: True=rent, False=free"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
):
    """Return list of cars with optional filters."""
    cars: List[CarSchema] = fetch_cars(type=type, active=active, limit=limit)
    return cars


@router.get("/{nickname}", response_model=CarSchema)
def api_get_car(nickname: str):
    """Return single car by nickname."""
    car = fetch_car(nickname)
    if car is None:
        return JSONResponse(
            content={
                "status": "fail",
                "detail": f"Car '{nickname}' not found",
            },
            status_code=404,
        )

    return car
