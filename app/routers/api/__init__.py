from fastapi import APIRouter

from app.routers.api import stats

router = APIRouter(prefix="/api")

router.include_router(stats.router, prefix="/stats")
