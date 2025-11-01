from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")


@router.get("/cars", response_class=HTMLResponse)
def get_cars(request: Request):
    # Render page; client JS fetches cars and applies filters.
    qp = request.query_params
    context = {
        "request": request,
        # Provide filters for template conditionals (safe defaults)
        "filters": {
            "type": qp.get("type"),
            "make": qp.get("make"),
            "price": {
                'min': qp.get('price_min', 0),
                'max': qp.get('price_max', 1000)
            },
            "sort": qp.get("sort")
        }
    }
    return templates.TemplateResponse(request, "pages/cars.html", context)


@router.get("/car", response_class=HTMLResponse)  # redirect to /cars page
def get_car_list():
    return RedirectResponse("/cars")


@router.get("/car/{nickname}", response_class=HTMLResponse)
def get_car(request: Request, nickname: str):
    pass # TODO
