from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    thumbnail_url: str
    