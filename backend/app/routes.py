from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from data_pipeline.scraper import get_all_prices
from database import save_price, get_price_history, save_alert
from email_service import send_alert_confirmation

router = APIRouter()


class AlertRequest(BaseModel):
    email: str
    product_name: str
    target_price: float


@router.get("/search")
async def search(q: str):
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query too short")

    results = get_all_prices(q)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")

    for r in results:
        save_price(q, r["platform"], r["price"], r["url"])

    best = min(results, key=lambda x: x["price"])
    worst = max(results, key=lambda x: x["price"])

    return {
        "query": q,
        "results": results,
        "best_deal": best,
        "savings": round(worst["price"] - best["price"], 2)
    }


@router.get("/history/{product_id}")
async def history(product_id: int):
    rows = get_price_history(product_id)
    if not rows:
        raise HTTPException(status_code=404, detail="No history found")
    return {"product_id": product_id, "history": rows}


# ✅ ONLY ONE /alert endpoint — with email sending
@router.post("/alert")
async def create_alert(data: AlertRequest):
    results = get_all_prices(data.product_name)
    if not results:
        raise HTTPException(status_code=404, detail="Product not found")

    best = min(results, key=lambda x: x["price"])

    product_id = save_price(
        data.product_name,
        best["platform"],
        best["price"],
        best["url"]
    )
    save_alert(data.email, product_id, data.target_price)

    send_alert_confirmation(
        to_email=data.email,
        product_name=data.product_name,
        target_price=data.target_price,
        current_price=best["price"],
        best_platform=best["platform"],
        best_url=best["url"]
    )

    return {
        "message": f"Alert set! Confirmation email sent to {data.email}",
        "email": data.email,
        "target_price": data.target_price
    }

from ml_model.predict import predict_future_prices

@router.get("/predict")
async def predict(q: str, platform: str = "Amazon"):
    """Get AI price predictions for a book"""
    result = predict_future_prices(q, platform)
    if not result:
        raise HTTPException(status_code=404, detail="Not enough data to predict")
    return result