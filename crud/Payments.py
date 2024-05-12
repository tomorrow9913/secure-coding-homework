from datetime import datetime
from typing import Union

from sqlalchemy.orm import Session

from core.models import Payment
import crud.Order as OrderCRUD


def create_payment(db: Session, username: str, pay_token: str) -> Payment:
    now = datetime.now()
    payment = Payment(
        username=username,
        pay_token=pay_token,
        payments_time=now
    )
    db.add(payment)
    db.commit()

    return db.query(Payment).filter(Payment.pay_token == pay_token).first()


def payment_count(db: Session) -> int:
    return db.query(Payment).count()


def get_payment_by_id(db: Session, pay_id: id, limit: int = 10, page: int = 0):
    pay_info = db.query(Payment).filter(Payment.id == pay_id).first()
    orders = OrderCRUD.order_list(db, pay_info.id, limit, page)

    pay_info = pay_info.__dict__
    pay_info["orders"] = orders
    return pay_info


def get_payment_list(
        db: Session,
        limit: int = 10,
        page: int = 0,
        user_name: Union[str, None] = None):

    if user_name is None:
        pays = db.query(Payment)
    else:
        pays = db.query(Payment).filter(Payment.username == user_name)

    cnt = 0 if pays is None else pays.count()
    pays = [] if pays is None else pays.limit(limit).offset(page * limit).all()

    pays = [pay.__dict__ for pay in pays]

    return {
        "cnt": cnt,
        "page": page,
        "limit": limit,
        "payments": pays
    }
