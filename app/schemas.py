from pydantic import BaseModel, Field
from typing import Optional, List




class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    amount: float = Field(gt=0) 


class CategoryRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {"from_attributes": True}


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)




class IngredientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    unit: str = Field(min_length=1, max_length=50)


class IngredientRead(BaseModel):
    id: int
    name: str
    unit: str

    model_config = {"from_attributes": True}


class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    unit: Optional[str] = Field(default=None, min_length=1, max_length=50)




class RecipeIngredientRead(BaseModel):
    ingredient_id: int
    amount: float
    ingredient: IngredientRead  

    model_config = {"from_attributes": True}


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    cooking_time: Optional[int] = Field(default=None, gt=0)
    servings: Optional[int] = Field(default=None, gt=0)
    category_id: int
    ingredients: List[RecipeIngredientCreate] = Field(default_factory=list)
   



class RecipeRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    cooking_time: Optional[int]
    servings: Optional[int]
    category_id: int
    category: CategoryRead
    recipe_ingredients: List[RecipeIngredientRead] = [] 

    model_config = {"from_attributes": True}


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    cooking_time: Optional[int] = Field(default=None, gt=0)
    servings: Optional[int] = Field(default=None, gt=0)
    category_id: Optional[int] = None