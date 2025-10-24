from fastapi import APIRouter
from app.services.firestore import (
    fetch_active_contracts_count,
    fetch_cars_count,
    fetch_inactive_contracts_count,
    fetch_new_contracts_count,
)
from app.utils.env import get_int

router = APIRouter()


@router.get("")
def api_get_stats():
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

    return {
        "status": "success",
        "cars": cars,
        "contracts": contracts,
        "clients": clients,
        "new": new,
    }
