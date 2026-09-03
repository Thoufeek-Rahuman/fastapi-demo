from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of products to skip (pagination)"),
    limit: int = Query(10, ge=1, le=100, description="Max products to return (1-100)"),
    search: Optional[str] = Query(None, description="Search by product name"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock availability"),
):
    """
    Get all products with optional filtering and pagination.
    
    - **skip**: Skip N products (for pagination)
    - **limit**: Return at most N products
    - **search**: Filter by name (case-insensitive)
    - **min_price**: Only products >= this price
    - **max_price**: Only products <= this price
    - **in_stock**: True = quantity > 0, False = quantity = 0
    """
    query = db.query(Product)
    
    # Apply filters
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if in_stock is not None:
        if in_stock:
            query = query.filter(Product.quantity > 0)
        else:
            query = query.filter(Product.quantity == 0)
    
    # Apply pagination
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Get a product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product."""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated_product: ProductUpdate, db: Session = Depends(get_db)):
    """Update an existing product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.quantity = updated_product.quantity
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return None
