from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.services.order_service import *
from app.db.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/{order_id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
async def get_by_id(order_id: int, db: Session = Depends(get_db)):
    return await get_order_by_id(order_id, db)

@router.get("/", response_model=List[OrderOut], status_code=status.HTTP_200_OK)
async def get_all(db: Session = Depends(get_db)):
    return await get_all_orders(db)

@router.get("/status/{status}", response_model=List[OrderOut], status_code=status.HTTP_200_OK)
async def get_by_status(status: OrderStatus, db: Session = Depends(get_db)):
    return await get_orders_by_status(status, db)

@router.get("/user/{user_id}", response_model=List[OrderOut], status_code=status.HTTP_200_OK)
async def get_by_user(user_id: int, db: Session = Depends(get_db)):
    return await get_orders_by_user(user_id, db)

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create(order_data: OrderCreateWithItems, db: Session = Depends(get_db)):
    return await create_order(order_data, db)

@router.put("/{order_id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
async def update_order_by_id(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    return await update_order(order_id, order_data, db)

@router.get("/{order_id}/items", response_model=List[OrderItemOut], status_code=status.HTTP_200_OK)
async def get_order_items(order_id: int, db: Session = Depends(get_db)):
    return await get_order_items_by_order(order_id, db)

@router.get("/items/{item_id}", response_model=OrderItemOut, status_code=status.HTTP_200_OK)
async def get_order_item(item_id: int, db: Session = Depends(get_db)):
    return await get_order_item_by_id(item_id, db)