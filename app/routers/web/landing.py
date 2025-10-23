from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.utils.env import get_int


router = APIRouter()
templates = Jinja2Templates(directory="app/templates/")


@router.get("/", response_class=HTMLResponse)
def get_landing(request: Request):

    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "stats_duration": get_int("STATS_DURATION", 1000)
        },
    )
