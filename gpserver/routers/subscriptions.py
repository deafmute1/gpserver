import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from const import formats
import dependencies
from database import operations
from sqlalchemy.orm import Session

from gpserver.routers import models

router_v1 = APIRouter(
    tags="subscriptions"
)
router_v2 = APIRouter(
    tags="subscriptions"
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
    subscriptions = operations.get_subscriptions_deltas(db, username, deviceid)


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
    username: str,
    deviceid: str,
    fmt: formats,
    db: Session = Depends(dependencies.get_db)
):
    # In case the device does not exist for the given user,
    # !!! it is automatically created.
    # If clients want to determine if a device exists, you have to to a GET request on the same URL first and check for a the 404 status code (see above).
    pass


class SubscriptionDeltas(BaseModel):
    add: list[str]
    remove: list[str]

@router_v2.post("/{username}/{deviceid}.json")
def upload_device_subscription_changes(
    username: str,
    deviceid: str,
    deltas: SubscriptionDeltas,
    db: Session = Depends(dependencies.get_db)
):
    # need to read source code to figure out what actual data is being returned - weirdly formed and formatted in docs.
    #format is:
    content = {
        'add':[],
        'remove':[],
        'timestamp':0
    }


@router_v2.post("/{username}/{_}.json")
@router_v2.post("/{username}.json")
def get_device_subscription_changes(
    username: str,
    since: Annotated[datetime.datetime, Query()] = 0,
    db: Session = Depends(dependencies.get_db)
):
    # deviceid doesn't matter here. or most places
    # notes from docs:
    # 'since' value SHOULD be timestamp value from the previous call to this API endpoint. If there has been no previous call, the cliend SHOULD use 0.
    # The response format is the same as the upload format: A dictionary with two keys “add” and “remove” where the value for each key is a list of URLs that should be added or removed. The timestamp SHOULD be stored by the client in order to provide it in the since parameter in the next request.
    pass
