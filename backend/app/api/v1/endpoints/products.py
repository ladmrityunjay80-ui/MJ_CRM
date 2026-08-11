"""
Product Endpoints
CRUD operations for products
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, Product, ProductListResponse
from app.models.user import User as UserModel
from app.models.product import Product as ProductModel

router = APIRouter()


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new product"""
    product_dict = product_data.model_dump(exclude={"tags"})
    new_product = ProductModel(
        id=str(uuid.uuid4()),
        **product_dict,
        organization_id=current_user.organization_id,
        tags=json.dumps(product_data.tags) if product_data.tags else None
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.get("/", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all products with filtering and pagination"""
    # Build query
    query = db.query(ProductModel).filter(ProductModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if type:
        query = query.filter(ProductModel.type == type)
    if is_active is not None:
        query = query.filter(ProductModel.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    products = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "products": products,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific product"""
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id,
        ProductModel.organization_id == current_user.organization_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a product"""
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id,
        ProductModel.organization_id == current_user.organization_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update product fields
    update_data = product_data.model_dump(exclude_unset=True)
    if "tags" in update_data:
        update_data["tags"] = json.dumps(update_data["tags"]) if update_data["tags"] else None
    
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a product"""
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id,
        ProductModel.organization_id == current_user.organization_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    
    return None
