"""
ETL script to extract raw logs and generate engineered features.
Milestone 3: Batch feature pipeline - basic feature computation.
"""

import pandas as pd
import sqlalchemy
import os

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:admin@localhost:5432/cardpooling"
)


def extract_transactions():
    engine = sqlalchemy.create_engine(DB_URL)
    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, engine)
    return df


def shopper_features(transactions: pd.DataFrame) -> pd.DataFrame:
    # Example features: transaction count, total spend, average rating
    grouped = transactions.groupby("shopper_id").agg(
        txn_count=("id", "count"),
        total_spend=("order_value", "sum"),
        avg_rating=("shopper_rating", "mean"),
    ).reset_index()
    return grouped


def cardholder_features(transactions: pd.DataFrame) -> pd.DataFrame:
    # Example features: transaction count, average response time,
    # success rate, average discount
    grouped = transactions.groupby("cardholder_id").agg(
        txn_count=("id", "count"),
        avg_response_time=("accepted_within_10s", "mean"),
        success_rate=("txn_success", "mean"),
        avg_discount=("discount_applied", "mean")
    ).reset_index()
    return grouped


def main():
    os.makedirs("etl/outputs", exist_ok=True)
    df = extract_transactions()
    print(f"Extracted {len(df)} transactions.")

    # Save raw
    df.to_csv("etl/outputs/raw_transactions.csv", index=False)

    # Shopper features
    shopper_df = shopper_features(df)
    shopper_df.to_csv("etl/outputs/shopper_features.csv", index=False)
    print("Saved shopper features to etl/outputs/shopper_features.csv")

    # Cardholder features
    cardholder_df = cardholder_features(df)
    cardholder_df.to_csv("etl/outputs/cardholder_features.csv", index=False)
    print("Saved cardholder features to etl/outputs/cardholder_features.csv")


if __name__ == "__main__":
    main()
