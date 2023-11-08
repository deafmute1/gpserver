from . import schema, models
from .connection import engine
from passlib.hash import bcrypt

from sqlalchemy.orm import Session


def create_user(db: Session, user: models.UserCreate):
    user = schema.User(
        username=user.username,
        password_hash=bcrypt(user.password),
    )
    with db.begin():
        db.add(user)
    db.refresh(user)
    return user

def get_user(db:Session, username:str):
    return db.get(schema.User,username)

def remove_user(db:Session,username:str):
    with db.begin():    
        db.delete(username)
        

