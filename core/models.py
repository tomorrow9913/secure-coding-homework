from sqlalchemy import Column, Float, ForeignKey, Integer, TIMESTAMP, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    pay_token = Column(Text, nullable=False)
    payments_time = Column(TIMESTAMP, nullable=False)
    refund_reason = Column(Text)
    refund_timestamp = Column(TIMESTAMP)
    refund = Column(Text)
    username = Column(Integer)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    category = Column(Text)
    price = Column(Float)
    thumbnail_url = Column(Text)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    password = Column(Text)
    role = Column(Text)
    full_name = Column(Text)
    address = Column(Text)
    payment_info = Column(Text)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'))
    quantity = Column(Integer)
    payments_id = Column(ForeignKey('payments.id'))

    payments = relationship('Payment')
    product = relationship('Product')
