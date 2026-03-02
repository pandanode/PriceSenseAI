import mysql.connector
import random
from datetime import datetime, timedelta

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "porsche718~1!@",  # ← change this
    "database": "pricesenseai"
}

def generate_price_history():
    """Generate 90 days of realistic price data for training"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Books to simulate
    books = [
        {"name": "Python Crash Course", "base_price": 1500},
        {"name": "Atomic Habits",        "base_price": 400},
        {"name": "Rich Dad Poor Dad",    "base_price": 300},
        {"name": "The Alchemist",        "base_price": 250},
        {"name": "Clean Code",           "base_price": 2500},
    ]

    platforms = ["Amazon", "Flipkart", "Snapdeal"]

    for book in books:
        # Get or create product
        cursor.execute("SELECT id FROM products WHERE name = %s", (book["name"],))
        row = cursor.fetchone()
        if row:
            product_id = row[0]
        else:
            cursor.execute(
                "INSERT INTO products (name, url) VALUES (%s, %s)",
                (book["name"], f"https://amazon.in/search?q={book['name']}")
            )
            product_id = cursor.lastrowid

        # Generate 90 days of price data
        base = book["base_price"]
        price = base

        for day in range(90):
            date = datetime.now() - timedelta(days=(90 - day))

            for platform in platforms:
                # Simulate realistic price fluctuation
                # Weekend discount
                if date.weekday() >= 5:
                    change = random.uniform(-0.08, 0.02)
                # Sale seasons (every ~30 days)
                elif day % 30 < 5:
                    change = random.uniform(-0.12, -0.02)
                else:
                    change = random.uniform(-0.03, 0.04)

                price = max(base * 0.5, price * (1 + change))

                # Platform price variation
                platform_factor = {
                    "Amazon": 1.0,
                    "Flipkart": random.uniform(0.92, 1.05),
                    "Snapdeal": random.uniform(0.88, 1.08)
                }[platform]

                final_price = round(price * platform_factor, 2)

                cursor.execute(
                    """INSERT INTO price_history (product_id, platform, price, recorded_at)
                       VALUES (%s, %s, %s, %s)""",
                    (product_id, platform, final_price, date)
                )

        print(f"✅ Generated 90 days of data for: {book['name']}")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n🎉 Training data generation complete!")

if __name__ == "__main__":
    generate_price_history()