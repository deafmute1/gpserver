from typing import Sequence
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

#gpsever
from gpserver.database import schema, operations
from .. import dependencies
from . import models

router = APIRouter(
    tags=["Episode Actions API"]
)

@router.post("/{username}.json")
@router.post("/{username}" )
def upload_actions(
    actions: Sequence[models.Action],
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
    pass