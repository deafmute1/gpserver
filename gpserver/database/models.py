from pydantic import BaseModel
from .schema import DeviceType, ActionType
import datetime


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(User):
    password_hash: str
    password_salt: str


class Device(BaseModel):
    id: str
    username: str
    caption: str
    type: DeviceType
    subscriptions: int

    class Config:
        orm_mode = True


class Podcast(BaseModel):
    url: str
    website: str
    description: str
    subscribers: int
    title: str
    author: str
    logo_url: str

    class Config:
        orm_mode = True


class Episode(BaseModel):
    url: str
    podcast_url: str
    description: str
    released: datetime.datetime

    class Config:
        orm_mode = True

class Subscription(BaseModel):
    username:str
    device_id: str
    podcast_url:str
    timestamp: datetime.datetime
    class Config:
        orm_mode = True

class Action(BaseModel):
    username: str
    device_id: str
    podcast_url: str
    episode_url: str
    action: ActionType
    timestamp: datetime.datetime

    class Config:
        orm_mode = True


class ActionPlay(Action):
    started: int
    position: int
    total: int


class Favourite(BaseModel):
    username: str
    podcast_url: str

    class Config:
        orm_mode = True
