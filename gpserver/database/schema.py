import datetime
from enum import Enum
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from typing import Optional


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(primary_key=True)
    # TODO check if I can use set rather than Set - not sure it'll work
    devices: Mapped[set["Device"]] = relationship(back_populates="user")
    sessions: Mapped[set["Device"]] = relationship(back_populates="user")

    # favourites: Mapped[set["Favourite"]] = relationship(back_populates="user")
    # lists: Mapped[set["PodcastList"]] = relationship(back_populates="user")
    password_hash: Mapped[str]


DeviceType = Enum('type', ['desktop', 'laptop', 'mobile', 'server', 'other'])


class Device(Base):
    __tablename__ = 'device'
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        ForeignKey('user.username'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="devices")
    actions: Mapped[list["Action"]] = relationship(back_populates="device")

    caption: Mapped[Optional[str]]
    type: Mapped[DeviceType]
    subscriptions: Mapped["Subscription"] = relationship(
        back_populates="device")


class Session(Base):
    __tablename__ = 'session'
    key: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(ForeignKey('user.username'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="sessions")
    created: Mapped[datetime.datetime]


class Podcast(Base):
    __tablename__ = 'podcast'
    url: Mapped[str] = mapped_column(primary_key=True)
    episodes: Mapped[list["Episode"]] = relationship(back_populates="podcast")
    # favourites: Mapped[set["Favourite"]] = relationship(
    #     back_populates="podcast")

    website: Mapped[str]
    description: Mapped[str]
    subscribers: Mapped[int]
    title: Mapped[str]
    author: Mapped[str]
    logo_url: Mapped[Optional[str]]

    subscriptions: Mapped[set["Subscription"]
                          ] = relationship(back_populates="podcast")


class Episode(Base):
    __tablename__ = 'episode'
    url: Mapped[str] = mapped_column(primary_key=True)
    podcast_url: Mapped[str] = mapped_column(
        ForeignKey('podcast.url'), primary_key=True)
    podcast: Mapped["Podcast"] = relationship(back_populates="episodes")

    actions: Mapped[list["Action"]] = relationship(back_populates="episode")

    description: Mapped[Optional[str]]
    released: Mapped[datetime.datetime]
    # website:Mapped[str] - this might be the same as the media url.
    # how do clients use it?
    # mygpo_link:Mapped[str] - don't know how this works or if we're handling it


class Subscription(Base):
    __tablename__ = 'subscription'
    username: Mapped[str] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(primary_key=True)
    device: Mapped["Device"] = relationship(back_populates="subscriptions")
    __table_args__ = (
        ForeignKeyConstraint(['username', 'device_id'],
                             ['device.username', 'device.id']),
    )

    podcast_url: Mapped[str] = mapped_column(
        ForeignKey('podcast.url'), primary_key=True)
    podcast: Mapped["Podcast"] = relationship(back_populates="subscriptions")

    timestamp: Mapped[datetime.datetime] = mapped_column(primary_key=True)


ActionType = Enum('action', ['download', 'play', 'delete', 'new'])


class Action(Base):
    __tablename__ = 'action'
    username: Mapped[str] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(primary_key=True)
    device: Mapped["Device"] = relationship(back_populates="actions")

    podcast_url: Mapped[str] = mapped_column(primary_key=True)
    episode_url: Mapped[str] = mapped_column(primary_key=True)
    episode: Mapped["Episode"] = relationship(back_populates="actions")

    __table_args__ = (
        ForeignKeyConstraint(['username', 'device_id'],
                             ['device.username', 'device.id']),
        ForeignKeyConstraint(['podcast_url', 'episode_url'], [
                             'episode.podcast_url', 'episode.url'])
    )

    action: Mapped[ActionType] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(primary_key=True)
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
