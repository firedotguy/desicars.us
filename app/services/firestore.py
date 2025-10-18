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

initialize_app(Certificate('key.json'))
db: Client = client()
logger = get_logger('firestore')


@timed_log
def fetch_cars_count() -> int:
    """Get all cars count."""
    logger.debug('get cars count')
    result = db.collection("cars").count().get()

    assert isinstance(result, QueryResultsList), f"Unexpected type: {type(result)}"

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug('total cars count: %s', inner_result[0].value)
    return int(inner_result[0].value)

@timed_log
def fetch_active_contracts_count() -> int:
    """Get all active contract count (where active is True)."""
    logger.debug('get active contracts count')
    result = db.collection('Contract').where(filter=FieldFilter('Active', '==', True)).count().get()

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug('total active contracts count: %s', inner_result[0].value)
    return int(inner_result[0].value)

@timed_log
def fetch_inactive_contracts_count() -> int:
    """Get all inactive contract count (where active is False)."""
    logger.debug('get inactive contracts count')
    result = db.collection('Contract').where(filter=FieldFilter('Active', '==', False)).count().get()

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug('total inactvie contracts count: %s', inner_result[0].value)
    return int(inner_result[0].value)

@timed_log
def fetch_new_contracts_count() -> int:
    """Get all new contracts count (created in last 31 days)."""
    logger.debug('get new contracts count')
    result = db.collection('Contract').where(filter=FieldFilter('begin_time', '>', datetime.now() - timedelta(days=31))).count().get()

    inner_result = cast(list[AggregationResult], result[0])
    logger.timed_debug('total new contracts count: %s', inner_result[0].value)
    return int(inner_result[0].value)


@timed_log
def fetch_gasoline_cars(limit: int = 10) -> list[dict]:
    """Get first N cars with gasoline line"""
    logger.debug('get first %s gasoline cars', limit)
    cars: list[dict] = []
    for car in db.collection('cars').where(filter=FieldFilter('type', '==', 'gasoline')).get():
        cars.append(map_car(car.to_dict() or {}))

    logger.timed_debug('fetched gasoline cars count: %s', len(cars))
    return cars