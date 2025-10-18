from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.utils.env import get_int


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def get_landing(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stats_duration": get_int("STATS_DURATION", 1000),
            "target_contracts": get_int("TARGET_CONTRACTS", 100),
            "target_clients": get_int("TARGET_CLIENTS", 860),
            "target_cars": get_int("TARGET_CARS", 170),
            "target_new": get_int("TARGET_NEW", 10),
        },
    )
