from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from .. import const

router = APIRouter()
@router.get("/",response_class=HTMLResponse)
def alive():
    return f'gpserver version {const.version} \n API docs at /docs or /redocs'