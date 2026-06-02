from typing import Dict, List

from fastapi import APIRouter, HTTPException, Response, status

from app.models import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])

products_db: Dict[int, Product] = {}
_next_product_id = 1


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Create a new product.",
    responses={201: {"description": "Product created"}},
)
def create_product(payload: ProductCreate) -> Product:
    global _next_product_id
    product = Product(id=_next_product_id, **payload.model_dump())
    products_db[product.id] = product
    _next_product_id += 1
    return product


@router.get(
    "/",
    response_model=List[Product],
    summary="List products",
    description="Return all products.",
)
def list_products() -> List[Product]:
    return list(products_db.values())


@router.get(
    "/{product_id}",
    response_model=Product,
    summary="Get product",
    description="Get a product by ID.",
    responses={404: {"description": "Product not found"}},
)
def get_product(product_id: int) -> Product:
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put(
    "/{product_id}",
    response_model=Product,
    summary="Update product",
    description="Replace a product by ID.",
    responses={404: {"description": "Product not found"}},
)
def update_product(product_id: int, payload: ProductCreate) -> Product:
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    product = Product(id=product_id, **payload.model_dump())
    products_db[product_id] = product
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete a product by ID.",
    responses={404: {"description": "Product not found"}},
)
def delete_product(product_id: int) -> Response:
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db.pop(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
