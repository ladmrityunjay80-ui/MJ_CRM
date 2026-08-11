"""
Campaign Schemas
Pydantic models for campaign request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.campaign import CampaignStatus


class CampaignBase(BaseModel):
    """Base campaign schema"""
    name: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    template_id: Optional[str] = None
    content: Optional[str] = None
    target_audience: Optional[dict] = None
    scheduled_at: Optional[datetime] = None


class CampaignCreate(CampaignBase):
    """Schema for creating a campaign"""
    pass


class CampaignUpdate(BaseModel):
    """Schema for updating a campaign"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    subject: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    template_id: Optional[str] = None
    content: Optional[str] = None
    target_audience: Optional[dict] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[CampaignStatus] = None


class Campaign(CampaignBase):
    """Schema for campaign response"""
    id: str
    status: CampaignStatus
    recipient_count: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    bounced_count: int
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    organization_id: str
    created_by_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CampaignRecipientBase(BaseModel):
    """Base campaign recipient schema"""
    email: str
    recipient_type: Optional[str] = None
    recipient_id: Optional[str] = None


class CampaignRecipientCreate(CampaignRecipientBase):
    """Schema for creating a campaign recipient"""
    campaign_id: str


class CampaignRecipient(CampaignRecipientBase):
    """Schema for campaign recipient response"""
    id: str
    campaign_id: str
    status: str
    sent_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    tracking_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CampaignListResponse(BaseModel):
    """Schema for campaign list response"""
    campaigns: List[Campaign]
    total: int
    page: int
    page_size: int


class CampaignStats(BaseModel):
    """Schema for campaign statistics"""
    total_recipients: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    bounced_count: int
    open_rate: float
    click_rate: float
    delivery_rate: float
