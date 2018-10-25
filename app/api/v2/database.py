import psycopg2
import os

db_url = os.getenv('DATABASE_URL')


def connection(db_url):
    """Get database connection"""
    con = psycopg2.connect(db_url)
    return con


def init_db():
    """Get database connection"""
    con = connection(db_url)
    return con


def create_tables():
    """Create tables and commit"""
    conn = connection(db_url)
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    conn.commit()


def delete_tables():
    """Delete tables"""

    conn = connection(db_url)
    curr = conn.cursor()

    table_1 = """DROP TABLE IF EXISTS users CASCADE"""
    table_2 = """DROP TABLE IF EXISTS sales CASCADE"""
    table_3 = """DROP TABLE IF EXISTS products CASCADE"""

    # Add all tables to the queries list
    queries = [table_1, table_2, table_3]

    for query in queries:
        curr.execute(query)
    conn.commit()


def tables():
    """Create tables"""
    table_1 = """CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY NOT NULL,
            name VARCHAR (100) NOT NULL,
            email VARCHAR (80) UNIQUE NOT NULL,
            phone numeric (12) UNIQUE NOT NULL,
            role VARCHAR (20) UNIQUE NOT NULL,
            password VARCHAR (20) NOT NULL
    )"""

    table_2 = """CREATE TABLE IF NOT EXISTS sales (
            id serial PRIMARY KEY NOT NULL,
            number_of_items_sold numeric (3) NOT NULL,
            transaction_amount numeric (6) NOT NULL,
            date_created TIMESTAMP with time zone DEFAULT('now'::text)::date NOT NULL,
            user_id INTEGER REFERENCES users(id)
    )"""

    table_3 = """CREATE TABLE IF NOT EXISTS products (
            id serial PRIMARY KEY NOT NULL,
            name VARCHAR (150) UNIQUE NOT NULL,
            category VARCHAR (80) NOT NULL,
            quantity numeric (4) NOT NULL,
            minimum_inventory_quantity numeric (4) NOT NULL,
            price numeric (6) NOT NULL,
            sale_id INTEGER REFERENCES sales(id)
    )"""

    # Add all tables to the queries list
    queries = [table_1, table_2, table_3]
    return queries
