"""
Permission Model
Represents granular permissions for RBAC
"""

from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class PermissionResource(str, enum.Enum):
    """Resources that can be accessed"""
    LEADS = "leads"
    CONTACTS = "contacts"
    COMPANIES = "companies"
    DEALS = "deals"
    ACTIVITIES = "activities"
    PRODUCTS = "products"
    WORKFLOWS = "workflows"
    EMAILS = "emails"
    ANALYTICS = "analytics"
    DOCUMENTS = "documents"
    WEBHOOKS = "webhooks"
    USERS = "users"
    ORGANIZATIONS = "organizations"
    SETTINGS = "settings"


class PermissionAction(str, enum.Enum):
    """Actions that can be performed"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    IMPORT = "import"
    MANAGE = "manage"


class Permission(Base, TimestampMixin):
    """Permission model for granular access control"""
    
    __tablename__ = "permissions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Permission details
    resource = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False, index=True)
    
    # Scope
    scope = Column(String, nullable=True)  # own, team, organization, all
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True, index=True)
    
    # Relationships
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name}, resource={self.resource}, action={self.action})>"


class RolePermission(Base, TimestampMixin):
    """Association between roles and permissions"""
    
    __tablename__ = "role_permissions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    role = Column(String, nullable=False, index=True)  # admin, manager, sales_rep, etc.
    permission_id = Column(String, ForeignKey("permissions.id"), nullable=False, index=True)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Relationships
    permission = relationship("Permission")
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<RolePermission(id={self.id}, role={self.role}, permission_id={self.permission_id})>"
