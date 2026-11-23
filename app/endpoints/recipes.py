from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/", response_model=schemas.RecipeRead, status_code=201)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(
        models.Category.id == recipe.category_id
    ).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db_recipe = models.Recipe(**recipe.model_dump(exclude={"ingredients"}))

    for item in recipe.ingredients:
        ingredient = db.query(models.Ingredient).filter(
            models.Ingredient.id == item.ingredient_id
        ).first()
        if ingredient is None:
            raise HTTPException(
                status_code=404,
                detail=f"Ingredient {item.ingredient_id} not found",
            )

        db_recipe.recipe_ingredients.append(
            models.RecipeIngredient(
                ingredient_id=item.ingredient_id,
                amount=item.amount,
            )
        )

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.get("/", response_model=List[schemas.RecipeRead])
def get_recipes(
    skip: int = 0,
    limit: int = 100,
    category_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Recipe)
    if category_id is not None:
        query = query.filter(models.Recipe.category_id == category_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{recipe_id}", response_model=schemas.RecipeRead)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{recipe_id}", response_model=schemas.RecipeRead)
def update_recipe(
    recipe_id: int,
    recipe_update: schemas.RecipeUpdate,
    db: Session = Depends(get_db),
):
    db_recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_data = recipe_update.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = db.query(models.Category).filter(
            models.Category.id == update_data["category_id"]
        ).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

    for field, value in update_data.items():
        setattr(db_recipe, field, value)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted"}
