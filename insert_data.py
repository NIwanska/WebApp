import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, orm
import os

if __name__ == "__main__":
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:{os.getenv('DB_PORT')}/app_db"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()

    product_monthly_reports = pd.read_csv("./csv_db/products_monthly_reports.csv")
    print(f"product_monthly_reports: {product_monthly_reports.head()}")

    res = product_monthly_reports.to_sql("product_monthly_reports", connection, if_exists="append", index=False)
    print(f"Affected {res} rows")
    connection.close()
