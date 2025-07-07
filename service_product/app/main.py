from fastapi import FastAPI
from app.routes import product, category
from app.db.database import engine, Base

app = FastAPI(
    title="Product API",
    description="Product API for product and order management",
    version="1.0.0",)

app.include_router(product.router)
app.include_router(category.router)
