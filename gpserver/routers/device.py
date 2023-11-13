from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from gpserver import dependencies
from gpserver.database.schema import DeviceType

devices_router = APIRouter(
    tags="devices"
)

devices_updates_router = APIRouter(
    tags="devices"
)

class DeviceData(BaseModel):
    caption:str
    type:DeviceType

@devices_router.post("/{username}/{deviceid}.json")
def update_device(
    username: str,
    deviceid: str,
    device:DeviceData,
    db: Session = Depends(dependencies.get_db)
):
    pass


@devices_router.get("/{username}.json")
def list_devices(
    username: str,
    db: Session = Depends(dependencies.get_db)
):
    pass

@devices_updates_router.get("/{username}/{deviceid}.json")
def get_device_updates(
    username:str,
    deviceid:str,
    db:Session = Depends(dependencies.get_db)
):
    pass

