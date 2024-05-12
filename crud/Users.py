from sqlalchemy.orm import Session

from core.models import User
from crud.Order import order_list


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_list(db: Session, limit: int, page: int) -> dict:
    users = db.query(User)
    cnt = users.count()

    users = users.limit(limit).offset(page * limit).all()
    users = [user.__dict__ for user in users]
    for user in users:
        user.pop('password')
    return {
        "cnt": cnt,
        "page": page,
        "limit": limit,
        "users": users
    }


def get_user_info_with_order(
        db: Session,
        username: str,
        limit: int = 10,
        page: int = 0
        ) -> dict:
    user = get_user_by_username(db, username)
    user = user.__dict__
    user.pop('password')
    order = order_list(db, limit, page, username)

    return {
        "user_info": user,
        "order_list": order
    }


def update_user_info(
        db: Session,
        username: str,
        role: str,
        full_name: str,
        address: str) -> dict:

    current_user = get_user_by_username(db, username)

    if current_user is None:
        raise ValueError("User not found!")

    db.query(User).filter(current_user.username == username).update({
        "role": role,
        "full_name": full_name,
        "address": address,
    })
    db.commit()

    return {"message": "User information updated successfully!"}


def delete_user(db: Session, username: str) -> dict:
    user = get_user_by_username(db, username)

    if user is None:
        raise ValueError("User not found!")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully!"}