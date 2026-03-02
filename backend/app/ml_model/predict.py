import numpy as np
import pandas as pd
import mysql.connector
import pickle
from tensorflow.keras.models import load_model

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "porsche718~1!@",  # ← change this
    "database": "pricesenseai"
}

SEQUENCE_LEN = 10
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "lstm_model.keras")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")


def get_recent_prices(product_name: str, platform: str = None):
    """Get last 10 prices for a product from MySQL"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT ph.price FROM price_history ph
        JOIN products p ON ph.product_id = p.id
        WHERE p.name = %s
    """
    params = [product_name]

    if platform:
        query += " AND ph.platform = %s"
        params.append(platform)

    query += " ORDER BY ph.recorded_at DESC LIMIT %s"
    params.append(SEQUENCE_LEN)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    prices = [r["price"] for r in reversed(rows)]
    return prices


def predict_future_prices(product_name: str, platform: str = "Amazon"):
    """Predict next 30/60/90 day prices using trained LSTM"""
    try:
        model = load_model(MODEL_PATH)
        with open(SCALER_PATH, "rb") as f:
            scaler = pickle.load(f)
    except Exception as e:
        print(f"❌ Model not found: {e}")
        return None

    prices = get_recent_prices(product_name, platform)

    if len(prices) < SEQUENCE_LEN:
        print(f"⚠️ Not enough data ({len(prices)} records, need {SEQUENCE_LEN})")
        return None

    current_price = prices[-1]
    results = {}

    # Predict for 7, 30, 90 days ahead
    for days_ahead, label in [(7, "next_week"), (30, "next_month"), (90, "next_3_months")]:
        sequence = list(prices[-SEQUENCE_LEN:])

        for _ in range(days_ahead):
            scaled = scaler.transform(np.array(sequence[-SEQUENCE_LEN:]).reshape(-1, 1))
            X = scaled.reshape(1, SEQUENCE_LEN, 1)
            pred_scaled = model.predict(X, verbose=0)
            pred_price = scaler.inverse_transform(pred_scaled)[0][0]
            sequence.append(float(pred_price))

        predicted = round(float(sequence[-1]), 2)
        change = round(predicted - current_price, 2)
        change_pct = round((change / current_price) * 100, 1)

        results[label] = {
            "price": predicted,
            "change": change,
            "change_pct": change_pct,
            "trend": "up" if change > 0 else "down" if change < 0 else "stable"
        }

    results["current_price"] = current_price
    results["platform"] = platform
    results["product"] = product_name

    return results


if __name__ == "__main__":
    result = predict_future_prices("Python Crash Course", "Amazon")
    if result:
        print(f"\n📚 Predictions for: {result['product']}")
        print(f"💰 Current Price : ₹{result['current_price']}")
        print(f"📅 Next Week     : ₹{result['next_week']['price']} ({result['next_week']['change_pct']}%)")
        print(f"📅 Next Month    : ₹{result['next_month']['price']} ({result['next_month']['change_pct']}%)")
        print(f"📅 Next 3 Months : ₹{result['next_3_months']['price']} ({result['next_3_months']['change_pct']}%)")