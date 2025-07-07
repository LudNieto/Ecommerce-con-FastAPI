from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List
from decimal import Decimal
from app.models.models import OrderStatus

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderItemOut(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_time_of_order: Decimal
    iva_at_time_of_order: Decimal

    model_config = ConfigDict(from_attributes=True)

class OrderItemCreateInput(BaseModel):
    product_id: int = Field(..., gt=0, description="ID del producto.")
    quantity: int = Field(..., gt=0, description="Cantidad del producto.")

class OrderCreateWithItems(BaseModel):
    user_id: int
    items: List[OrderItemCreateInput] = Field(..., min_length=1, description="Lista de productos en la orden.")

class OrderUpdate(BaseModel):
    status: OrderStatus | None = None