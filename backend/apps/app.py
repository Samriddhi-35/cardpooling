from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.apps.models import Shopper, Cardholder, Transaction
from backend.apps.db import SessionLocal
from datetime import datetime

app = FastAPI()

# Schemas


class ShopperCreate(BaseModel):
    location: str
    order_category: str
    merchant: str


class CardholderCreate(BaseModel):
    card_type: str
    bank: str
    avg_response_time: float
    availability: bool
    rating_avg: float
    discount_rate: float


class TransactionLog(BaseModel):
    shopper_id: int
    cardholder_id: int
    merchant: str
    category: str
    order_value: float
    accepted_within_10s: bool
    discount_applied: float
    shopper_rating: float
    txn_success: bool


@app.post("/add_shopper")
def add_shopper(shopper: ShopperCreate):
    db = SessionLocal()
    try:
        shopper_obj = Shopper(
            location=shopper.location,
            order_category=shopper.order_category,
            merchant=shopper.merchant,
            created_at=datetime.utcnow()
        )
        db.add(shopper_obj)
        db.commit()
        db.refresh(shopper_obj)
        return {"shopper_id": shopper_obj.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.post("/add_cardholder")
def add_cardholder(cardholder: CardholderCreate):
    db = SessionLocal()
    try:
        cardholder_obj = Cardholder(
            card_type=cardholder.card_type,
            bank=cardholder.bank,
            avg_response_time=cardholder.avg_response_time,
            availability=cardholder.availability,
            rating_avg=cardholder.rating_avg,
            discount_rate=cardholder.discount_rate,
            created_at=datetime.utcnow()
        )
        db.add(cardholder_obj)
        db.commit()
        db.refresh(cardholder_obj)
        return {"cardholder_id": cardholder_obj.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.post("/log_transaction")
def log_transaction(txn: TransactionLog):
    db = SessionLocal()
    try:
        transaction = Transaction(
            shopper_id=txn.shopper_id,
            cardholder_id=txn.cardholder_id,
            merchant=txn.merchant,
            category=txn.category,
            order_value=txn.order_value,
            accepted_within_10s=txn.accepted_within_10s,
            discount_applied=txn.discount_applied,
            shopper_rating=txn.shopper_rating,
            txn_success=txn.txn_success,
            created_at=datetime.utcnow(),
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return {"status": "success", "transaction_id": transaction.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()