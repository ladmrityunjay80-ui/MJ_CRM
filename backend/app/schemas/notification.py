"""
Notification Schemas
Pydantic models for notification request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.notification import NotificationType


class NotificationBase(BaseModel):
    """Base notification schema"""
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)
    notification_type: NotificationType
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    action_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    """Schema for creating a notification"""
    user_id: str


class NotificationUpdate(BaseModel):
    """Schema for updating a notification"""
    is_read: Optional[bool] = None


class Notification(NotificationBase):
    """Schema for notification response"""
    id: str
    is_read: bool
    read_at: Optional[datetime] = None
    user_id: str
    organization_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class NotificationListResponse(BaseModel):
    """Schema for notification list response"""
    notifications: list[Notification]
    total: int
    unread_count: int
