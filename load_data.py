
# load_data.py

import pandas as pd
import mysql.connector
from mysql.connector import Error

# ==========================================================
# MYSQL CONFIGURATION
# ==========================================================

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Root@123",  # Change as needed
}

DATABASE_NAME = "retail_ai_agent"


# ==========================================================
# CREATE DATABASE
# ==========================================================

def create_database():
    conn = mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"]
    )

    cursor = conn.cursor()

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"
    )

    cursor.close()
    conn.close()

    print(f"Database '{DATABASE_NAME}' ready.")


# ==========================================================
# CONNECT DATABASE
# ==========================================================

def get_connection():

    return mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=DATABASE_NAME
    )


# ==========================================================
# CREATE TABLES
# ==========================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Customers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(20) PRIMARY KEY,
        customer_segment VARCHAR(50),
        signup_date DATE,
        preferred_channel VARCHAR(50),
        city VARCHAR(100)
    )
    """)

    # Products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR(20) PRIMARY KEY,
        product_name VARCHAR(100),
        category VARCHAR(100),
        sub_category VARCHAR(100),
        base_price DECIMAL(10,2)
    )
    """)

    # Stores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        store_id VARCHAR(20) PRIMARY KEY,
        store_name VARCHAR(100),
        region VARCHAR(50),
        city VARCHAR(100),
        store_type VARCHAR(50)
    )
    """)

    # Sales Transactions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_transactions (
        order_id VARCHAR(20) PRIMARY KEY,
        order_date DATE,

        store_id VARCHAR(20),
        product_id VARCHAR(20),
        customer_id VARCHAR(20),

        sales_channel VARCHAR(50),

        units_sold INT,
        unit_price DECIMAL(10,2),
        discount_pct DECIMAL(5,2),

        payment_status VARCHAR(50),
        delivery_status VARCHAR(50),

        FOREIGN KEY (store_id)
            REFERENCES stores(store_id),

        FOREIGN KEY (product_id)
            REFERENCES products(product_id),

        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    )
    """)

    # Returns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS returns (
        return_id VARCHAR(20) PRIMARY KEY,
        order_id VARCHAR(20),
        return_date DATE,
        return_reason VARCHAR(100),

        FOREIGN KEY (order_id)
            REFERENCES sales_transactions(order_id)
    )
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print("Tables created successfully.")


# ==========================================================
# LOAD CSV TO MYSQL
# ==========================================================

def load_csv_to_table(csv_path, table_name, date_columns=None):

    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_csv(csv_path)

    if date_columns:
        for col in date_columns:
            df[col] = pd.to_datetime(
                df[col],
                dayfirst=True,
                errors="coerce"
            )

    columns = ",".join(df.columns)

    placeholders = ",".join(
        ["%s"] * len(df.columns)
    )

    insert_query = f"""
    INSERT INTO {table_name}
    ({columns})
    VALUES ({placeholders})
    """

    data = [
        tuple(
            None if pd.isna(x) else x
            for x in row
        )
        for row in df.itertuples(index=False, name=None)
    ]

    cursor.executemany(insert_query, data)

    conn.commit()

    print(
        f"Loaded {len(df)} rows into '{table_name}'"
    )

    cursor.close()
    conn.close()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    create_database()
    create_tables()

    load_csv_to_table(
        "data/customers.csv",
        "customers",
        ["signup_date"]
    )

    load_csv_to_table(
        "data/products.csv",
        "products"
    )

    load_csv_to_table(
        "data/stores.csv",
        "stores"
    )

    load_csv_to_table(
        "data/sales_transactions.csv",
        "sales_transactions",
        ["order_date"]
    )

    load_csv_to_table(
        "data/returns.csv",
        "returns",
        ["return_date"]
    )

    print("\nData loading completed successfully.")
