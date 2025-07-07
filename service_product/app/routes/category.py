from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.category import CategoryOut, CategoryInput
from app.services.category_service import *
from app.db.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/", response_model=List[CategoryOut], status_code=status.HTTP_200_OK)
async def get_categories(db: Session = Depends(get_db)):
    return await get_all_categories(db)

@router.get("/{category_id}", response_model=CategoryOut, status_code=status.HTTP_200_OK)
async def get_by_id(category_id: int, db: Session = Depends(get_db)):
    return await get_category_by_id(category_id, db)

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def add_category(category_data: CategoryInput, db: Session = Depends(get_db)):
    return await create_category(category_data, db)

@router.put("/{category_id}", response_model=CategoryOut, status_code=status.HTTP_200_OK)
async def update_category_by_id(category_id: int, category_data: CategoryInput, db: Session = Depends(get_db)):
    return await update_category(category_id, category_data, db)

@router.delete("/{category_id}", response_model=CategoryOut, status_code=status.HTTP_200_OK)
async def delete_by_id(category_id: int, db: Session = Depends(get_db)):
    return await delete_category(category_id, db)