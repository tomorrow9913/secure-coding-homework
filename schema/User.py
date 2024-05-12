from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str
    role: str
    full_name: str
    address: str
    payment_info: str

