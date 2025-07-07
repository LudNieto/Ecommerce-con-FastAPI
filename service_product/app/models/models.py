from sqlalchemy import Integer, Column, String, Boolean, DateTime, Text, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text
from common_db.base import Base
from enum import Enum

from common_db.models import User

class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DELETED = "deleted"

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    products = relationship("Product", backref="category", passive_deletes=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text(500))
    img_url = Column(String(255))
    price = Column(Numeric(12,2), nullable=False)
    iva = Column(Numeric(5,2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    status = Column(SQLEnum(ProductStatus, name="product_status"), nullable=False, default=ProductStatus.ACTIVE)
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    order_items = relationship("OrderItem", backref="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    user = relationship("User", backref="orders")
    total_amount = Column(Numeric(12,2), nullable=False)
    status = Column(SQLEnum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.PENDING)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    order_items = relationship("OrderItem", backref=backref("order"), cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_time_of_order = Column(Numeric(12,2), nullable=False)
    iva_at_time_of_order = Column(Numeric(5,2), nullable=False)

    __table_args__ = (UniqueConstraint('order_id', 'product_id', name='_order_product_uc'),)