from fastapi import APIRouter
from fastapi.responses import HTMLResponse
router = APIRouter()
@router.get("/",response_class=HTMLResponse)
def alive():
    return "alive"