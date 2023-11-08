from pydantic import BaseModel
from .schema import DeviceType, ActionType
import datetime

class BaseModelORM(BaseModel):
    model_config = { 'orm_mode' : True }

class SessionToken(BaseModelORM):
    key: bytes
    username: str
    

class SessionTokenTimestamp(SessionToken):
    created: datetime.datetime

class User(BaseModelORM):
    username: str

class UserCreate(User):
    password: str

class Device(BaseModelORM):
    id: str
    username: str
    caption: str
    type: DeviceType
    subscriptions: int

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
    released: datetime.datetime

class Subscription(BaseModelORM):
    username:str
    device_id: str
    podcast_url:str
    timestamp: datetime.datetime
    class Config:
        orm_mode = True

class Action(BaseModelORM):
    username: str
    device_id: str
    podcast_url: str
    episode_url: str
    action: ActionType
    timestamp: datetime.datetime


class ActionPlay(Action):
    started: int
    position: int
    total: int

class Favourite(BaseModelORM):
    username: str
    podcast_url: str