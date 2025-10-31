from datetime import datetime, timedelta
from typing import cast

from firebase_admin.firestore import client
from firebase_admin.credentials import Certificate
from firebase_admin import initialize_app
from google.cloud.firestore import Client
from google.cloud.firestore_v1.query_results import QueryResultsList
from google.cloud.firestore_v1.base_aggregation import AggregationResult
from google.cloud.firestore_v1.base_query import FieldFilter

from app.utils.firestore_mapper import map_car
from app.utils.logger import get_logger, timed_log
from app.enums import CarType
from app.schemas.car import Car

initialize_app(Certificate("key.json"))
db: Client = client()
logger = get_logger("firestore")


@timed_log
def fetch_cars_count() -> int:
    """Get all cars count."""
    logger.debug("fetch cars count")
    result = db.collection("cars").count().get()

    assert isinstance(result, QueryResultsList), f"Unexpected type: {type(result)}"

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug("total cars count: %s", inner_result[0].value)
    return int(inner_result[0].value)


@timed_log
def fetch_active_contracts_count() -> int:
    """Get all active contract count (where active is True)."""
    logger.debug("fetch active contracts count")
    result = (
        db.collection("Contract")
        .where(filter=FieldFilter("Active", "==", True))
        .count()
        .get()
    )

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug("total active contracts count: %s", inner_result[0].value)
    return int(inner_result[0].value)


@timed_log
def fetch_inactive_contracts_count() -> int:
    """Get all inactive contract count (where active is False)."""
    logger.debug("fetch inactive contracts count")
    result = (
        db.collection("Contract")
        .where(filter=FieldFilter("Active", "==", False))
        .count()
        .get()
    )

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug("total inactvie contracts count: %s", inner_result[0].value)
    return int(inner_result[0].value)


@timed_log
def fetch_new_contracts_count() -> int:
    """Get all new contracts count (created in last 31 days)."""
    logger.debug("fetch new contracts count")
    result = (
        db.collection("Contract")
        .where(
            filter=FieldFilter("begin_time", ">", datetime.now() - timedelta(days=31))
        )
        .count()
        .get()
    )

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug("total new contracts count: %s", inner_result[0].value)
    return int(inner_result[0].value)


@timed_log
def fetch_cars(
    type: CarType | None = None, active: bool | None = None, limit: int | None = None
) -> list[Car]:
    """Fetch cars data"""
    logger.debug(
        "fetch cars type=%s status=%s limit=%s",
        type.value if type else "all",
        "free" if active is False else "rent" if active is True else "all",
        limit or "no",
    )
    cars: list[Car] = []
    query = db.collection("cars")
    if type:
        query = query.where(filter=FieldFilter("type", "==", type.value))
    if active is not None:  # if false, do not passing, so checking only on None
        query = query.where(
            filter=FieldFilter(
                "status",
                "in",
                ("Занята", "занята", "Аренда", "аренда", "rent", "Rent")
                if active
                else ("Свободна", "свободна", "Free", "free"),
            )
        )
    if limit:
        query = query.limit(limit)

    for car in query.stream():
        cars.append(map_car(car.to_dict() or {}))

    logger.timed_debug("fetched cars count: %s", len(cars))
    return cars


@timed_log
def fetch_car(nickname: str) -> Car | None:
    """Fetch car by nickname."""
    logger.debug("fetch car nickname=%s", nickname)
    car = (
        db.collection("cars")
        .where(filter=FieldFilter("nickname", "==", nickname))
        .get()
    )
    if not car:
        logger.timed_debug("car not found")
        return
    logger.timed_debug("fetched car")
    return map_car(car[0].to_dict() or {})
