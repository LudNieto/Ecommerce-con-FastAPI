from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import User
from app.schema.user import UserOut, UserUpdate
from app.core.security import get_password_hash

async def get_user_by_id(user_id: int, db: Session) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)

async def update_user(user_id: int, user_data: UserUpdate, db: Session) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_data.model_dump(exclude_unset=True).items():
        if key == "password":
            setattr(user, "hashed_password", get_password_hash(value))
        else:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)

async def deactivate_user(user_id: int, db: Session) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)