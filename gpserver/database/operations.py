from datetime import datetime
import itertools
from sqlalchemy import Row, select, update

from ..routers import models
from . import schema
from typing import Any, NamedTuple
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


def update_users(db: Session, users: Sequence[Mapping[str, Any]]):
    db.execute(
        update(schema.User),
        map(lambda user: dict(user), users)
    )


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


def get_session(db: Session, session: models.SessionToken) -> schema.Session | None:
    return db.get(
        schema.Session,
        {"key": session.key, "username": session.username}
    )


def delete_session(db: Session, session: models.SessionToken):
    db.delete(get_session(db, session))

# Device


def create_device(db: Session, device: models.Device) -> schema.Device | None:
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


def get_subscriptions_deltas(db: Session, username: str, device_id: str = None):
    subscriptions = select(*ColumnFilters.subscription)
    if username is not None:
        subscriptions = subscriptions.where(
            schema.SubscriptionAction.username == username)
        if device_id is not None:
            subscriptions = subscriptions.where(
                schema.SubscriptionAction.device_id == device_id)
    return db.execute(subscriptions).all()


def add_subscription_deltas(
    db: Session, username: str, deviceid: str,
    deltas: models.SubscriptionDeltas, time: datetime
):
    with db.begin():
        shared_kwargs = {
            "username": username,
            "device_id": deviceid,
            "time": time
        }
        db.add_all(itertools.chain(
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


def get_subscriptions(db: Session, username: str, device_id: str = None):
    # SELECT SubscriptionAction.podcast_url FROM SubscriptionAction GROUP BY SubscriptionAction.podcast_url HAVING sum(SubscriptionAction.action)>0
    pass
