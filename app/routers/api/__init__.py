from fastapi import APIRouter

from app.routers.api import stats, car

router = APIRouter(prefix="/api")

router.include_router(stats.router, prefix="/stats")
router.include_router(car.router, prefix="/cars")
