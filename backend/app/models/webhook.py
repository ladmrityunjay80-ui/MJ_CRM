"""
Webhook Model
Represents webhooks for external integrations
"""

from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class WebhookEvent(str, enum.Enum):
    """Types of webhook events"""
    LEAD_CREATED = "lead.created"
    LEAD_UPDATED = "lead.updated"
    LEAD_DELETED = "lead.deleted"
    CONTACT_CREATED = "contact.created"
    CONTACT_UPDATED = "contact.updated"
    CONTACT_DELETED = "contact.deleted"
    DEAL_CREATED = "deal.created"
    DEAL_UPDATED = "deal.updated"
    DEAL_DELETED = "deal.deleted"
    ACTIVITY_CREATED = "activity.created"
    ACTIVITY_UPDATED = "activity.updated"
    ACTIVITY_DELETED = "activity.deleted"


class Webhook(Base, TimestampMixin):
    """Webhook model for external integrations"""
    
    __tablename__ = "webhooks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Webhook configuration
    url = Column(String, nullable=False)
    method = Column(String, nullable=False, default="POST")  # POST, PUT, PATCH
    headers = Column(Text, nullable=True)  # JSON string for custom headers
    secret = Column(String, nullable=True)  # Secret for signature verification
    
    # Event subscriptions
    events = Column(Text, nullable=False)  # JSON array of subscribed events
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    created_by = relationship("User")
    
    def __repr__(self):
        return f"<Webhook(id={self.id}, name={self.name}, url={self.url})>"


class WebhookLog(Base, TimestampMixin):
    """Webhook execution log"""
    
    __tablename__ = "webhook_logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    webhook_id = Column(String, ForeignKey("webhooks.id"), nullable=False, index=True)
    
    # Request details
    event_type = Column(String, nullable=False)
    request_url = Column(String, nullable=False)
    request_method = Column(String, nullable=False)
    request_headers = Column(Text, nullable=True)  # JSON string
    request_body = Column(Text, nullable=True)  # JSON string
    
    # Response details
    response_status = Column(String, nullable=True)
    response_headers = Column(Text, nullable=True)  # JSON string
    response_body = Column(Text, nullable=True)
    
    # Execution details
    status = Column(String, nullable=False)  # success, failed, pending
    error_message = Column(Text, nullable=True)
    retry_count = Column(String, nullable=False, default="0")
    
    # Relationships
    webhook = relationship("Webhook")
    
    def __repr__(self):
        return f"<WebhookLog(id={self.id}, webhook_id={self.webhook_id}, event_type={self.event_type}, status={self.status})>"
