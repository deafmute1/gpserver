from sqlalchemy import select, update
from . import schema, models
from typing import Any, NamedTuple
from const import hasher
from collections.abc import Sequence, Mapping

from sqlalchemy.orm import Session

# User


class ColumnFilters(NamedTuple):
    user: list[schema.User] = [schema.User.username]
    subscription: list[schema.SubscriptionAction] = [schema.SubscriptionAction.podcast_url]


def create_user(db: Session, user: models.UserCreate) -> schema.User:
    user = schema.User(
        username=user.username,
        password_hash=hasher.hash(user.password),
    )
    with db.begin():
        db.add(user)
    db.refresh(user)
    return user


def get_user(db: Session, username: str) -> schema.User:
    return db.get(schema.User, username)


def get_user_model(db: Session, username: str) -> models.User | None:
    return models.User(**db.execute(
        select(*ColumnFilters.user)
        .where(schema.User.username == username)
    ).one_or_none())


def get_all_user_models(db: Session) -> list[models.User]:
    return [models.User(**e) for e in
            db.execute(select(*ColumnFilters.user)).all()
            ]


def update_users(db: Session, users: Sequence[Mapping[str, Any]]):
    with db.begin():
        db.execute(
            update(schema.User),
            map(lambda user: user.__dict, users),
        )


def delete_user(db: Session, user: schema.User):
    with db.begin():
        db.delete(user)

# Session


def create_session(db: Session, session: models.SessionTokenTimestamp) -> schema.Session:
    session = schema.Session(
        key_hash=hasher.hash(session.key),
        username=session.username,
        created=session.created
    )
    with db.begin():
        db.add(session)
    db.refresh(session)


def get_session(db: Session, session: models.SessionToken) -> schema.Session:
    db.get(
        schema.Session,
        {"key_hash": hasher.hash(session.key), "username": session.username}
    )


def delete_session(db: Session, session: models.SessionToken):
    with db.begin():
        db.delete(get_session(db, session))

def get_subscriptions(db:Session,username:str,device_id:str=None):
    # return db.get(schema.Device,(username,device_id)).subscriptions
    subscriptions = select(*ColumnFilters.subscription)
    if username is not None:
        subscriptions = subscriptions.where(schema.SubscriptionAction.username == username)
        if device_id is not None:
            subscriptions = subscriptions.where(schema.SubscriptionAction.device_id == device_id)
    return db.execute(subscriptions)