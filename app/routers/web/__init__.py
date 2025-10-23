from fastapi import APIRouter

from app.routers.web import landing


router = APIRouter()

router.include_router(landing.router)