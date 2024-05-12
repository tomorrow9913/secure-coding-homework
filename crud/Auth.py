from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from core.models import User
from core.oauthConfig import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from crud.Users import get_user_by_username

from jose import jwt
from utils.passHash import hash_password, check_password
from schema.Auth import Token


def add_user(
        db: Session,
        username: str,
        password: str,
        full_name: str,
        role: str = "user",
        address: Optional[str] = None,
        payment_info: Optional[str] = None) -> dict:
    if get_user_by_username(db, username) is not None:
        return {"message": "User already exists!"}

    new_user = User(
        username=username,
        password=hash_password(password),
        role=role,
        full_name=full_name,
        address=address,
        payment_info=payment_info
    )

    db.add(new_user)
    db.commit()

    user = {
        "username": username,
        "role": role,
        "full_name": full_name,
        "address": address,
        "payment_info": payment_info
    }

    return {"message": "User created successfully!", "user": user}


def register_admin(db: Session,
                   username: str,
                   password: str,
                   full_name: str) -> dict:
    return add_user(db, username, password, 'admin', full_name, None, None)


def authenticate_user(db: Session, username: str, password: str) -> Token:
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if check_password(password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return Token(access_token=access_token, token_type="bearer", username=user.username, role=user.role)
