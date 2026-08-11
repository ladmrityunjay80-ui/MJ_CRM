"""
Integration Model
Represents third-party integrations and connections
"""

from sqlalchemy import Column, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class IntegrationStatus(str, enum.Enum):
    """Integration status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"


class Integration(Base, TimestampMixin):
    """Integration model for third-party connections"""
    
    __tablename__ = "integrations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    provider = Column(String, nullable=False, index=True)  # slack, google, salesforce, etc.
    description = Column(Text, nullable=True)
    
    # Configuration
    config = Column(Text, nullable=True)  # JSON string of configuration
    api_key = Column(String, nullable=True)
    webhook_url = Column(String, nullable=True)
    
    # Status
    status = Column(String, default=IntegrationStatus.INACTIVE, nullable=False, index=True)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    created_by = relationship("User")
    
    def __repr__(self):
        return f"<Integration(id={self.id}, name={self.name}, provider={self.provider}, status={self.status})>"


class IntegrationLog(Base, TimestampMixin):
    """Integration log for tracking sync operations"""
    
    __tablename__ = "integration_logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    integration_id = Column(String, ForeignKey("integrations.id"), nullable=False, index=True)
    
    # Operation details
    operation = Column(String, nullable=False)  # sync, import, export, etc.
    status = Column(String, nullable=False)  # success, error, pending
    records_processed = Column(String, nullable=True)  # JSON string of record counts
    
    # Error details
    error_message = Column(Text, nullable=True)
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    integration = relationship("Integration")
    
    def __repr__(self):
        return f"<IntegrationLog(id={self.id}, operation={self.operation}, status={self.status})>"
