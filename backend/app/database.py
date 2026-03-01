import mysql.connector
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "porsche718~1!@",  # ← change this
    "database": "pricesenseai"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def save_price(product_name: str, platform: str, price: float, url: str):
    """Save scraped price to price_history table"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get or create product
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

    # Save price record
    cursor.execute(
        "INSERT INTO price_history (product_id, platform, price) VALUES (%s, %s, %s)",
        (product_id, platform, price)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return product_id


def get_price_history(product_id: int):
    """Get all historical prices for a product"""
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
    """Save a price drop alert for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get or create user
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        user_id = row[0]
    else:
        cursor.execute("INSERT INTO users (email) VALUES (%s)", (email,))
        user_id = cursor.lastrowid

    # Save alert
    cursor.execute(
        "INSERT INTO alerts (user_id, product_id, target_price) VALUES (%s, %s, %s)",
        (user_id, product_id, target_price)
    )

    conn.commit()
    cursor.close()
    conn.close()