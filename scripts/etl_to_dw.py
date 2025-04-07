import pandas as pd
import sqlite3
import pathlib
import sys

# Add project root to path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import logger
from utils.logger import logger

# Paths
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        CustomerID INTEGER PRIMARY KEY,
        Name TEXT,
        Region TEXT,
        JoinDate TEXT,
        LoyaltyPoints INTEGER,
        CustomerSegments TEXT
    );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            productid INTEGER PRIMARY KEY,
            productname TEXT,
            category TEXT,
            unitprice REAL, 
            stockquantity INTEGER,
            supplier TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            SaleID INTEGER PRIMARY KEY,
            CustomerID INTEGER,
            ProductID INTEGER,
            SaleAmount REAL,
            SaleDate TEXT,
            StoreID INTEGER,
            CampaignId INTEGER,
            DiscountPercentage INTEGER,
            PaymentType TEXT,
            FOREIGN KEY (CustomerID) REFERENCES customer (CustomerID),
            FOREIGN KEY (productid) REFERENCES product (productid)
        );
    """)
    logger.info("Schema created.")
def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_prepared.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()