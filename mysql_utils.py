
# mysql_utils.py

import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Root@123",      # Change if needed
    "database": "retail_ai_agent"
}


# ==========================================================
# CONNECTION
# ==========================================================

def get_connection():
    """
    Create and return MySQL connection.
    """

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Database Connection Error: {e}")

    return None


# ==========================================================
# EXECUTE SELECT QUERY
# ==========================================================

def run_select_query(query: str) -> pd.DataFrame:
    """
    Execute SELECT query and return results
    as Pandas DataFrame.
    """

    connection = get_connection()

    if connection is None:
        raise Exception("Unable to connect to database")

    try:
        df = pd.read_sql(query, connection)

        

        return df

    except Exception as e:

        raise Exception(
            f"Error executing query:\n{e}"
        )

    finally:

        connection.close()


# ==========================================================
# EXECUTE NON-SELECT QUERY
# ==========================================================

def run_query(query: str):
    """
    Execute INSERT/UPDATE/DELETE query.
    """

    connection = get_connection()

    if connection is None:
        raise Exception("Unable to connect to database")

    cursor = connection.cursor()

    try:

        cursor.execute(query)

        connection.commit()

        return {
            "status": "success",
            "rows_affected": cursor.rowcount
        }

    except Exception as e:

        connection.rollback()

        raise Exception(
            f"Query Execution Error:\n{e}"
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# GET TABLES
# ==========================================================

def get_tables():
    """
    Returns list of tables in database.
    """

    query = """
    SHOW TABLES
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query)

    tables = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    connection.close()

    return tables


# ==========================================================
# GET TABLE SCHEMA
# ==========================================================

def get_table_schema(table_name: str):
    """
    Returns schema for a table.
    """

    query = f"""
    DESCRIBE {table_name}
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query)

    schema = cursor.fetchall()

    cursor.close()
    connection.close()

    return schema


# ==========================================================
# DATABASE SCHEMA TEXT
# ==========================================================

def get_schema_text():
    """
    Returns schema information in text format
    for LLM prompts.
    """

    tables = get_tables()

    schema_text = ""

    for table in tables:

        schema_text += f"\nTable: {table}\n"

        columns = get_table_schema(table)

        for col in columns:

            schema_text += (
                f"- {col[0]} ({col[1]})\n"
            )

    return schema_text


# ==========================================================
# QUERY VALIDATION
# ==========================================================

def is_safe_query(query: str):
    """
    Allow only SELECT queries.
    """

    query = query.strip().lower()

    blocked_keywords = [
        "delete",
        "drop",
        "truncate",
        "alter",
        "update",
        "insert",
        "create"
    ]

    for keyword in blocked_keywords:

        if keyword in query:
            return False

    return query.startswith("select")


# ==========================================================
# EXECUTE AGENT QUERY
# ==========================================================

def execute_agent_query(query: str):
    """
    Validates query before execution.
    Used by SQL Agent.
    """

    if not is_safe_query(query):

        raise Exception(
            "Unsafe SQL detected. Only SELECT queries are allowed."
        )

    return run_select_query(query)


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    print("Available Tables")
    print("-" * 50)

    print(get_tables())

    print("\nSchema")
    print("-" * 50)

    print(get_schema_text())

    print("\nSample Query")
    print("-" * 50)

    sample_query = """
    SELECT *
    FROM customers
    LIMIT 5
    """

    result = execute_agent_query(sample_query)

    print(result)

