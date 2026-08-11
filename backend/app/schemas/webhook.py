"""
Webhook Schemas
Pydantic models for webhook request/response validation
"""

from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
import json
from app.models.webhook import WebhookEvent


class WebhookBase(BaseModel):
    """Base webhook schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    url: HttpUrl
    method: str = Field(default="POST", pattern="^(POST|PUT|PATCH)$")
    headers: Optional[dict[str, str]] = None
    secret: Optional[str] = None
    events: List[str] = Field(..., min_length=1)


class WebhookCreate(WebhookBase):
    """Schema for creating a webhook"""
    pass


class WebhookUpdate(BaseModel):
    """Schema for updating a webhook"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    method: Optional[str] = Field(None, pattern="^(POST|PUT|PATCH)$")
    headers: Optional[dict[str, str]] = None
    secret: Optional[str] = None
    events: Optional[List[str]] = None
    is_active: Optional[bool] = None


class Webhook(WebhookBase):
    """Schema for webhook response"""
    id: str
    is_active: bool
    organization_id: str
    created_by_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    @field_validator('events', mode='before')
    @classmethod
    def parse_events(cls, v):
        """Parse JSON string to list if needed"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
    
    model_config = ConfigDict(from_attributes=True)


class WebhookLog(BaseModel):
    """Schema for webhook log response"""
    id: str
    webhook_id: str
    event_type: str
    request_url: str
    request_method: str
    request_headers: Optional[dict[str, str]] = None
    request_body: Optional[dict] = None
    response_status: Optional[str] = None
    response_headers: Optional[dict[str, str]] = None
    response_body: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    retry_count: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class WebhookListResponse(BaseModel):
    """Schema for webhook list response"""
    webhooks: List[Webhook]
    total: int
    page: int
    page_size: int


class WebhookLogListResponse(BaseModel):
    """Schema for webhook log list response"""
    logs: List[WebhookLog]
    total: int
    page: int
    page_size: int
