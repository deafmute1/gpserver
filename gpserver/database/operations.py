from . import schema, models

from passlib.hash import bcrypt
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import delete


# User
def create_user(db: Session, user: models.UserCreate) -> schema.User:
    user = schema.User(
        username=user.username.encode('utf8'),
        password_hash=bcrypt(user.password),
    )
    with db.begin():
        db.add(user)
    db.refresh(user)
    return user

def get_user(db:Session, username:str) -> schema.User:
    return db.get(schema.User,username)

def remove_user(db:Session, username:str):
    with db.begin():    
        db.delete(get_user(username))

# Session
def set_session(db:Session, session: models.SessionTokenTimestamp) -> schema.Session:
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
        schema.Session, { "key": session.key, "username": session.username }
    )
    
def delete_session(db: Session, session: models.SessionToken):
    with db.begin(): 
        db.delete(get_session(session))