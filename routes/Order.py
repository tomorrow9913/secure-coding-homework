from datetime import datetime

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud.Order as OrderCRUD
import crud.Payments as PayCRUD
from core.database import get_db
from crud.Products import get_product_name
from schema.Order import OrderReq, OrderUpdateReq
from utils.oauth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Order"]
)


# Create
@router.post("/")
async def add_new_order(
        order: OrderReq,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    order_list = [{"product_id": order.product_id, "quantity": order.quantity} for order in order.order_list]

    if len(order_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No order list!"
        )

    return OrderCRUD.add_order(db, current_user.username, order_list)


# Read
@router.get("/{pay_id}")
async def read_order_by_id(
        pay_id: int,
        limit: int = 10,
        page: int = 0,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin' and current_user.username != PayCRUD.get_payment_by_id(db, pay_id).username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return PayCRUD.get_payment_by_id(db, pay_id, limit, page)


@router.get("/")
async def read_all_payments(
        limit: int = 10,
        page: int = 0,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return PayCRUD.get_payment_list(db, limit, page)


@router.get("/usr/{username}")
async def read_pay_list_by_user(
        username: str,
        limit: int = 10,
        page: int = 0,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin' and current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return PayCRUD.get_payment_list(db, limit, page, username)


# Update
@router.put("/{payments_id}")
async def refund_order(
        payments_id: int,
        refund_req: OrderUpdateReq,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):

    if (current_user.role != 'admin'
            and current_user.username != PayCRUD.get_payment_by_id(db, payments_id).username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return OrderCRUD.refund_order(db, payments_id, current_user.username, refund_req)
