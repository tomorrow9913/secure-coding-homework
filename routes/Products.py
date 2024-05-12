from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from core.database import get_db
import crud.Products as ProductsCRUD
from schema.Product import Product
from utils.oauth import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Create
@router.post("/")
async def add_new_product(
        name: str,
        category: str,
        price: float,
        thumbnail_url: str,
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return ProductsCRUD.add_product(db, name, category, price, thumbnail_url)


# Read
@router.get("/")
async def get_products_all(limit: int = 10, page: int = 0, db: Session = Depends(get_db)):
    return ProductsCRUD.get_all_products(db, page, limit)


@router.get("/{product_id}")
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return ProductsCRUD.get_product_by_id(db, product_id)


# Update
@router.put("/{product_id}")
async def update_product(
        product_id: int,
        name: str,
        category: str,
        price: float,
        thumbnail_url: str,
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )

    return ProductsCRUD.update_product(db, product_id, name, category, price, thumbnail_url)


# Delete
@router.delete("/{product_id}")
async def delete_product(product_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized!"
        )
    return ProductsCRUD.delete_product(db, product_id)
