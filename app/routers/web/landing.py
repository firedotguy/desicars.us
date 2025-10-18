from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.utils.env import get_int
from app.services.firestore import fetch_active_contracts_count, fetch_cars_count, fetch_inactive_contracts_count, fetch_new_contracts_count


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def get_landing(request: Request):
    if get_int("TARGET_CONTRACTS", -1) == -1:
        contracts = fetch_active_contracts_count()
    else:
        contracts = get_int("TARGET_CONTRACTS", 100)

    if get_int("TARGET_CARS", -1) == -1:
        cars = fetch_cars_count()
    else:
        cars = get_int("TARGET_CARS", 170)

    if get_int("TARGET_CLIENTS", -1) == -1:
        clients = fetch_inactive_contracts_count()
    else:
        clients = get_int("TARGET_CLIENTS", 860)

    if get_int("TARGET_NEW", -1) == -1:
        new = fetch_new_contracts_count()
    else:
        new = get_int("TARGET_NEW", 50)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stats_duration": get_int("STATS_DURATION", 1000),
            "target_contracts": contracts,
            "target_clients": clients,
            "target_cars": cars,
            "target_new": new,
        },
    )
