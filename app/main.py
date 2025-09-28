from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.utils.env import get_bool, get_str
from app.utils.logger import setup_logging

# get dotenv vars
DEBUG = get_bool('DEBUG', False)
LOG_LEVEL = get_str('LOG_LEVEL', 'DEBUG').upper()
LOG_COLORFUL = get_bool('LOG_COLORFUL', DEBUG)


# setup logger
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = setup_logging(LOG_LEVEL, LOG_COLORFUL)
logger.debug('CONFIG: DEBUG=%s LOG_LEVEL=%s LOG_COLORFUL=%s', DEBUG, LOG_LEVEL, LOG_COLORFUL)


# lifespan (custom startup & shutdown logging)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("DesiCars server started")
    try:
        yield
    finally:
        logger.info("DesiCars server stopped")

# create fastapi app
app = FastAPI(
    debug=DEBUG,
    title='DesiCars',
    description='DesiCars - car rental company in Texas',
    version='0.1.0',
    lifespan=lifespan
)


# mount static files for templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
