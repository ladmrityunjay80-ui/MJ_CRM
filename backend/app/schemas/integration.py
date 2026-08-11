"""
Integration Schemas
Pydantic models for integration request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.integration import IntegrationStatus


class IntegrationBase(BaseModel):
    """Base integration schema"""
    name: str = Field(..., min_length=1, max_length=200)
    provider: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    config: Optional[dict] = None
    api_key: Optional[str] = None
    webhook_url: Optional[str] = None


class IntegrationCreate(IntegrationBase):
    """Schema for creating an integration"""
    pass


class IntegrationUpdate(BaseModel):
    """Schema for updating an integration"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    config: Optional[dict] = None
    api_key: Optional[str] = None
    webhook_url: Optional[str] = None
    status: Optional[IntegrationStatus] = None


class Integration(IntegrationBase):
    """Schema for integration response"""
    id: str
    status: IntegrationStatus
    last_sync_at: Optional[datetime] = None
    organization_id: str
    created_by_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class IntegrationListResponse(BaseModel):
    """Schema for integration list response"""
    integrations: list[Integration]
    total: int
    page: int
    page_size: int


class IntegrationLogBase(BaseModel):
    """Base integration log schema"""
    operation: str
    status: str
    records_processed: Optional[dict] = None
    error_message: Optional[str] = None


class IntegrationLogCreate(IntegrationLogBase):
    """Schema for creating an integration log"""
    integration_id: str


class IntegrationLog(IntegrationLogBase):
    """Schema for integration log response"""
    id: str
    integration_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
