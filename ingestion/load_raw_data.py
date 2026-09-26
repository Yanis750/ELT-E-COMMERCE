import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine("postgresql://dataeng:dataeng@localhost:5432/ecommerce")

RAW_DIR = "../data/raw"
files = {
    "raw_orders": "olist_orders_dataset.csv",
    "raw_order_items": "olist_order_items_dataset.csv",
    "raw_payments": "olist_order_payments_dataset.csv",
    "raw_reviews": "olist_order_reviews_dataset.csv",
    "raw_customers": "olist_customers_dataset.csv",
    "raw_products": "olist_products_dataset.csv",
    "raw_sellers": "olist_sellers_dataset.csv",
    "raw_geolocation": "olist_geolocation_dataset.csv",
    "raw_category_translation": "product_category_name_translation.csv",
}

for table_name, filename in files.items():
    path = os.path.join(RAW_DIR, filename)
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists="replace", index=False, schema="public")
    print(f"✅ {table_name} chargée ({len(df)} lignes)")