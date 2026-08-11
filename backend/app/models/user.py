"""
User Model
Represents users in the system with role-based access
"""

from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class UserRole(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    MANAGER = "manager"
    SALES_REP = "sales_rep"
    EXECUTIVE = "executive"
    OWNER = "owner"
    INVESTOR = "investor"


class User(Base, TimestampMixin):
    """User model"""
    
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.SALES_REP, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    avatar_url = Column(String, nullable=True)
    
    # Foreign Keys
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    leads = relationship("Lead", back_populates="assigned_to")
    contacts = relationship("Contact", back_populates="created_by")
    deals = relationship("Deal", back_populates="assigned_to")
    activities = relationship("Activity", back_populates="created_by")
    notifications = relationship("Notification", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
