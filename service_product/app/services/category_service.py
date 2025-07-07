from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Category
from app.schemas.category import CategoryOut

async def get_category_by_id(category_id: int, db: Session) -> CategoryOut:
    categoy = db.query(Category).filter(Category.id == category_id).first()
    if not categoy:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryOut.model_validate(categoy)

async def get_all_categories(db: Session) -> list[CategoryOut]:
    categories = db.query(Category).all()
    return [CategoryOut.model_validate(category) for category in categories]

async def create_category(category_name: str, db: Session) -> CategoryOut:
    new_category = Category(name=category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return CategoryOut.model_validate(new_category)

async def update_category(category_id: int, category_name: str, db: Session) -> CategoryOut:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.name = category_name
    db.commit()
    db.refresh(category)
    return CategoryOut.model_validate(category)

async def delete_category(category_id: int, db: Session) -> CategoryOut:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return CategoryOut.model_validate(category)