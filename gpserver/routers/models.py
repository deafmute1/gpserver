from typing import List, Literal, Optional, Sequence, Tuple
from pydantic import BaseModel, ValidationInfo, field_validator

from gpserver import const
from ..database.schema import DeviceType
from datetime import datetime


class BaseModelORM(BaseModel):
    model_config = { 'orm_mode' : True }

## Session
class SessionToken(BaseModelORM):
    key: str
    username: str

class SessionTokenTimestamp(SessionToken):
    created: datetime

## User
class User(BaseModelORM):
    username: str

class UserCreate(User):
    password: str

## Device
class Device(BaseModelORM):
    id: str
    caption: str
    type: DeviceType

class DeviceCreate(Device):
    username: str

class Podcast(BaseModelORM):
    url: str
    website: str
    description: str
    subscribers: int
    title: str
    author: str
    logo_url: str

class Episode(BaseModelORM):
    url: str
    podcast_url: str
    description: str
    released: datetime

class Subscription(BaseModelORM):
    username:str
    device_id: str
    podcast_url:str
    timestamp: datetime

## Actions 
class Action(BaseModelORM):
    podcast: str
    episode: str
    device: str
    timestamp: datetime
    action: const.episodeActionsLiteral
    position: Optional[int]
    started: Optional[int] 
    total: Optional[int]
    @field_validator('started', 'position', 'total', mode='after')
    @classmethod
    def validate_play_fields(cls, v: Optional[int], info: ValidationInfo):
        if info.data['action'] != "play": 
            if v is not None: 
                raise ValueError(f'{info.field_name} must be None if action != play')
        else: 
            if info.field_name == "started" and (
                info.data['position'] is None or info.data['total'] is None
            ): 
                raise ValueError(f'started field requires position and total to be set')
            elif info.field_name == "total" and (
                info.data['position'] is None or info.data['started'] is None
            ):
                raise ValueError('total field requires position and started to be set')

class ChangeUploadReponse(BaseModelORM):
    timestamp: float
    update_urls: List[Tuple[str, str]]

## Subscriptions
class SubscriptionDeltas(BaseModelORM):
    add: Sequence[str]
    remove: Sequence[str]
    
class TimeStampedSubscriptionDeltas(SubscriptionDeltas):
    timestamp: int 