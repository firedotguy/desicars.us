from collections.abc import Callable
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles

from app.utils.env import get_bool, get_str
from app.utils.logger import setup_logging, format_request
from app.routers.web import landing

# get dotenv vars
DEBUG = get_bool('DEBUG', False)
LOG_LEVEL = get_str('LOG_LEVEL', 'DEBUG').upper()
LOG_COLORFUL = get_bool('LOG_COLORFUL', DEBUG)

# get base dir
BASE_DIR = Path(__file__).resolve().parent

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

# middleware
@app.middleware('http')
async def middleware(request: Request, call_next: Callable) -> Response:
    response: Response = await call_next(request)
    # custom access log
    logger.info(format_request(request, response), extra={"highlighter": None}) # remove number highlighting
    return response


# mount static files for templates
app.mount("/static", StaticFiles(directory=BASE_DIR / 'static'), name="static")

# favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")


app.include_router(landing.router)