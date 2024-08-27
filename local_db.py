
import os
import sqlite3

def create_tables_db():
  
  sql_statements = [ 
    """
      CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        sku TEXT UNIQUE NOT NULL, 
        stock INTEGER,
        price TEXT
      );
    """,
    """
      CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT UNIQUE NOT NULL,
        total TEXT NOT NULL
      );
    """,
    """
      CREATE TABLE IF NOT EXISTS products_orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        quantity INT NOT NULL,
        sub_total TEXT NOT NULL,
        orders_id INTEGER NOT NULL,
        products_id INTEGER NOT NULL,
        FOREIGN KEY (orders_id) REFERENCES orders (id),
        FOREIGN KEY (products_id) REFERENCES products (id) 
      );
    """]
  try:
    with sqlite3.connect(os.getenv("DB_CONNECTION")) as conn:
      cursor = conn.cursor()
      for statement in sql_statements:
        cursor.execute(statement)
        conn.commit()
  except sqlite3.Error as e:
    print(e)