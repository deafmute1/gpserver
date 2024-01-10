from datetime import datetime
from enum import Enum
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.sql import func
from typing import Optional


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(primary_key=True)
    devices: Mapped[set["Device"]] = relationship(back_populates="user")
    sessions: Mapped[list["Session"]] = relationship(back_populates="user")

    # favourites: Mapped[set["Favourite"]] = relationship(back_populates="user")
    # lists: Mapped[set["PodcastList"]] = relationship(back_populates="user")
    password_hash: Mapped[str]


class DeviceType(Enum):
    desktop = 'desktop'
    laptop = 'laptop'
    mobile = 'mobile'
    server = 'server'
    other = 'other'


class Device(Base):
    __tablename__ = 'device'
    device_id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        ForeignKey('user.username'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="devices")
    actions: Mapped[list["EpisodeAction"]] = relationship(back_populates="device")

    caption: Mapped[Optional[str]]
    device_type: Mapped[DeviceType]
    subscriptions: Mapped["SubscriptionAction"] = relationship(
        back_populates="device")


class Session(Base):
    __tablename__ = 'session'
    key: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        ForeignKey('user.username'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="sessions")
    created: Mapped[datetime]


class Podcast(Base):
    __tablename__ = 'podcast'
    url: Mapped[str] = mapped_column(primary_key=True)
    # episodes: Mapped[list["Episode"]] = relationship(back_populates="podcast")
    # favourites: Mapped[set["Favourite"]] = relationship(
    #     back_populates="podcast")

    website: Mapped[str]
    description: Mapped[str]
    subscribers: Mapped[int]
    title: Mapped[str]
    author: Mapped[str]
    logo_url: Mapped[Optional[str]]

    subscriptions: Mapped[set["SubscriptionAction"]] = relationship(back_populates="podcast")


# class Episode(Base):
#     __tablename__ = 'episode'
#     url: Mapped[str] = mapped_column(primary_key=True)
#     podcast_url: Mapped[str] = mapped_column(
#         ForeignKey('podcast.url'), primary_key=True)
#     podcast: Mapped["Podcast"] = relationship(back_populates="episodes")

#     actions: Mapped[list["EpisodeAction"]] = relationship(back_populates="episode")

#     description: Mapped[Optional[str]]
#     released: Mapped[datetime.datetime]
#     # website:Mapped[str] - this might be the same as the media url.
#     # how do clients use it?
#     # mygpo_link:Mapped[str] - don't know how this works or if we're handling it

class SubscriptionActionType(Enum):
    add = 1
    remove = -1

class SubscriptionAction(Base):
    __tablename__ = 'subscription'
    username: Mapped[str] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(primary_key=True)
    device: Mapped["Device"] = relationship(back_populates="subscriptions")
    __table_args__ = (
        ForeignKeyConstraint(['username', 'device_id'],
                             ['device.username', 'device.device_id']),
    )

    podcast_url: Mapped[str] = mapped_column(ForeignKey('podcast.url'),primary_key=True)
    podcast: Mapped["Podcast"] = relationship(back_populates="subscriptions")

    time: Mapped[datetime] = mapped_column(primary_key=True, server_default=func.now())
    action: Mapped[SubscriptionActionType]



EpisodeActionType = Enum('action', ['download', 'play', 'delete', 'new'])


class EpisodeAction(Base):
    __tablename__ = 'action'
    username: Mapped[str] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(primary_key=True)
    device: Mapped["Device"] = relationship(back_populates="actions")

    podcast_url: Mapped[str] = mapped_column(ForeignKey('podcast.url'),primary_key=True)
    # episode_url: Mapped[str] = mapped_column(primary_key=True)
    # episode: Mapped["Episode"] = relationship(back_populates="actions")

    __table_args__ = (
        ForeignKeyConstraint(['username', 'device_id'],
                             ['device.username', 'device.device_id']),
        # ForeignKeyConstraint(['podcast_url', 'episode_url'], [
        #                      'episode.podcast_url', 'episode.url'])
    )

    action: Mapped[EpisodeActionType] = mapped_column(primary_key=True)
    time: Mapped[datetime] = mapped_column(primary_key=True)
    started: Mapped[Optional[int]]
    position: Mapped[Optional[int]]
    total: Mapped[Optional[int]]


# class Favourite(Base): moved to boolean value in subscriptions
#     __tablename__ = 'favourite'
#     username: Mapped[str] = mapped_column(
#         ForeignKey('user.username'), primary_key=True)
#     user: Mapped["User"] = relationship(back_populates="favourites")

#     podcast_url: Mapped[str] = mapped_column(
#         ForeignKey('podcast.url'), primary_key=True)
#     podcast: Mapped["Podcast"] = relationship(back_populates="favourites")

# class Tag(Base):
#     __tablename__ = 'tag'
#     tag: Mapped[str] = mapped_column(primary_key=True)
#     title: Mapped[Optional[str]]
#     usage: Mapped[int]

# class PodcastList(Base):
#     __tablename__ = 'podcast_list'
#     username: Mapped[str] = mapped_column(
#         ForeignKey('user.username'), primary_key=True)
#     user: Mapped["User"] = relationship(back_populates="lists")

#     name: Mapped[str] = mapped_column(primary_key=True)
#     title: Mapped[Optional[str]]
