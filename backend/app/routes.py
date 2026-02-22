from fastapi import APIRouter
from sqlalchemy import text
from app.database import SessionLocal

router = APIRouter()

@router.get("/products")
def get_products():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM products"))
        products = result.fetchall()
        return {"products": [dict(row._mapping) for row in products]}
    finally:
        db.close()