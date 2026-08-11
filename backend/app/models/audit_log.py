"""
Audit Log Model
Tracks all system changes for compliance and security
"""

from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class AuditAction(str, enum.Enum):
    """Types of audit actions"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    BULK_DELETE = "bulk_delete"
    BULK_UPDATE = "bulk_update"
    PERMISSION_CHANGE = "permission_change"
    SETTINGS_CHANGE = "settings_change"


class AuditLog(Base, TimestampMixin):
    """Audit log model for tracking system changes"""
    
    __tablename__ = "audit_logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    
    # Action details
    action = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False, index=True)  # lead, contact, deal, etc.
    entity_id = Column(String, nullable=True, index=True)
    
    # Change details
    old_values = Column(Text, nullable=True)  # JSON string of old values
    new_values = Column(Text, nullable=True)  # JSON string of new values
    description = Column(Text, nullable=True)
    
    # User and context
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    user_email = Column(String, nullable=False)
    user_name = Column(String, nullable=True)
    
    # Request context
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Relationships
    user = relationship("User")
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, entity_type={self.entity_type}, user_id={self.user_id})>"
