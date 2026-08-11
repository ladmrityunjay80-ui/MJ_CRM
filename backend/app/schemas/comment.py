"""
Comment Schemas
Pydantic models for comment request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class CommentBase(BaseModel):
    """Base comment schema"""
    content: str = Field(..., min_length=1)
    entity_type: str
    entity_id: str
    parent_id: Optional[str] = None
    mentions: Optional[List[str]] = None


class CommentCreate(CommentBase):
    """Schema for creating a comment"""
    pass


class CommentUpdate(BaseModel):
    """Schema for updating a comment"""
    content: Optional[str] = Field(None, min_length=1)
    mentions: Optional[List[str]] = None


class Comment(CommentBase):
    """Schema for comment response"""
    id: str
    organization_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CommentWithUser(Comment):
    """Schema for comment with user details"""
    user_name: Optional[str] = None
    user_email: Optional[str] = None


class CommentListResponse(BaseModel):
    """Schema for comment list response"""
    comments: List[CommentWithUser]
    total: int
    page: int
    page_size: int
