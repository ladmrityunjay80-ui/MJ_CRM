"""
Audit Log Schemas
Pydantic models for audit log request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.audit_log import AuditAction


class AuditLogBase(BaseModel):
    """Base audit log schema"""
    action: AuditAction
    entity_type: str
    entity_id: Optional[str] = None
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log"""
    user_id: str
    user_email: str
    user_name: Optional[str] = None
    organization_id: str


class AuditLog(AuditLogBase):
    """Schema for audit log response"""
    id: str
    user_id: str
    user_email: str
    user_name: Optional[str] = None
    organization_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AuditLogListResponse(BaseModel):
    """Schema for audit log list response"""
    logs: list[AuditLog]
    total: int
    page: int
    page_size: int
