from threading import RLock
from typing import Dict, Set

from app.models import Order, Product, User

users_db: Dict[int, User] = {}
user_email_index: Set[str] = set()
products_db: Dict[int, Product] = {}
orders_db: Dict[int, Order] = {}

state_lock = RLock()

_next_user_id = 1
_next_product_id = 1
_next_order_id = 1


def get_next_user_id() -> int:
    global _next_user_id
    with state_lock:
        user_id = _next_user_id
        _next_user_id += 1
    return user_id


def get_next_product_id() -> int:
    global _next_product_id
    with state_lock:
        product_id = _next_product_id
        _next_product_id += 1
    return product_id


def get_next_order_id() -> int:
    global _next_order_id
    with state_lock:
        order_id = _next_order_id
        _next_order_id += 1
    return order_id
