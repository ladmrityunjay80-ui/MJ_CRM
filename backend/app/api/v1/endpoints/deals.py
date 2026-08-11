"""
Deal Endpoints
CRUD operations for deals
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.deal import DealCreate, DealUpdate, Deal, DealListResponse
from app.models.user import User as UserModel
from app.models.deal import Deal as DealModel

router = APIRouter()


@router.post("/", response_model=Deal, status_code=status.HTTP_201_CREATED)
def create_deal(
    deal_data: DealCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new deal"""
    deal_dict = deal_data.model_dump(exclude={"tags"})
    new_deal = DealModel(
        id=str(uuid.uuid4()),
        **deal_dict,
        organization_id=current_user.organization_id,
        tags=json.dumps(deal_data.tags) if deal_data.tags else None
    )
    
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    
    return new_deal


@router.get("/", response_model=DealListResponse)
def get_deals(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    stage: Optional[str] = None,
    assigned_to: Optional[str] = None,
    company_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all deals with filtering and pagination"""
    # Build query
    query = db.query(DealModel).filter(DealModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if stage:
        query = query.filter(DealModel.stage == stage)
    if assigned_to:
        query = query.filter(DealModel.assigned_to_id == assigned_to)
    if company_id:
        query = query.filter(DealModel.company_id == company_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    deals = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "deals": deals,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{deal_id}", response_model=Deal)
def get_deal(
    deal_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific deal"""
    deal = db.query(DealModel).filter(
        DealModel.id == deal_id,
        DealModel.organization_id == current_user.organization_id
    ).first()
    
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    return deal


@router.put("/{deal_id}", response_model=Deal)
def update_deal(
    deal_id: str,
    deal_data: DealUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a deal"""
    deal = db.query(DealModel).filter(
        DealModel.id == deal_id,
        DealModel.organization_id == current_user.organization_id
    ).first()
    
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    # Update deal fields
    update_data = deal_data.model_dump(exclude_unset=True)
    if "tags" in update_data:
        update_data["tags"] = json.dumps(update_data["tags"]) if update_data["tags"] else None
    
    for field, value in update_data.items():
        setattr(deal, field, value)
    
    db.commit()
    db.refresh(deal)
    
    return deal


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deal(
    deal_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a deal"""
    deal = db.query(DealModel).filter(
        DealModel.id == deal_id,
        DealModel.organization_id == current_user.organization_id
    ).first()
    
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    
    db.delete(deal)
    db.commit()
    
    return None
