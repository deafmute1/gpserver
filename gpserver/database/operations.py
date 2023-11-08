from . import schema, models
from .connection import engine

from sqlalchemy.orm import Session


def create_user(db: Session, user: models.UserCreate):
    item = schema.User(username=user.username,
                          password_hash=user.password_hash,
                          password_salt=user.password_salt)
    with db.begin():
        db.add(item)
    db.refresh(item)
    return item

def get_user(db:Session,username:str):
    return db.get(schema.User,username)

def remove_user(db:Session,username:str):
    with db.begin():    
        db.delete(username)
        

