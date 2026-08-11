"""
Notification Endpoints
CRUD operations for user notifications
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.notification import NotificationCreate, NotificationUpdate, Notification, NotificationListResponse
from app.models.user import User as UserModel
from app.models.notification import Notification as NotificationModel

router = APIRouter()


@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new notification"""
    new_notification = NotificationModel(
        id=str(uuid.uuid4()),
        title=notification_data.title,
        message=notification_data.message,
        notification_type=notification_data.notification_type,
        entity_type=notification_data.entity_type,
        entity_id=notification_data.entity_id,
        action_url=notification_data.action_url,
        is_read=False,
        user_id=notification_data.user_id,
        organization_id=current_user.organization_id
    )
    
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    
    return new_notification


@router.get("/", response_model=NotificationListResponse)
def get_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get notifications for the current user"""
    # Build query
    query = db.query(NotificationModel).filter(
        NotificationModel.user_id == current_user.id,
        NotificationModel.organization_id == current_user.organization_id
    )
    
    # Apply filters
    if is_read is not None:
        query = query.filter(NotificationModel.is_read == is_read)
    
    # Get total count
    total = query.count()
    
    # Get unread count
    unread_count = db.query(NotificationModel).filter(
        NotificationModel.user_id == current_user.id,
        NotificationModel.is_read == False
    ).count()
    
    # Get paginated results
    notifications = query.order_by(NotificationModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "notifications": notifications,
        "total": total,
        "unread_count": unread_count
    }


@router.get("/{notification_id}", response_model=Notification)
def get_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific notification"""
    notification = db.query(NotificationModel).filter(
        NotificationModel.id == notification_id,
        NotificationModel.user_id == current_user.id,
        NotificationModel.organization_id == current_user.organization_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return notification


@router.put("/{notification_id}/read", response_model=Notification)
def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Mark a notification as read"""
    notification = db.query(NotificationModel).filter(
        NotificationModel.id == notification_id,
        NotificationModel.user_id == current_user.id,
        NotificationModel.organization_id == current_user.organization_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    
    db.commit()
    db.refresh(notification)
    
    return notification


@router.put("/mark-all-read", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Mark all notifications as read for the current user"""
    db.query(NotificationModel).filter(
        NotificationModel.user_id == current_user.id,
        NotificationModel.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })
    
    db.commit()
    
    return None


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a notification"""
    notification = db.query(NotificationModel).filter(
        NotificationModel.id == notification_id,
        NotificationModel.user_id == current_user.id,
        NotificationModel.organization_id == current_user.organization_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    db.delete(notification)
    db.commit()
    
    return None
