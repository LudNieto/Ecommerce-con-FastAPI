from fastapi import FastAPI
from app.routes import product, category, order
from app.db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Product API",
    description="Product API for product and order management",
    version="1.0.0",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product.router)
app.include_router(category.router)
app.include_router(order.router)
