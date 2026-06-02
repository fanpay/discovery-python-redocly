from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., example="Mechanical Keyboard", description="Product name")
    description: str = Field(..., example="A tactile mechanical keyboard")
    price: float = Field(..., gt=0, example=129.99, description="Price in USD")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Mechanical Keyboard",
                "description": "A tactile mechanical keyboard",
                "price": 129.99,
            }
        }
    }


class Product(ProductCreate):
    id: int = Field(..., example=1, description="Unique product ID")
