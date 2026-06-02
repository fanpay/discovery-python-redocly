from fastapi import FastAPI

from app.routers.orders import router as orders_router
from app.routers.products import router as products_router
from app.routers.users import router as users_router

app = FastAPI(
    title="Redocly FastAPI Sample",
    version="0.1.0",
    description=(
        "Sample API for OpenAPI and Redocly experimentation. "
        "Includes CRUD-style endpoints for users, products, and orders."
    ),
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations related to user records and profiles.",
        },
        {
            "name": "Products",
            "description": "Operations related to product catalog management.",
        },
        {
            "name": "Orders",
            "description": "Operations related to order lifecycle and totals.",
        },
    ],
)

app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)
