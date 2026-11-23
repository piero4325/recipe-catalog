
REST API каталога рецептов: категории, ингредиенты и рецепты со связью «многие-ко-многим» (ингредиент + количество). Проект на FastAPI + SQLAlchemy 2.0 + Alembic + Pydantic v2.

Возможности

- CRUD для категорий, ингредиентов и рецептов
- Связь рецепт ↔ ингредиент через association object с полем `amount`
- Валидация входных данных (Pydantic), автоматические ошибки 422
- Проверка существования связанных сущностей (404)
- Фильтрация рецептов по категории, пагинация (`skip` / `limit`)
- Миграции схемы БД через Alembic (upgrade / downgrade)
- Автодокументация Swagger: `/docs`


Запуск

```bash
git clone https://github.com/piero4325/recipe-catalog.git
cd recipe-catalog

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Документация: http://127.0.0.1:8000/docs

## Эндпоинты

| Метод | Путь | Описание |
|---|---|---|
| GET | `/health` | проверка работоспособности |
| POST | `/categories/` | создать категорию |
| GET | `/categories/` | список категорий |
| GET / PUT / DELETE | `/categories/{id}` | чтение / обновление / удаление |
| POST | `/ingredients/` | создать ингредиент |
| GET | `/ingredients/` | список ингредиентов |
| GET / PUT / DELETE | `/ingredients/{id}` | чтение / обновление / удаление |
| POST | `/recipes/` | создать рецепт с ингредиентами |
| GET | `/recipes/` | список (`skip`, `limit`, `category_id`) |
| GET / PUT / DELETE | `/recipes/{id}` | чтение / обновление / удаление |

Пример: создание рецепта

`POST /recipes/`

```json
{
  "title": "Кекс",
  "cooking_time": 45,
  "servings": 4,
  "category_id": 1,
  "ingredients": [
    {"ingredient_id": 1, "amount": 200},
    {"ingredient_id": 2, "amount": 300}
  ]
}
```

Миграции

```bash
alembic revision --autogenerate -m "описание изменения"  # создать миграцию
alembic upgrade head     # применить
alembic downgrade -1     # откатить на шаг назад
alembic history          # история миграций
alembic current          # текущая версия БД
```

## Структура проекта

```
recipe-catalog/
├── alembic/             # миграции
├── app/
│   ├── database.py      # engine, сессии, get_db
│   ├── models.py        # таблицы SQLAlchemy
│   ├── schemas.py       # Pydantic-схемы
│   ├── main.py          # приложение FastAPI
│   └── endpoints/       # роутеры: categories, ingredients, recipes
├── alembic.ini
├── requirements.txt
└── .env.example
```