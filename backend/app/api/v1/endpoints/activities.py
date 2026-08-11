"""
Activity Endpoints
CRUD operations for activities
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.activity import ActivityCreate, ActivityUpdate, Activity, ActivityListResponse
from app.models.user import User as UserModel
from app.models.activity import Activity as ActivityModel

router = APIRouter()


@router.post("/", response_model=Activity, status_code=status.HTTP_201_CREATED)
def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new activity"""
    new_activity = ActivityModel(
        id=str(uuid.uuid4()),
        **activity_data.model_dump(),
        organization_id=current_user.organization_id,
        created_by_id=current_user.id
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    
    return new_activity


@router.get("/", response_model=ActivityListResponse)
def get_activities(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    type: Optional[str] = None,
    status: Optional[str] = None,
    deal_id: Optional[str] = None,
    contact_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all activities with filtering and pagination"""
    # Build query
    query = db.query(ActivityModel).filter(ActivityModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if type:
        query = query.filter(ActivityModel.type == type)
    if status:
        query = query.filter(ActivityModel.status == status)
    if deal_id:
        query = query.filter(ActivityModel.deal_id == deal_id)
    if contact_id:
        query = query.filter(ActivityModel.contact_id == contact_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    activities = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "activities": activities,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{activity_id}", response_model=Activity)
def get_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific activity"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.organization_id == current_user.organization_id
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity


@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: str,
    activity_data: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update an activity"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.organization_id == current_user.organization_id
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Update activity fields
    update_data = activity_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete an activity"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.organization_id == current_user.organization_id
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    db.delete(activity)
    db.commit()
    
    return None
