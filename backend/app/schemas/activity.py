"""
Activity Schemas
Pydantic models for activity request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.activity import ActivityType, ActivityStatus


class ActivityBase(BaseModel):
    """Base activity schema"""
    type: ActivityType
    subject: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class ActivityCreate(ActivityBase):
    """Schema for creating an activity"""
    status: Optional[ActivityStatus] = ActivityStatus.SCHEDULED
    location: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    reminder_minutes_before: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None
    lead_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None


class ActivityUpdate(BaseModel):
    """Schema for updating an activity"""
    type: Optional[ActivityType] = None
    status: Optional[ActivityStatus] = None
    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    completed_at: Optional[datetime] = None
    reminder_minutes_before: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None
    lead_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None


class Activity(ActivityBase):
    """Schema for activity response"""
    id: str
    status: ActivityStatus
    location: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    completed_at: Optional[datetime] = None
    reminder_minutes_before: Optional[int] = None
    reminder_sent: bool
    notes: Optional[str] = None
    organization_id: str
    created_by_id: Optional[str] = None
    lead_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ActivityListResponse(BaseModel):
    """Schema for activity list response"""
    activities: list[Activity]
    total: int
    page: int
    page_size: int
