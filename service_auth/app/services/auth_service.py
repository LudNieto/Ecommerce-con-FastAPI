from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import get_user_token
from app.models.models import User
from app.schema.auth import Token, UserSignup
from app.schema.user import UserOut
from app.core.security import get_password_hash, get_token_payload, verify_password

async def signup(user: UserSignup, db: Session) -> UserOut:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered",)
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut.model_validate(new_user)

async def signin(user_credentials: OAuth2PasswordRequestForm, db: Session) -> Token:
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return await get_user_token(id=user.id)

async def get_refresh_token(token: str, db: Session) -> Token:
    payload = await get_token_payload(token)
    user_id = payload.get("id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await get_user_token(id=user.id, refresh_token=token)