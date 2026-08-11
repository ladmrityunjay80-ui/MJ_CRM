"""
Lead Endpoints
CRUD operations for leads
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.lead import LeadCreate, LeadUpdate, Lead, LeadListResponse
from app.models.user import User as UserModel
from app.models.lead import Lead as LeadModel

router = APIRouter()


@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED)
def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new lead"""
    lead_dict = lead_data.model_dump(exclude={"tags"})
    new_lead = LeadModel(
        id=str(uuid.uuid4()),
        **lead_dict,
        organization_id=current_user.organization_id,
        tags=json.dumps(lead_data.tags) if lead_data.tags else None
    )
    
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    return new_lead


@router.get("/", response_model=LeadListResponse)
def get_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all leads with filtering and pagination"""
    # Build query
    query = db.query(LeadModel).filter(LeadModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if status:
        query = query.filter(LeadModel.status == status)
    if assigned_to:
        query = query.filter(LeadModel.assigned_to_id == assigned_to)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    leads = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "leads": leads,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{lead_id}", response_model=Lead)
def get_lead(
    lead_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific lead"""
    lead = db.query(LeadModel).filter(
        LeadModel.id == lead_id,
        LeadModel.organization_id == current_user.organization_id
    ).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    return lead


@router.put("/{lead_id}", response_model=Lead)
def update_lead(
    lead_id: str,
    lead_data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a lead"""
    lead = db.query(LeadModel).filter(
        LeadModel.id == lead_id,
        LeadModel.organization_id == current_user.organization_id
    ).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Update lead fields
    update_data = lead_data.model_dump(exclude_unset=True)
    if "tags" in update_data:
        update_data["tags"] = json.dumps(update_data["tags"]) if update_data["tags"] else None
    
    for field, value in update_data.items():
        setattr(lead, field, value)
    
    db.commit()
    db.refresh(lead)
    
    return lead


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(
    lead_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a lead"""
    lead = db.query(LeadModel).filter(
        LeadModel.id == lead_id,
        LeadModel.organization_id == current_user.organization_id
    ).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    db.delete(lead)
    db.commit()
    
    return None
