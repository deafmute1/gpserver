from typing import Annotated

from pydantic import BaseModel, RootModel

from gpserver.routers import models
from .. import dependencies
from ..database import operations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["admin"]
)

class UserList(BaseModel): 
    users: list[models.User]
class UserCreateList(BaseModel): 
    users: list[models.UserCreate]

@router.post("/users/create/")
def create_users(
    users: UserCreateList,
    db: Session = Depends(dependencies.get_db),
):
    existing = []
    with db.begin():
        for user in users.users:
            if operations.get_user(db, user.username) is None:
                operations.create_user(db, user)
            else:
                existing.append(user.username)
    if existing:
        raise HTTPException(409, f"Users already exist: {existing}")


@router.post(
    "/users/modify",
    summary="Merges (with priority) provided user data with existing user data matching username"
)
def modify_user(
    users: UserList,
    db: Session = Depends(dependencies.get_db)
):
    raise HTTPException(501)
    #set this up once some other modify endpoint exists as a template - users have a bit of weirdness & it would be nice to have a more standard modify endpoint to crib from
    #what format will modifications be sent in? partial models with only the attributes to modify actually set? dicts in format {columnname:newvalue, ...}? 
    with db.begin():
        for user in users:
            operations.update_user(db,user.username,)


@router.post("/users/delete")
def delete_user(
    username: Annotated[list[str], Query()],
    db: Session = Depends(dependencies.get_db)
):
    nonexisting = []
    with db.begin():
        for name in username:
            if (user := operations.get_user(db, name)) is None:
                nonexisting.append(name)
            else:
                operations.delete_user(db, user)
    if nonexisting:
        raise HTTPException(409, f"Users {nonexisting} do not exist")


@router.get("/users", response_model=UserList)
def get_users(
    username: Annotated[list[str], Query()],
    db: Session = Depends(dependencies.get_db)
):
    return [operations.get_user_filtered(db, n) for n in username]


@router.get("/users/all", response_model=UserList)
def get_all_users(
    db: Session = Depends(dependencies.get_db)
):
    return operations.get_all_users_filtered(db)
