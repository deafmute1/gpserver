from dataclasses import dataclass
from sqlalchemy import select
from . import schema, models
from typing import NamedTuple
from const import hasher

from sqlalchemy.orm import Session, defer

# User


class ColumnFilters(NamedTuple):
    user: list[schema.User] = [schema.User.username]


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


def delete_user(db: Session, user: schema.User):
    with db.begin():
        db.delete(user)

# Session


def create_session(db: Session, session: models.SessionTokenTimestamp) -> schema.Session:
    session: schema.Session(
        key=session.key,
        username=session.username,
        created=session.created
    )
    with db.begin():
        db.add(session)
    db.refresh()


def get_session(db: Session, session: models.SessionToken) -> schema.Session:
    db.get(
        schema.Session, {"key": session.key, "username": session.username}
    )


def delete_session(db: Session, session: models.SessionToken):
    with db.begin():
        db.delete(get_session(db, session))
