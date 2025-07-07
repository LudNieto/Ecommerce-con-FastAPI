from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from app.models.models import ProductStatus

class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    img_url: str | None = None
    price: Decimal
    iva: Decimal
    category_id: int | None = None
    status: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    img_url: str | None = None
    price: Decimal
    iva: Decimal
    category_id: int | None = None

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    img_url: str | None = None
    price: Decimal | None = None
    iva: Decimal| None = None
    category_id: int | None = None
    status: ProductStatus | None = None

