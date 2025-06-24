import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
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