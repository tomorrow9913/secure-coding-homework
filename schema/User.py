from pydantic import BaseModel


class UserInfoRes(BaseModel):
    id: int
    username: str
    role: str
    full_name: str
    address: str
    payment_info: int


class UserInfoUpdateReq(BaseModel):
    username: str
    password: str
    role: str
    full_name: str
    address: str
    payment_info: int
