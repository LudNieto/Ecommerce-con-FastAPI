from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer 
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from app.core.config import settings
from app.schema.auth import Token
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(data: dict, access_token_expiry: Optional[int] = None) -> str:
    to_encode = data.copy()
    
    expire_minutes = access_token_expiry or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)

    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_user_token(id: int, refresh_token: Optional[str] = None) -> Token:
    payload = {"id": id}
    access_token_expiry = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = await create_access_token(data=payload, access_token_expiry=access_token_expiry)
    
    if not refresh_token:
        refresh_token = await create_access_token(data=payload)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry * 60
    )

async def get_token_payload(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    payload = await get_token_payload(token.credentials)
    user_id = payload.get("id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: Id not found",
        )
    
    return user_id
