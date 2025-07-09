from fastapi import FastAPI
from app.routes import auth, user
from app.db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Auth API",
    description="Authentication API for authentication and user management",
    version="1.0.0",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)