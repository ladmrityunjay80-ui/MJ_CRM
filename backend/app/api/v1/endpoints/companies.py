"""
Company Endpoints
CRUD operations for companies
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.company import CompanyCreate, CompanyUpdate, Company, CompanyListResponse
from app.models.user import User as UserModel
from app.models.company import Company as CompanyModel

router = APIRouter()


@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new company"""
    company_dict = company_data.model_dump(exclude={"tags"})
    new_company = CompanyModel(
        id=str(uuid.uuid4()),
        **company_dict,
        organization_id=current_user.organization_id,
        tags=json.dumps(company_data.tags) if company_data.tags else None
    )
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return new_company


@router.get("/", response_model=CompanyListResponse)
def get_companies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    industry: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all companies with filtering and pagination"""
    # Build query
    query = db.query(CompanyModel).filter(CompanyModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if industry:
        query = query.filter(CompanyModel.industry == industry)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    companies = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "companies": companies,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{company_id}", response_model=Company)
def get_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific company"""
    company = db.query(CompanyModel).filter(
        CompanyModel.id == company_id,
        CompanyModel.organization_id == current_user.organization_id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company


@router.put("/{company_id}", response_model=Company)
def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a company"""
    company = db.query(CompanyModel).filter(
        CompanyModel.id == company_id,
        CompanyModel.organization_id == current_user.organization_id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Update company fields
    update_data = company_data.model_dump(exclude_unset=True)
    if "tags" in update_data:
        update_data["tags"] = json.dumps(update_data["tags"]) if update_data["tags"] else None
    
    for field, value in update_data.items():
        setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a company"""
    company = db.query(CompanyModel).filter(
        CompanyModel.id == company_id,
        CompanyModel.organization_id == current_user.organization_id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    db.delete(company)
    db.commit()
    
    return None
