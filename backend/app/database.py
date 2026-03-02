import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "pricesenseai")
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def save_price(product_name: str, platform: str, price: float, url: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM products WHERE name = %s", (product_name,))
    row = cursor.fetchone()

    if row:
        product_id = row[0]
    else:
        cursor.execute(
            "INSERT INTO products (name, url) VALUES (%s, %s)",
            (product_name, url)
        )
        product_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO price_history (product_id, platform, price) VALUES (%s, %s, %s)",
        (product_id, platform, price)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return product_id


def get_price_history(product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT platform, price, recorded_at 
           FROM price_history 
           WHERE product_id = %s 
           ORDER BY recorded_at DESC 
           LIMIT 50""",
        (product_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def save_alert(email: str, product_id: int, target_price: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        user_id = row[0]
    else:
        cursor.execute("INSERT INTO users (email) VALUES (%s)", (email,))
        user_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO alerts (user_id, product_id, target_price) VALUES (%s, %s, %s)",
        (user_id, product_id, target_price)
    )

    conn.commit()
    cursor.close()
    conn.close()