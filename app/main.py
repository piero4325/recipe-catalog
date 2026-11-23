from fastapi import FastAPI

from app.endpoints import categories, ingredients, recipes

app = FastAPI(
    title="Recipe Catalog API",
    description="API for managing recipes, ingredients, and categories",
    version="1.0.0",
)

app.include_router(categories.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)


@app.get("/")
def root():
    return {"message": "Recipe Catalog API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
