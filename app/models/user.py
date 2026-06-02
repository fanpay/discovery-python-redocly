from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., example="Alice Johnson", description="Full name of the user")
    email: EmailStr = Field(..., example="alice@example.com", description="Unique email")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Alice Johnson",
                "email": "alice@example.com",
            }
        }
    }


class User(UserCreate):
    id: int = Field(..., example=1, description="Unique user ID")
