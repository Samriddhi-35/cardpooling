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


def compute_shopper_features(df):
    shopper_group = df.groupby('shopper_id')
    shopper_features = pd.DataFrame({
        'shopper_id': shopper_group.size().index,
        'txn_count': shopper_group.size().values,
        'total_spend': shopper_group['order_value'].sum().values,
        'avg_order_value': shopper_group['order_value'].mean().values,
        'unique_merchants': shopper_group['merchant'].nunique().values,
        'avg_rating': shopper_group['shopper_rating'].mean().values
    })
    return shopper_features


def compute_cardholder_features(df):
    cardholder_group = df.groupby('cardholder_id')
    cardholder_features = pd.DataFrame({
        'cardholder_id': cardholder_group.size().index,
        'txn_count': cardholder_group.size().values,
        'avg_discount': cardholder_group['discount_applied'].mean().values,
        'success_rate': (
            cardholder_group['txn_success'].sum() / cardholder_group.size()
        ).values,
        'avg_rating': cardholder_group['shopper_rating'].mean().values
    })
    return cardholder_features


def main():
    df = extract_transactions()
    print(f"Extracted {len(df)} transactions.")

    os.makedirs("etl/outputs", exist_ok=True)
    df.to_csv("etl/outputs/raw_transactions.csv", index=False)
    print("Saved raw transactions to etl/outputs/raw_transactions.csv")

    # Compute shopper features
    # and save them to the output directory
    shopper_features = compute_shopper_features(df)
    shopper_features.to_csv("etl/outputs/shopper_features.csv", index=False)
    print("Saved shopper features to etl/outputs/shopper_features.csv")

    # Compute and save cardholder features
    cardholder_features = compute_cardholder_features(df)
    cardholder_features.to_csv(
        "etl/outputs/cardholder_features.csv",
        index=False)
    print("Saved cardholder features to etl/outputs/cardholder_features.csv")


if __name__ == "__main__":
    main()
