from fastapi import FastAPI
from app.routes import auth, user
from app.db.database import engine, Base

app = FastAPI(
    title="Auth API",
    description="Authentication API for authentication and user management",
    version="1.0.0",)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)