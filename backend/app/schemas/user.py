"""
User Schemas
Pydantic models for user request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None
    role: UserRole = UserRole.SALES_REP


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=8)
    organization_id: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None


class UserInDB(UserBase):
    """Schema for user in database"""
    id: str
    hashed_password: str
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    """Schema for user response"""
    id: str
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: User


class TokenData(BaseModel):
    """Schema for token data"""
    email: Optional[str] = None
    user_id: Optional[str] = None


class UserListResponse(BaseModel):
    """Schema for paginated user list response"""
    users: list[User]
    total: int
    page: int
    page_size: int
