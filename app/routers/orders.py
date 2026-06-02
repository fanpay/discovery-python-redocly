from typing import Dict, List

from fastapi import APIRouter, HTTPException, Response, status

from app.models import Order, OrderCreate
from app.routers.products import products_db
from app.routers.users import users_db

router = APIRouter(prefix="/orders", tags=["Orders"])

orders_db: Dict[int, Order] = {}
_next_order_id = 1


def _build_order(order_id: int, payload: OrderCreate) -> Order:
    if payload.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    total = 0.0
    for item in payload.items:
        product = products_db.get(item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found",
            )
        total += product.price * item.quantity

    return Order(id=order_id, total=round(total, 2), **payload.model_dump())


@router.post(
    "/",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    summary="Create order",
    description="Create a new order for an existing user and products.",
    responses={
        201: {"description": "Order created"},
        404: {"description": "User or product not found"},
    },
)
def create_order(payload: OrderCreate) -> Order:
    global _next_order_id
    order = _build_order(_next_order_id, payload)
    orders_db[order.id] = order
    _next_order_id += 1
    return order


@router.get(
    "/",
    response_model=List[Order],
    summary="List orders",
    description="Return all orders.",
)
def list_orders() -> List[Order]:
    return list(orders_db.values())


@router.get(
    "/{order_id}",
    response_model=Order,
    summary="Get order",
    description="Get an order by ID.",
    responses={404: {"description": "Order not found"}},
)
def get_order(order_id: int) -> Order:
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put(
    "/{order_id}",
    response_model=Order,
    summary="Update order",
    description="Replace an order by ID.",
    responses={404: {"description": "Order, user, or product not found"}},
)
def update_order(order_id: int, payload: OrderCreate) -> Order:
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    order = _build_order(order_id, payload)
    orders_db[order_id] = order
    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete order",
    description="Delete an order by ID.",
    responses={404: {"description": "Order not found"}},
)
def delete_order(order_id: int) -> Response:
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db.pop(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
