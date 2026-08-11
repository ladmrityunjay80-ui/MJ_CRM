"""
Campaign Model
Represents email marketing campaigns
"""

from sqlalchemy import Column, String, Text, ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class CampaignStatus(str, enum.Enum):
    """Campaign status options"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class Campaign(Base, TimestampMixin):
    """Email campaign model"""
    
    __tablename__ = "campaigns"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Campaign details
    status = Column(String, default=CampaignStatus.DRAFT, nullable=False, index=True)
    
    # Email template
    template_id = Column(String, ForeignKey("email_templates.id"), nullable=True)
    content = Column(Text, nullable=True)  # HTML content
    
    # Targeting
    target_audience = Column(Text, nullable=True)  # JSON array of criteria
    recipient_count = Column(Integer, default=0)
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Statistics
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)
    bounced_count = Column(Integer, default=0)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    created_by = relationship("User")
    template = relationship("EmailTemplate")
    
    def __repr__(self):
        return f"<Campaign(id={self.id}, name={self.name}, status={self.status})>"


class CampaignRecipient(Base, TimestampMixin):
    """Campaign recipient tracking"""
    
    __tablename__ = "campaign_recipients"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False, index=True)
    
    # Recipient
    email = Column(String, nullable=False)
    recipient_type = Column(String, nullable=True)  # lead, contact, etc.
    recipient_id = Column(String, nullable=True)
    
    # Status
    status = Column(String, default="pending")  # pending, sent, delivered, opened, clicked, bounced
    sent_at = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Tracking
    tracking_id = Column(String, nullable=True, unique=True)
    
    # Relationships
    campaign = relationship("Campaign")
    
    def __repr__(self):
        return f"<CampaignRecipient(id={self.id}, email={self.email}, status={self.status})>"
