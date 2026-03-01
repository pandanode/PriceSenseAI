from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from data_pipeline.scraper import get_all_prices
from database import save_price, get_price_history, save_alert

router = APIRouter()


# -------------------------------------------------------
# REQUEST MODELS
# -------------------------------------------------------

class AlertRequest(BaseModel):
    email: str
    product_name: str
    target_price: float


# -------------------------------------------------------
# ENDPOINTS
# -------------------------------------------------------

@router.get("/search")
async def search(q: str):
    """Search all platforms and return price comparison"""
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query too short")

    results = get_all_prices(q)

    if not results:
        raise HTTPException(status_code=404, detail="No results found")

    # Save to database
    for r in results:
        save_price(q, r["platform"], r["price"], r["url"])

    # Find best deal
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
    """Get price history for a product"""
    rows = get_price_history(product_id)
    if not rows:
        raise HTTPException(status_code=404, detail="No history found")
    return {"product_id": product_id, "history": rows}


@router.post("/alert")
async def create_alert(data: AlertRequest):
    """Set a price drop alert"""
    results = get_all_prices(data.product_name)
    if not results:
        raise HTTPException(status_code=404, detail="Product not found")

    product_id = save_price(
        data.product_name,
        results[0]["platform"],
        results[0]["price"],
        results[0]["url"]
    )
    save_alert(data.email, product_id, data.target_price)

    return {
        "message": f"Alert set! You'll be notified when price drops below ₹{data.target_price}",
        "email": data.email,
        "target_price": data.target_price
    }