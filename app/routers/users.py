from typing import List

from fastapi import APIRouter, HTTPException, Response, status

from app.models import User, UserCreate
from app.state import get_next_user_id, state_lock, users_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    description="Create a new user. Returns `400` if the email already exists.",
    responses={
        201: {"description": "User created"},
        400: {"description": "Email already exists"},
    },
)
def create_user(payload: UserCreate) -> User:
    with state_lock:
        if any(user.email == payload.email for user in users_db.values()):
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(id=get_next_user_id(), **payload.model_dump())
        users_db[user.id] = user
    return user


@router.get(
    "/",
    response_model=List[User],
    summary="List users",
    description="Return all users.",
)
def list_users() -> List[User]:
    return list(users_db.values())


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get user",
    description="Get a user by ID.",
    responses={404: {"description": "User not found"}},
)
def get_user(user_id: int) -> User:
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put(
    "/{user_id}",
    response_model=User,
    summary="Update user",
    description="Replace a user by ID.",
    responses={404: {"description": "User not found"}},
)
def update_user(user_id: int, payload: UserCreate) -> User:
    with state_lock:
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        user = User(id=user_id, **payload.model_dump())
        users_db[user_id] = user
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by ID.",
    responses={404: {"description": "User not found"}},
)
def delete_user(user_id: int) -> Response:
    with state_lock:
        if user_id not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        users_db.pop(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
