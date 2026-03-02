import numpy as np
import pandas as pd
import mysql.connector
import pickle
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "porsche718~1!@",  # ← change this
    "database": "pricesenseai"
}

SEQUENCE_LEN = 10   # Use last 10 days to predict next price
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "lstm_model.keras")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

# -------------------------------------------------------
# LOAD DATA FROM MYSQL
# -------------------------------------------------------
def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("""
        SELECT ph.product_id, ph.platform, ph.price, ph.recorded_at
        FROM price_history ph
        ORDER BY ph.product_id, ph.platform, ph.recorded_at
    """, conn)
    conn.close()
    print(f"✅ Loaded {len(df)} price records from MySQL")
    return df


# -------------------------------------------------------
# PREPARE SEQUENCES
# -------------------------------------------------------
def prepare_sequences(df):
    scaler = MinMaxScaler()
    X_all, y_all = [], []

    groups = df.groupby(["product_id", "platform"])

    for (product_id, platform), group in groups:
        prices = group["price"].values.reshape(-1, 1)

        if len(prices) < SEQUENCE_LEN + 1:
            continue

        # Scale prices
        scaled = scaler.fit_transform(prices)

        # Create sequences
        for i in range(len(scaled) - SEQUENCE_LEN):
            X_all.append(scaled[i:i + SEQUENCE_LEN])
            y_all.append(scaled[i + SEQUENCE_LEN])

    X = np.array(X_all)
    y = np.array(y_all)

    print(f"✅ Prepared {len(X)} training sequences")
    return X, y, scaler


# -------------------------------------------------------
# BUILD LSTM MODEL
# -------------------------------------------------------
def build_model(input_shape):
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(16, activation="relu"),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    model.summary()
    return model


# -------------------------------------------------------
# TRAIN
# -------------------------------------------------------
def train():
    print("\n🤖 Starting LSTM Training...\n")

    df = load_data()
    X, y, scaler = prepare_sequences(df)

    # Split 80/20
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    print(f"📊 Train: {len(X_train)} | Test: {len(X_test)}")

    model = build_model((SEQUENCE_LEN, 1))

    # Early stopping to avoid overfitting
    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=16,
        validation_data=(X_test, y_test),
        callbacks=[early_stop],
        verbose=1
    )

    # Save model and scaler
    os.makedirs("ml_model", exist_ok=True)
    model.save(MODEL_PATH)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    # Evaluate
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n✅ Model trained!")
    print(f"📉 Test Loss : {loss:.4f}")
    print(f"📉 Test MAE  : {mae:.4f}")
    print(f"💾 Saved to  : {MODEL_PATH}")

    return model, scaler, history


if __name__ == "__main__":
    train()