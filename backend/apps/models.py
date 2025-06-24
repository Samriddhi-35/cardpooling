from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Shopper(Base):
    __tablename__ = 'shoppers'
    id = Column(Integer, primary_key=True)
    location = Column(String)
    order_category = Column(String)
    merchant = Column(String)
    created_at = Column(DateTime)


class Cardholder(Base):
    __tablename__ = 'cardholders'
    id = Column(Integer, primary_key=True)
    card_type = Column(String)
    bank = Column(String)
    avg_response_time = Column(Float)
    availability = Column(Boolean)
    rating_avg = Column(Float)
    discount_rate = Column(Float)
    created_at = Column(DateTime)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    shopper_id = Column(Integer, ForeignKey('shoppers.id'))
    cardholder_id = Column(Integer, ForeignKey('cardholders.id'))
    merchant = Column(String)
    category = Column(String)
    order_value = Column(Float)
    accepted_within_10s = Column(Boolean)
    discount_applied = Column(Float)
    shopper_rating = Column(Float)
    txn_success = Column(Boolean)
    created_at = Column(DateTime)
