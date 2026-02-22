import requests
from bs4 import BeautifulSoup
from app.database import SessionLocal
from sqlalchemy import text

# Example: scrape product price from simple HTML
def scrape_price(url):
    # For demo, pretend we scrape the price
    # In reality, use requests + BeautifulSoup to extract real price
    # Example: return 499.99
    return 499.99

def update_prices():
    db = SessionLocal()
    products = db.execute(text("SELECT * FROM products")).fetchall()
    
    for product in products:
        price = scrape_price(product['url'])
        db.execute(text("INSERT INTO price_history (product_id, price) VALUES (:pid, :price)"),
                   {"pid": product['id'], "price": price})
        db.commit()
        print(f"Updated {product['name']} -> {price}")
    
if __name__ == "__main__":
    update_prices()