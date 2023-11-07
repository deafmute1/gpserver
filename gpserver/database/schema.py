import datetime
from enum import Enum
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from typing import Set

Base = DeclarativeBase


class User(Base):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(primary_key=True)
    # TODO check if I can use set rather than Set - not sure it'll work
    devices: Mapped[set["Device"]] = relationship(back_populates="user")
    favourites: Mapped[set["Favourite"]] = relationship(back_populates="user")
    lists: Mapped[set["PodcastList"]] = relationship(back_populates="user")


class Device(Base):
    __tablename__ = 'device'
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        ForeignKey('user.username'), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="devices")
    actions: Mapped[list["Action"]] = relationship(back_populates="device")


class Tag(Base):
    __tablename__ = 'tag'
    tag: Mapped[str] = mapped_column(primary_key=True)


class Podcast(Base):
    __tablename__ = 'podcast'
    url: Mapped[str] = mapped_column(primary_key=True)
    episodes: Mapped[list["Episode"]] = relationship(back_populates="podcast")
    favourites: Mapped[set["Favourite"]] = relationship(back_populates="podcast")


class Episode(Base):
    __tablename__ = 'episode'
    url: Mapped[str] = mapped_column(primary_key=True)
    podcast_url: Mapped[str] = mapped_column(
        ForeignKey('podcast.url'), primary_key=True)
    podcast: Mapped["Podcast"] = relationship(back_populates="episodes")
    
    actions: Mapped[list["Action"]] = relationship(back_populates="episode")


class Action(Base):
    __tablename__ = 'action'
    username: Mapped[str] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(primary_key=True)
    device: Mapped["Device"] = relationship(back_populates="actions")

    podcast_url: Mapped[str] = mapped_column(primary_key=True)
    episode_url: Mapped[str] = mapped_column(primary_key=True)
    episode: Mapped["Episode"] = relationship(back_populates="actions")

    action: Mapped[Enum(
        'action',
        ['download', 'play', 'delete', 'new'])] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['username', 'device_id'],
                             ['user.username', 'device.id']),
        ForeignKeyConstraint(['podcast_url', 'episode_url'], [
                             'episode.podcast_url', 'episode.url'])
    )


class PodcastList(Base):
    __tablename__ = 'podcast_list'
    username: Mapped[str] = mapped_column(
        ForeignKey('user.username'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="lists")
    
    name: Mapped[str] = mapped_column(primary_key=True)


class Favourite(Base):
    __tablename__ = 'favourite'
    username: Mapped[str] = mapped_column(
        ForeignKey('user.username'), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="favourites")
    
    podcast_url: Mapped[str] = mapped_column(
        ForeignKey('podcast.url'), primary_key=True)
    podcast: Mapped["Podcast"] = relationship(back_populates="favourites")
