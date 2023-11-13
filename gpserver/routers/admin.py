from typing import Annotated

from pydantic import BaseModel
from .. import dependencies
from database import models, operations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["admin"]
) 

class UserList(BaseModel): 
    __root__ = list[models.User] | dict[str: None]

class UserCreateList(BaseModel):
    __root__ = list[models.UserCreate] 

@router.post("/users/create")
def create_users(
    users: UserCreateList,
    db: Session = Depends(dependencies.get_db),
): 
    for user in users: 
        if operations.get_user_model(db, user.name) is not None: 
            raise HTTPException(409, f"User with username {user.name} already exists")
        operations.create_user(db, user)

@router.post(
    "/users/modify", 
    summary="Merges (with priority) provided user data with existing user data matching username"
)
def modify_user(
    users: UserList,
    db: Session = Depends(dependencies.get_db)
):
    operations.update_users(db, users.__root__)

@router.post("/users/delete")
def delete_user(
    usernames: Annotated[[list[str]], Query()],
    db: Session = Depends(dependencies.get_db)
):
    for name in usernames: 
        user = operations.get_user(db, name)
        if user is None: 
            raise HTTPException(409, f"User {name} does not exist")
        operations.delete_user(user)

@router.get("/users", response_model=UserList)
def get_users(   
    usernames: Annotated[[list[str]], Query()],
    db: Session = Depends(dependencies.get_db)
):
    return {
        [operations.get_user_filtered(db, n) for n in usernames]
    }

@router.get("/users/all", response_model=UserList)
def get_all_users(
    db: Session = Depends(dependencies.get_db)
):
    return {
        [models.User(**dict(e)) for e in operations.get_all_users_filtered(db)]
    }