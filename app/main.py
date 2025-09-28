import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.utils.env import get_bool, get_str

# get dotenv vars
DEBUG = get_bool('DEBUG', False)
LOG_LEVEL = get_str('LOG_LEVEL', 'DEBUG').upper()

# setup logger
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger('desicars')
logger.debug('CONFIG: DEBUG=%s LOG_LEVEL=%s', DEBUG, LOG_LEVEL)

# create fastapi app
app = FastAPI(
    debug=DEBUG,
    title='DesiCars',
    description='DesiCars - car rental company in Texas',
    version='0.1.0'
)


# mount static files for templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")