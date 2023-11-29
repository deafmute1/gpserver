from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from gpserver import dependencies
from gpserver.routers import models
from ..database import operations

from gpserver.database.schema import DeviceType

devices_router = APIRouter(
    tags=["devices"]
)

devices_updates_router = APIRouter(
    tags=["devices"]
)


class DeviceData(BaseModel):
    caption: str
    type: DeviceType


@devices_router.post("/{username}/{deviceid}")
@devices_router.post("/{username}/{deviceid}.json")
def update_device(
    username: str,
    deviceid: str,
    data: DeviceData,
    db: Session = Depends(dependencies.get_db)
):
    with db.begin():
        if (device := operations.get_device(db, username, deviceid)) is None:
            operations.create_device(
                db, models.DeviceCreate(
                    id=deviceid,
                    username=username,
                    caption=data.caption,
                    type=data.type
                ))
        else:
            device.caption, device.device_type = data.caption, data.type


@devices_router.get("/{username}")
@devices_router.get("/{username}.json")
def list_devices(
    username: str,
    db: Session = Depends(dependencies.get_db)
):
    with db.begin():
        return [models.Device(id=device.device_id, caption=device.caption, type=device.device_type) for device in operations.get_user(db, username).devices]


@devices_updates_router.get("/{username}/{deviceid}")
@devices_updates_router.get("/{username}/{deviceid}.json")
def get_device_updates(
    username: str,
    deviceid: str,
    db: Session = Depends(dependencies.get_db)
):
    pass
