🚀 PriceSenseAI: AI-Powered Product Price Prediction & Smart Alert System

PriceSenseAI is a production-ready end-to-end machine learning system that tracks product prices, predicts future price trends using LSTM-based time series modeling, and automatically notifies users when it’s the optimal time to buy.

Built with real-world engineering practices including backend APIs, data pipelines, model deployment, and automated notifications.

🧠 Problem Statement

Consumers struggle to decide the best time to purchase products due to fluctuating prices.

PriceSenseAI solves this by:

Tracking historical product price data

Predicting future price trends using deep learning

Automatically alerting users when a price drop is expected

🏗️ System Architecture
User → Frontend (React)
      → Backend API (FastAPI)
      → Database (MySQL)
      → Data Pipeline (Scraper + Scheduler)
      → LSTM Model (Price Prediction)
      → Notification Service (Email)
      → User
⚙️ Tech Stack
Backend

Python

FastAPI

MygreSQL

APScheduler (cron jobs)

SMTP (Email automation)

Machine Learning

LSTM (Time Series Forecasting)

Pandas / NumPy

Scikit-learn

TensorFlow / Keras

Frontend

React.js

Axios

Chart.js (trend visualization)

DevOps (Optional Enhancement)

Docker

CI/CD (GitHub Actions)

Cloud Deployment (AWS / GCP)

🔁 End-to-End Workflow

User searches and selects a product.

Backend stores product and user email.

Scheduler runs periodically:

Scrapes latest product price.

Updates database.

Historical data is fed into LSTM model.

Model predicts future price trend.

If predicted price meets user condition:

Email notification is triggered automatically.

Frontend displays updated trend graph.

📊 Machine Learning Model
Model Type:

LSTM (Long Short-Term Memory Network)

Why LSTM?

Handles time series dependencies

Captures price trends and seasonality

Learns sequential patterns from historical data

Input:

Last N days of price history

Output:

Predicted future price

📬 Email Alert Logic

Trigger Conditions:

Predicted price < user target price

Significant downward trend detected

Real-time price drop observed

Automated using SMTP integration.

🗂️ Project Structure
PriceSenseAI/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── scheduler.py
│
├── model/
│   ├── train.py
│   ├── predict.py
│   └── lstm_model.h5
│
├── data_pipeline/
│   ├── scraper.py
│   ├── preprocess.py
│
├── frontend/
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
🧪 Running the Project Locally
1️⃣ Clone the repository
git clone [https://github.com/pandanode/PriceSenseAI.git](https://github.com/pandanode/PriceSenseAI)
cd PriceSenseAI
2️⃣ Setup backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
3️⃣ Run frontend
cd frontend
npm install
npm start
📈 Future Improvements

Reinforcement learning for buy/sell recommendations

Multi-platform scraping

Real-time websocket updates

Mobile app integration

Cloud deployment with CI/CD

🏆 Engineering Highlights

Full end-to-end ML pipeline

Production-style API architecture

Automated data ingestion

Real-time notification engine

Modular and scalable design


📄 License

MIT License