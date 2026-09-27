import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect, text

# Host configurable : "localhost" par defaut (execution locale),
# "postgres" quand le script tourne dans un conteneur Docker (Airflow).
DB_HOST = os.environ.get("DB_HOST", "localhost")

engine = create_engine(f"postgresql://dataeng:dataeng@{DB_HOST}:5432/ecommerce")
inspector = inspect(engine)

# Chemin absolu, calcule a partir de l'emplacement du script lui-meme.
SCRIPT_DIR = Path(__file__).resolve().parent
RAW_DIR = SCRIPT_DIR.parent / "data" / "raw"

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
    path = RAW_DIR / filename
    df = pd.read_csv(path)

    if inspector.has_table(table_name, schema="public"):
        # La table existe deja (et peut-etre des vues dbt en dependent) :
        # on vide son contenu sans toucher a sa structure, plutot que de la supprimer.
        with engine.begin() as conn:
            conn.execute(text(f'TRUNCATE TABLE public."{table_name}"'))
        df.to_sql(table_name, engine, if_exists="append", index=False, schema="public")
    else:
        # Premiere execution : la table n'existe pas encore, on la cree normalement.
        df.to_sql(table_name, engine, if_exists="replace", index=False, schema="public")

    print(f"OK {table_name} chargee ({len(df)} lignes)")
