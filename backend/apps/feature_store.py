import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://walmart-redis-1:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def update_cardholder_features(
        cardholder_id: int,
        txn_success: bool,
        discount_applied: float):
    """
    Update rolling features for a cardholder after a transaction.
    """
    pipe = r.pipeline()
    pipe.hincrby(f"cardholder:{cardholder_id}:features", "txn_count", 1)
    if txn_success:
        pipe.hincrby(
            f"cardholder:{cardholder_id}:features",
            "success_count",
            1
        )
    pipe.hincrbyfloat(f"cardholder:{cardholder_id}:features",
                      "total_discount", discount_applied)
    pipe.execute()


def get_cardholder_features(cardholder_id: int):
    """
    Get the feature summary for a cardholder.
    """
    data = r.hgetall(f"cardholder:{cardholder_id}:features")
    # Return zeros if no data yet
    return {
        "txn_count": int(data.get("txn_count", 0)),
        "success_count": int(data.get("success_count", 0)),
        "total_discount": float(data.get("total_discount", 0.0))
    }


def update_shopper_features(
        shopper_id: int,
        order_value: float,
        shopper_rating: float):
    """
    Update rolling features for a shopper after a transaction.
    """
    pipe = r.pipeline()
    pipe.hincrby(f"shopper:{shopper_id}:features",
                 "txn_count", 1)
    pipe.hincrbyfloat(f"shopper:{shopper_id}:features",
                      "total_spend", order_value)
    pipe.hincrbyfloat(f"shopper:{shopper_id}:features",
                      "total_rating", shopper_rating)
    pipe.execute()


def get_shopper_features(shopper_id: int):
    data = r.hgetall(f"shopper:{shopper_id}:features")
    txn_count = int(data.get("txn_count", 0))
    total_spend = float(data.get("total_spend", 0.0))
    total_rating = float(data.get("total_rating", 0.0))
    avg_rating = total_rating / txn_count if txn_count > 0 else 0.0
    return {
        "txn_count": txn_count,
        "total_spend": total_spend,
        "avg_rating": avg_rating
    }
