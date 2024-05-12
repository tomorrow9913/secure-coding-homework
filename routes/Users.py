from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud.Users as UsersCRUD
from core.database import get_db
from core.models import User
from schema.User import UserInfoUpdateReq
from utils.oauth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create is in Auth.py

# Read
@router.get("/me")
async def read_users_me(
        limit: int = 10,
        page: int = 0,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    return UsersCRUD.get_user_info_with_order(db, current_user.username, limit, page)


@router.get("/{username}")
async def read_user_by_username(
        username: str,
        limit: int = 10,
        page: int = 0,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):

    if current_user.role != 'admin' and current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return UsersCRUD.get_user_info_with_order(db, username, limit, page)


@router.get("/")
async def read_all_users(limit: int = 10, page: int = 0, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return UsersCRUD.get_user_list(db, limit, page)


# Update
@router.put("/update")
async def update_user_info_endpoint(
        update_info: UserInfoUpdateReq,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin' and current_user.username != update_info.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    if current_user.role != 'admin' and current_user.role != update_info.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return UsersCRUD.update_user_info(db, **update_info.dict())


# Delete
@router.delete("/{username}")
async def delete_user_endpoint(
        username: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin' or current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return UsersCRUD.delete_user(db, username)
