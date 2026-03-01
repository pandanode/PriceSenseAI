from database import get_connection, save_price, get_price_history

# Test connection
try:
    conn = get_connection()
    print("✅ MySQL connected!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")

# Test saving a price
try:
    product_id = save_price(
        "Python Crash Course",
        "Amazon",
        3533.0,
        "https://www.amazon.in/test"
    )
    print(f"✅ Price saved! Product ID: {product_id}")
except Exception as e:
    print(f"❌ Save failed: {e}")

# Test reading history
try:
    rows = get_price_history(4)
    print(f"✅ History found: {len(rows)} records")
    for r in rows:
        print(f"   {r}")
except Exception as e:
    print(f"❌ History failed: {e}")