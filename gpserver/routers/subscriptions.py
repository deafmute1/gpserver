from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel

from gpserver.database import schema
from ..const import formats
from .. import dependencies
from ..database import operations
from sqlalchemy.orm import Session
from datetime import datetime
import urllib.parse

from . import models

router_v1 = APIRouter(
    tags=["subscriptions"]
)
router_v2 = APIRouter(
    tags=["subscriptions"]
)

# namespace issue with using 'format' - format is a reserved word.


@router_v1.get("/{username}/{deviceid}.{fmt}")
def get_device_subscriptions(
    response: Response,
    username: str,
    deviceid: str,
    fmt: formats,
    jsonp: Annotated[str, Query()],
    db: Session = Depends(dependencies.get_db)
):
    subscriptions = operations.get_subscriptions(db, username, deviceid)


@router_v1.get("/{username}.{fmt}")
def get_subscriptions(
    response: Response,
    username: str,
    fmt: formats,
    jsonp: Annotated[str, Query()],
    db: Session = Depends(dependencies.get_db)
):
    subscriptions = operations.get_subscriptions_deltas(db, username)


@router_v1.put("/{username}/{deviceid}.{fmt}")
def upload_device_subscriptions(
    request: Request,
    username: str,
    deviceid: str,
    fmt: formats,
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
    username: str,
    deviceid: str,
    deltas: models.SubscriptionDeltas,
    db: Session = Depends(dependencies.get_db)
):
    deltas_new = models.SubscriptionDeltas(
        add=map(deltas.add, urllib.parse.quote),
        remove=map(deltas.remove, urllib.parse.quote)
    )
    time = operations.add_subscription_deltas(db, username, deviceid, deltas_new)
    return {
        "timestamp" : int(time.timestamp()),
        "update_urls" : [
            e for e in zip(deltas_new.add + deltas.add, deltas_new.remove, deltas.remove) 
        ]       
    }

class TimeStampedSubscriptionDeltas(models.SubscriptionDeltas):
    timestamp: int 

@router_v2.post("/{username}/{_}.json")
@router_v2.post("/{username}.json")
def get_device_subscription_changes(
    username: str,
    since: int = 0,
    db: Session = Depends(dependencies.get_db)
): 
    since = datetime.fromtimestamp(since)
    time = operations.get_newest_subscription_delta_timestamp() 
    return TimeStampedSubscriptionDeltas(
        add = operations.get_subscriptions_deltas(
            db, username=username, since=since, action=schema.SubscriptionActionType.add
        ),
        remove = operations.get_subscriptions_deltas(
            db, username=username, since=since, action=schema.SubscriptionActionType.remove
        )
        timestamp = time
    )
