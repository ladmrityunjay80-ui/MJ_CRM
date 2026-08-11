"""
Permission Schemas
Pydantic models for permission request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.permission import PermissionResource, PermissionAction


class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    resource: PermissionResource
    action: PermissionAction
    scope: Optional[str] = None


class PermissionCreate(PermissionBase):
    """Schema for creating a permission"""
    pass


class PermissionUpdate(BaseModel):
    """Schema for updating a permission"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    resource: Optional[PermissionResource] = None
    action: Optional[PermissionAction] = None
    scope: Optional[str] = None
    is_active: Optional[bool] = None


class Permission(PermissionBase):
    """Schema for permission response"""
    id: str
    is_active: bool
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RolePermissionBase(BaseModel):
    """Base role permission schema"""
    role: str = Field(..., min_length=1)
    permission_id: str


class RolePermissionCreate(RolePermissionBase):
    """Schema for creating a role permission"""
    pass


class RolePermission(RolePermissionBase):
    """Schema for role permission response"""
    id: str
    organization_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PermissionListResponse(BaseModel):
    """Schema for permission list response"""
    permissions: list[Permission]
    total: int
    page: int
    page_size: int


class RolePermissionListResponse(BaseModel):
    """Schema for role permission list response"""
    role_permissions: list[RolePermission]
    total: int
    page: int
    page_size: int


class UserPermissionsResponse(BaseModel):
    """Schema for user permissions response"""
    permissions: list[str]  # List of permission names
    role: str
