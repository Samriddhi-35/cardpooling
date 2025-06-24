"""
ETL script to extract raw logs and prepare for feature engineering.
Milestone 3: Batch feature pipeline scaffolding.
"""

import pandas as pd
import sqlalchemy
import os

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:admin@localhost:5432/cardpooling"
)


def extract_transactions():
    """
    Extract raw transactions from PostgreSQL.
    """
    engine = sqlalchemy.create_engine(DB_URL)
    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, engine)
    return df


def main():
    df = extract_transactions()
    print(f"Extracted {len(df)} transactions.")
    # Save as CSV for initial check
    os.makedirs("etl/outputs", exist_ok=True)
    df.to_csv("etl/outputs/raw_transactions.csv", index=False)
    print("Saved raw transactions to etl/outputs/raw_transactions.csv")


if __name__ == "__main__":
    main()
