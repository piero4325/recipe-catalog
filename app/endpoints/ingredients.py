from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db


router = APIRouter(prefix="/ingredients", tags=["ingredients"])



@router.post("/", response_model=schemas.IngredientRead, status_code=201)
def create_ingredient(
    ingredient: schemas.IngredientCreate,
    db: Session = Depends(get_db),
):

    existing = db.query(models.Ingredient).filter(models.Ingredient.name == ingredient.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Ingredient with this name already exists")

    db_ingredient = models.Ingredient(**ingredient.model_dump())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


@router.get("/", response_model=List[schemas.IngredientRead])
def get_ingredients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()


@router.get("/{ingredient_id}", response_model=schemas.IngredientRead)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient



@router.put("/{ingredient_id}", response_model=schemas.IngredientRead)
def update_ingredient(
    ingredient_id: int,
    ingredient_update: schemas.IngredientUpdate,
    db: Session = Depends(get_db),
):
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    update_data = ingredient_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ingredient, field, value)

    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient



@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db.delete(db_ingredient)
    db.commit()
    return None