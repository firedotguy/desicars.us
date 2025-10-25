from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, HTMLResponse

from app.services.firestore import fetch_cars

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")


@router.get("/cars", response_class=HTMLResponse)
def get_cars(request: Request):
    return templates.TemplateResponse(request, "pages/cars.html", {})


@router.get("/car", response_class=HTMLResponse)
def get_car_list():
    return RedirectResponse("/cars")


@router.get("/car/{nickname}", response_class=HTMLResponse)
def get_car(request: Request, nickname: str):
    pass
