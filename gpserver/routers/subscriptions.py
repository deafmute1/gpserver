from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel
from w3lib import url

from gpserver.database import schema
from ..const import formats
from .. import dependencies
from ..database import operations
from sqlalchemy.orm import Session
from datetime import datetime

from . import models

router_v1 = APIRouter(
    tags=["subscriptions"]
)
router_v2 = APIRouter(
    tags=["subscriptions"]
)

@router_v1.get("/{username}/{deviceid}.{fmt}")
def get_device_subscriptions(
    response: Response,
    deviceid: str,
    fmt: formats,
    jsonp: Annotated[str, Query()],
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
    subscriptions = operations.get_subscriptions(db, username, deviceid)


@router_v1.get("/{username}.{fmt}")
def get_subscriptions(
    response: Response,
    fmt: formats,
    jsonp: Annotated[str, Query()],
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
    subscriptions = operations.get_subscriptions_deltas(db, username)


@router_v1.put("/{username}/{deviceid}.{fmt}")
def upload_device_subscriptions(
    request: Request,
    deviceid: str,
    fmt: formats,
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
    # In case the device does not exist for the given user,
    # !!! it is automatically created.
    # If clients want to determine if a device exists, you have to to a GET request on the same URL first and check for a the 404 status code (see above).
    with db.begin():
        if (device := operations.get_device(db, username, deviceid)) is None:
                device = operations.create_device(
                    db, models.DeviceCreate(
                        id=deviceid,
                        username=username,
                        caption='',
                        type='other'
                    ))
        match fmt:
            case 'json':
                #request.json()
                #not sure what actual json content to expect here
                return request.json()
                operations.add_subscription_deltas(db,username,deviceid,)
            case _:
                raise HTTPException(415,"This subscription format is currently unsupported")

class SubcriptionUploadReponse(BaseModel):
    timestamp: float
    update_urls: list[tuple[str, str]]


@router_v2.post("/{username}/{deviceid}.json", response_model=SubcriptionUploadReponse)
def upload_device_subscription_changes(
    deltas: models.SubscriptionDeltas,
    deviceid: str,
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
    deltas_new = models.SubscriptionDeltas(
        add=list(map(url.canonicalize_url, deltas.add)),
        remove=list(map(url.canonicalize_url, deltas.remove))
    )
    time = operations.add_subscription_deltas(db, username, deviceid, deltas_new)
    return {
        "timestamp" : time.timestamp(),
        "update_urls" : [
            e for e in zip(deltas.add + deltas.remove, deltas_new.add + deltas_new.remove) 
        ]       
    }

class TimeStampedSubscriptionDeltas(models.SubscriptionDeltas):
    timestamp: int 

@router_v2.get("/{username}/{_}.json")
@router_v2.get("/{username}.json")
def get_device_subscription_changes(
    username: str = Depends(dependencies.auth_user),
    since: int = 0,
    db: Session = Depends(dependencies.get_db)
): 
    since = datetime.fromtimestamp(since)
    time = operations.get_newest_subscription_delta_timestamp(db) 
    return TimeStampedSubscriptionDeltas(
        add = operations.get_subscriptions_deltas(
            db, username=username, since=since, action=schema.SubscriptionActionType.add
        ),
        remove = operations.get_subscriptions_deltas(
            db, username=username, since=since, action=schema.SubscriptionActionType.remove
        ),
        timestamp = time.timestamp()
    )
