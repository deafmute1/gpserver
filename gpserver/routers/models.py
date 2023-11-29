from pydantic import AnyHttpUrl, Base64Str, BaseModel
from ..database.schema import DeviceType, EpisodeActionType
from datetime import datetime


class BaseModelORM(BaseModel):
    model_config = { 'orm_mode' : True }

class SubscriptionDeltas(BaseModel):
    add: list[AnyHttpUrl]
    remove: list[AnyHttpUrl]

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

## Action
class Action(BaseModelORM):
    username: str
    device_id: str
    podcast_url: str
    episode_url: str
    action: EpisodeActionType
    timestamp: datetime

class ActionPlay(Action):
    started: int
    position: int
    total: int

##
class Favourite(BaseModelORM):
    username: str
    podcast_url: str