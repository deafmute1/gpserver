from datetime import datetime
import itertools
from sqlalchemy import Result, Row, insert, select, update, func

from ..routers import models
from . import schema
from typing import Any, NamedTuple, Optional
from ..const import hasher
from collections.abc import Sequence, Mapping

from sqlalchemy.orm import Session, InstrumentedAttribute

# User


class ColumnFilters(NamedTuple):
    user = [schema.User.username,]
    subscription = [schema.SubscriptionAction.podcast_url,]


def create_user(db: Session, user: models.UserCreate) -> schema.User | None:
    user = schema.User(
        username=user.username,
        password_hash=hasher.hash(user.password),
    )
    db.add(user)
    return user


def get_user(db: Session, username: str) -> schema.User | None:
    return db.get(schema.User, username)


def get_user_filtered(db: Session, username: str):
    return db.execute(
        select(*ColumnFilters.user)
        .where(schema.User.username == username)
    ).one_or_none()


def get_all_users_filtered(db: Session):
    return db.execute(select(*ColumnFilters.user)).all()


def update_user(db: Session, username: str, updates: Mapping[str, Any]):
    user = get_user(db, username)
    for col, val in updates:
        if col == 'password':
            col, val = 'password_hash', hasher.hash(val)
        setattr(user, col, val)
    return user


def delete_user(db: Session, user: schema.User):
    db.delete(user)

# Session


def create_session(db: Session, session: models.SessionTokenTimestamp) -> schema.Session | None:
    session = schema.Session(
        key=session.key,
        username=session.username,
        created=session.created
    )
    db.add(session)
    return session


def get_session(db: Session, session: models.SessionToken) -> schema.Session | None:
    return db.get(schema.Session,
                  {"key": session.key, "username": session.username})


def delete_session(db: Session, session: models.SessionToken):
    db.delete(get_session(db, session))

# Device


def create_device(db: Session, device: models.DeviceCreate) -> schema.Device | None:
    device = schema.Device(
        device_id=device.id,
        username=device.username,
        caption=device.caption,
        device_type=device.type,
    )
    db.add(device)
    return device


def get_device(db: Session, username: str, device_id: str):
    return db.get(schema.Device,
                  {"username": username, "device_id": device_id})

# Subscription


def get_subscriptions_deltas(
    db: Session, 
    username: Optional[str] = None, device_id: Optional[str] = None, 
    since: Optional[datetime] = None, action: Optional[schema.SubscriptionActionType] = None
    ):
    subscriptions = select(schema.SubscriptionAction.podcast_url) \
        .distinct(schema.SubscriptionAction.podcast_url)
    if username is not None:
        subscriptions = subscriptions.where(schema.SubscriptionAction.username == username) 
    if device_id is not None:
        subscriptions = subscriptions.where(schema.SubscriptionAction.device_id == device_id)
    if since is not None: 
        subscriptions = subscriptions.where(schema.SubscriptionAction.time > since)
    if action is not None: 
        subscriptions = subscriptions.where(schema.SubscriptionAction.action == action)
    return db.execute(subscriptions).scalars().all()

def get_newest_subscription_delta_timestamp(db: Session) -> datetime:
    return db.execute(select(func.max(schema.SubscriptionAction.time))).scalar()

def add_subscription_deltas(
    db: Session, username: str, deviceid: str,
    deltas: models.SubscriptionDeltas
) -> datetime:
    shared_kwargs = {
        "username": username,
        "device_id": deviceid,
    }
    actions = list(itertools.chain(
        (
            schema.SubscriptionAction(
                **shared_kwargs, podcast_url=e, action=schema.SubscriptionActionType.add
            ) for e in deltas.add
        ),
        (
            schema.SubscriptionAction(
                **shared_kwargs, podcast_url=e, action=schema.SubscriptionActionType.remove
            ) for e in deltas.remove
        )
    ))
    db.add_all(actions)
    db.commit() # commit so we have retrievable timestamp
    return actions[0].time 


def get_subscriptions(db: Session, username: str = None, device_id: str = None):
    subscriptions = select(*ColumnFilters.subscription)
    if username is not None:
        subscriptions = subscriptions.where(
            schema.SubscriptionAction.username == username)
        if device_id is not None:
            subscriptions = subscriptions.where(
                schema.SubscriptionAction.device_id == device_id)
    return db.execute(
        subscriptions
        .group_by(schema.SubscriptionAction.podcast_url)
        # need to change the way this works to be not jank. maybe look at a canonical way of implementing deltas in cs and copy that.
        .having(func.sum(schema.SubscriptionAction.action) > 0)
    ).all()
