from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=schemas.CategoryRead, status_code=201)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Category with this name already exists",
        )

    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=List[schemas.CategoryRead])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return db.query(models.Category).offset(skip).limit(limit).all()


@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    category_update: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
):
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category_update.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing = db.query(models.Category).filter(
            models.Category.name == update_data["name"],
            models.Category.id != category_id,
        ).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Category with this name already exists",
            )

    for field, value in update_data.items():
        setattr(db_category, field, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    recipe_exists = db.query(models.Recipe).filter(
        models.Recipe.category_id == category_id
    ).first()
    if recipe_exists:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete category because it contains recipes",
        )

    db.delete(db_category)
    db.commit()
    return None
