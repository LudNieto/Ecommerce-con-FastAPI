from pydantic import BaseModel, ConfigDict, Field
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
    price: Decimal = Field(..., gt=0, description="Precio del producto (mayor que 0).")
    iva: Decimal = Field(..., ge=0, le=1, description="IVA como decimal entre 0 y 1.")
    category_id: int | None = None

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    img_url: str | None = None
    price: Decimal | None = Field(default=None, gt=0, description="Nuevo precio (si se provee, debe ser > 0).")
    iva: Decimal | None = Field(default=None, ge=0, le=1, description="Nuevo IVA (entre 0 y 1 si se provee).")
    category_id: int | None = None
    status: ProductStatus | None = None

