from datetime import datetime
from typing import Union

import bcrypt
from sqlalchemy.orm import Session

from core.models import Order, Payment
from crud.Payments import create_payment, payment_count
from crud.Products import get_product_price, get_product_name
from schema.Order import OrderUpdateReq, OrderReq

from utils.toss.client import TossPayClient

# 매개 변수가 없는 경우 샌드박스 모드로 동작
client = TossPayClient()


def get_order_user_by_order_id(db: Session, order_id):
    return db.query(Order).filter(Order.id == order_id).first().username


async def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


async def get_price(db: Session, product_list: OrderReq) -> int:
    orders = product_list.order_list

    price = 0
    for order in orders:
        price += order.quantity * get_product_price(db, order.product_id)

    return price


def order_list(
        db: Session,
        pay_id: int,
        limit: int = 10,
        page: int = 0,):

    orders = db.query(Order).filter(Order.payments_id == pay_id)

    cnt = 0 if orders is None else orders.count()
    orders = [] if orders is None else orders.limit(limit).offset(page * limit).all()

    orders = [order.__dict__ for order in orders]

    return {
        "cnt": cnt,
        "page": page,
        "limit": limit,
        "orders": orders
    }


def add_order(db:Session, username, orders):
    fst_product_name = get_product_name(db, orders[0]["product_id"])
    products_desc = f"{fst_product_name}"

    if len(orders) > 1:
        products_desc += f" 외 {len(orders) - 1}개 상품"

    # 결제 요청
    # result = client.purchase('주문번호', 1000, '상품설명', 'http://returning .url', False)
    # payment = client.get_payment(result.pay_token)
    # client.approve(payment.pay_token)

    payment = create_payment(
        db, username,
        bcrypt.hashpw(f"{username}{payment_count(db)}".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))


    try:
        for order in orders:
            new_order = Order(
                product_id=order["product_id"],
                quantity=order["quantity"],
                payments_id=payment.id,
            )
            db.add(new_order)
            db.commit()

        return {"message": "Order created successfully!"}
    except Exception as e:
        # 결제 취소
        # client.cancel(payment.pay_token)
        raise ValueError(f"Order creation failed: {e}")


def refund_order(db: Session, payment_id: int, user: str, refund_data: OrderUpdateReq,):
    old_order = db.query(Payment).filter(Payment.id == payment_id).first()

    if old_order is None:
        raise ValueError("Order not found!")

    db.query(Payment).filter(Payment.id == payment_id).update({
        "refund": user,
        "refund_reason": refund_data.refund_reason,
        "refund_timestamp": datetime.now()
    })

    db.commit()

    return {"message": "Order refunded successfully!"}
