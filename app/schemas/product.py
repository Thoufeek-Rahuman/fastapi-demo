from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    """Base schema with common product fields."""
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass


class ProductUpdate(ProductBase):
    """Schema for updating an existing product."""
    pass


class ProductResponse(ProductBase):
    """Schema for product response with ID."""
    id: int

    class Config:
        from_attributes = True  # Allows ORM model to Pydantic conversion
