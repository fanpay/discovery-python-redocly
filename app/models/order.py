from typing import List

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    product_id: int = Field(..., example=1, description="Referenced product ID")
    quantity: int = Field(..., gt=0, example=2, description="Number of items")


class OrderCreate(BaseModel):
    user_id: int = Field(..., example=1, description="User placing the order")
    items: List[OrderItem] = Field(..., min_items=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1},
                ],
            }
        }
    }


class Order(OrderCreate):
    id: int = Field(..., example=1, description="Unique order ID")
    total: float = Field(..., example=389.97, description="Computed order total in USD")
