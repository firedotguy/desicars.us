from fastapi import APIRouter

from app.routers.web import landing, car

router = APIRouter()

router.include_router(landing.router)
router.include_router(car.router)
