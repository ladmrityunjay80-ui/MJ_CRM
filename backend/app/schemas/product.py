"""
Product Schemas
Pydantic models for product request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.product import ProductType


class ProductBase(BaseModel):
    """Base product schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    sku: Optional[str] = None
    type: ProductType = ProductType.PRODUCT
    price: float = Field(..., gt=0)
    currency: str = "USD"


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None
    tags: Optional[list[str]] = None


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    sku: Optional[str] = None
    type: Optional[ProductType] = None
    price: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = None


class Product(ProductBase):
    """Schema for product response"""
    id: str
    quantity_in_stock: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    is_active: bool
    organization_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """Schema for product list response"""
    products: list[Product]
    total: int
    page: int
    page_size: int
