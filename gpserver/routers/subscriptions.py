# stdlib
from datetime import datetime
from typing import Annotated

# pip
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from w3lib import url
from sqlalchemy.orm import Session

#gpserver
from gpserver.database import schema, operations
from ..const import formatsLiteral
from .. import dependencies
from . import models

router_v1 = APIRouter(
    tags=["Subscriptions API"]
)
router_v2 = APIRouter(
    tags=["Subscriptions API"]
)

@router_v1.get("/test")
def test(astr: str):
    return ""

@router_v1.get("/{username}/{deviceid}.{fmt}")
def get_device_subscriptions(
    response: Response,
    deviceid: str,
    fmt: formatsLiteral,
    jsonp: Annotated[str, Query()],
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
    raise NotImplementedError


@router_v1.get("/{username}.{fmt}")
def get_subscriptions(
    response: Response,
    fmt: formatsLiteral,
    jsonp: Annotated[str, Query()],
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
   raise NotImplementedError 


@router_v1.put("/{username}/{deviceid}.{fmt}")
def upload_device_subscriptions(
    request: Request,
    deviceid: str,
    fmt: formatsLiteral,
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
            case _:
                raise HTTPException(415,"This subscription format is currently unsupported")

@router_v2.post("/{username}/{deviceid}.json")
@router_v2.post("/{username}/{deviceid}")
def upload_subscription_actions(
    deltas: models.SubscriptionDeltas,
    deviceid: str,
    username: str = Depends(dependencies.auth_user),
    db: Session = Depends(dependencies.get_db)
):
    deltas_new = models.SubscriptionDeltas(
        add=list(map(url.canonicalize_url, deltas.add)),
        remove=list(map(url.canonicalize_url, deltas.remove))
    )
    with db.begin():
        operations.add_subscription_deltas(db, username, deviceid, deltas_new)
        time = operations.get_newest_subscription_delta_time(db)
    return models.ChangeUploadReponse(
        timestamp = time.timestamp(),
        update_urls = [
            e for e in zip(deltas.add + deltas.remove, deltas_new.add + deltas_new.remove, strict=True)
        ]       
    )

@router_v2.get("/{username}/{_}.json")
@router_v2.get("/{username}.json")
def get_subscription_actions(
    username: str = Depends(dependencies.auth_user),
    since: int = 0,
    db: Session = Depends(dependencies.get_db)
): 
    since = datetime.fromtimestamp(since)
    with db.begin():
        time = operations.get_newest_subscription_delta_time(db) 
        add = operations.get_subscriptions_deltas(
                db, username=username, since=since, action=schema.SubscriptionActionType.add
            )
        remove = operations.get_subscriptions_deltas(
                db, username=username, since=since, action=schema.SubscriptionActionType.remove
            )
    return models.TimeStampedSubscriptionDeltas(add=add, remove=remove, timestamp=time.timestamp())