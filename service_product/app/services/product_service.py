from sqlalchemy.orm import Session
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate
from fastapi import HTTPException
from app.models.models import Product, ProductStatus, Category

async def get_product_by_id(product_id: int, db: Session) -> ProductOut:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.model_validate(product)

async def get_all_products(db: Session) -> list[ProductOut]:
    products = db.query(Product).all()
    return [ProductOut.model_validate(product) for product in products]

async def get_all_products_by_status(status: ProductStatus, db: Session) -> list[ProductOut]:
    products = db.query(Product).filter(Product.status == status).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found with the specified status")
    return [ProductOut.model_validate(product) for product in products]

async def get_all_products_by_category(category_id: int, db: Session) -> list[ProductOut]:
    products = db.query(Product).filter(Product.category_id == category_id).all()
    return [ProductOut.model_validate(product) for product in products]

async def create_product(product_data: ProductCreate, db: Session) -> ProductOut:
    if product_data.category_id:
        category = db.query(Category).filter(Category.id == product_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {product_data.category_id} not found"
            )

    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return ProductOut.model_validate(new_product)

async def update_product(product_id: int, product_data: ProductUpdate, db: Session) -> ProductOut:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = product_data.model_dump(exclude_unset=True)

    if "category_id" in updates and updates["category_id"] is not None:
        category = db.query(Category).filter(Category.id == updates["category_id"]).first()
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {updates['category_id']} not found"
            )

    for key, value in updates.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return ProductOut.model_validate(product)

async def deactivate_product(product_id: int, db: Session) -> ProductOut:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.status = "inactive"
    db.commit()
    db.refresh(product)
    return ProductOut.model_validate(product)
