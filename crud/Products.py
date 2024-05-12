from sqlalchemy.orm import Session

from core.models import Product


def get_product_price(db: Session, product_id: int) -> float:
    product = db.query(Product).filter(Product.id == product_id).first()
    return product.price


def get_product_name(db, product_id):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise ValueError("Product not found!")

    return product.name


# Create
def add_product(db: Session, name: str, category: str, price: float, thumbnail_url: str):
    product = Product(name=name, category=category, price=price, thumbnail_url=thumbnail_url)
    db.add(product)
    db.commit()
    return {"message": "Product add successfully"}


# Read
def get_all_products(db: Session, page: int, limit: int):
    product = db.query(Product)
    cnt = product.count()

    product = product.limit(limit).offset(page * limit).all()
    product = [p.__dict__ for p in product]

    return {
        "cnt": cnt,
        "page": page,
        "limit": limit,
        "products": product
    }


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


# Update
def update_product(db: Session, product_id, name, category, price, thumbnail_url):
    product = get_product_by_id(db, product_id)

    if product is None:
        return {"message": "Product not found!"}

    db.query(Product).filter(Product.id == product_id).update({
        "name": name,
        "category": category,
        "price": price,
        "thumbnail_url": thumbnail_url
    })
    db.commit()

    return {"message": "Product updated successfully"}


# Delete
def delete_product(db: Session, product_id):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise ValueError("Product not found!")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully!"}


