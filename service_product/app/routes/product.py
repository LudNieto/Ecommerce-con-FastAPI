from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.models.models import ProductStatus
from app.services.product_service import *
from app.db.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_products(db: Session = Depends(get_db)):
    return await get_all_products(db)

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return await create_product(product_data, db)

@router.get("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get_by_id(product_id: int, db: Session = Depends(get_db)):
    return await get_product_by_id(product_id, db)

@router.get("/category/{category_id}", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_by_category(category_id: int, db: Session = Depends(get_db)):
    return await get_all_products_by_category(category_id, db)

@router.get("/status/{product_status}", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_by_status(product_status: ProductStatus, db: Session = Depends(get_db)):  
    return await get_all_products_by_status(product_status, db)

@router.put("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def update_product_by_id(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return await update_product(product_id, product_data, db)

@router.delete("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    return await deactivate_product(product_id, db)