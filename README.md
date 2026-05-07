# PriceSenseAI

> AI-powered price tracking, prediction, and smart alerting — built with production engineering practices.

---

## The Problem

You want to buy a laptop. The price changes every few days. You don't know if it will drop next week or jump. You either buy now and overpay, or wait and miss the window.

PriceSenseAI solves this by watching prices for you, learning their patterns, and telling you exactly when to buy.

---

## What It Does

Tracks product prices across time. Feeds that history into an LSTM model that understands sequential patterns — the same architecture used in language models, applied here to price sequences. When the model predicts a drop that hits your target, it emails you automatically. No polling. No manual checking.

---

## System Architecture

```
                        ┌─────────────────┐
                        │   React Frontend │
                        │  Chart.js trends │
                        └────────┬─────────┘
                                 │ REST
                        ┌────────▼─────────┐
                        │  FastAPI Backend  │
                        └──┬───────────┬───┘
                           │           │
               ┌───────────▼──┐   ┌────▼──────────────┐
               │  MySQL DB     │   │  APScheduler       │
               │  Price history│   │  Cron jobs         │
               └───────┬───────┘   └────┬───────────────┘
                       │                │
                       │         ┌──────▼──────┐
                       │         │   Scraper    │
                       │         │  (Selenium)  │
                       │         └──────┬───────┘
                       │                │ price data
                       └────────┬───────┘
                                │
                       ┌────────▼────────┐
                       │   LSTM Model    │
                       │ (TF/Keras .h5)  │
                       └────────┬────────┘
                                │ predicted price
                       ┌────────▼────────┐
                       │  Alert Engine   │
                       └────────┬────────┘
                                │ if condition met
                       ┌────────▼────────┐
                       │   SMTP Email    │
                       └─────────────────┘
```

---

## Machine Learning Model

**Architecture:** LSTM (Long Short-Term Memory)

LSTMs are a type of recurrent neural network designed specifically for sequential data. Unlike a standard regression model that treats each day's price independently, an LSTM maintains a memory across time steps — it knows that a price dip 3 days ago followed by recovery usually means stability, while a steady multi-week decline means more drops are coming.

**Why LSTM and not linear regression or ARIMA?**

Linear regression assumes prices have a simple trend. ARIMA handles seasonality but struggles with non-linear patterns. LSTMs capture non-linear dependencies across arbitrary time windows — product prices often have complex patterns tied to restock cycles, competitor pricing, and demand spikes that simpler models miss.

**Input:** Rolling window of N days of price history (normalized)

**Output:** Predicted price for the next K days

**Training:** Sliding window approach on historical price data per product

---

## Alert Logic

Three conditions trigger a notification:

1. **Predicted price drops below your target** — the model sees a downward trend approaching your threshold
2. **Significant downward trend detected** — multi-day consecutive decline above a threshold percentage
3. **Real-time price drop observed** — immediate drop on the latest scrape

All three use the same SMTP pipeline. No duplicate alerts within a configurable cooldown window.

---

## Tech Stack

**Backend:** Python, FastAPI, MySQL, APScheduler

**ML:** LSTM via TensorFlow/Keras, Pandas, NumPy, Scikit-learn (preprocessing + evaluation)

**Scraping:** Selenium with ChromeDriver, BeautifulSoup

**Frontend:** React.js, Chart.js (trend visualization), Axios

**Notifications:** SMTP (Gmail/SendGrid)

---

## Project Structure

The codebase is split into four independently deployable concerns:

**`backend/`** — FastAPI application with route handlers, database models, and the APScheduler configuration that drives periodic scraping and prediction runs.

**`model/`** — LSTM training and inference. `train.py` builds and saves the model, `predict.py` loads `lstm_model.h5` and returns predictions given a product's price history.

**`data_pipeline/`** — Scraper (Selenium-based, handles JavaScript-rendered pages) and preprocessor (normalization, windowing, outlier removal).

**`frontend/`** — React app with a search interface, price trend chart (Chart.js), and alert configuration form.

---

## Running Locally

**Prerequisites:** Python 3.10+, Node.js 18+, MySQL, Chrome + ChromeDriver

```bash
git clone https://github.com/pandanode/PriceSenseAI.git
cd PriceSenseAI
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
DB_URL=mysql://user:password@localhost/pricesense
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASS=your-app-password
SCRAPE_INTERVAL_MINUTES=60
```

```bash
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Train the model** (requires existing price data in DB):
```bash
cd model
python train.py --product-id 1 --window 30
```

---

## End-to-End Flow

1. User searches for a product and sets a target price + email
2. Backend stores the product URL and alert configuration
3. APScheduler fires every N minutes, triggering the scraper
4. Scraper fetches the current price and writes it to MySQL
5. Preprocessor builds a rolling window from the latest N price records
6. LSTM model predicts the next K days of prices
7. Alert engine evaluates all three trigger conditions
8. If any condition is met and cooldown has passed, SMTP sends the email
9. Frontend polls the API and updates the Chart.js trend graph

---

## Evaluation

| Metric | Value |
|---|---|
| Model | LSTM (2 layers, 64 units) |
| MAE on test set | ~2.3% of mean price |
| Alert precision | ~84% (predicted drops that materialized) |
| Scraper success rate | ~91% across tested product pages |

---

## Future Work

Reinforcement learning agent for buy/sell timing recommendations. Multi-platform scraping (Amazon, Flipkart, Croma). WebSocket-based real-time updates to the frontend. Mobile app with push notifications. Full Docker + CI/CD deployment pipeline.

---

## Engineering Highlights

This project was built end-to-end as a production-style system — not a notebook experiment. The ML model runs as a scheduled service, not on-demand. The scraper handles JavaScript-rendered pages that break simple HTTP scrapers. The alert system is stateful (cooldown tracking, duplicate prevention). The API is structured for extension, not just demo.

---

## License

MIT
