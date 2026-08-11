"""
Email Model
Represents email communications in the CRM
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class EmailStatus(str, enum.Enum):
    """Email delivery status"""
    DRAFT = "draft"
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    BOUNCED = "bounced"
    FAILED = "failed"


class Email(Base, TimestampMixin):
    """Email model for CRM communications"""
    
    __tablename__ = "emails"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    
    # Email details
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    body_html = Column(Text, nullable=True)
    
    # Recipients
    to_email = Column(String, nullable=False, index=True)
    to_name = Column(String, nullable=True)
    cc_email = Column(String, nullable=True)
    bcc_email = Column(String, nullable=True)
    
    # Sender
    from_email = Column(String, nullable=False)
    from_name = Column(String, nullable=True)
    
    # Email status
    status = Column(String, default=EmailStatus.DRAFT)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    
    # Tracking
    tracking_id = Column(String, nullable=True, unique=True, index=True)
    opened_count = Column(String, nullable=False, default="0")
    clicked_count = Column(String, nullable=False, default="0")
    
    # Related entities
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True, index=True)
    contact_id = Column(String, ForeignKey("contacts.id"), nullable=True, index=True)
    deal_id = Column(String, ForeignKey("deals.id"), nullable=True, index=True)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Template
    template_id = Column(String, nullable=True)
    
    # Relationships
    lead = relationship("Lead", back_populates="emails")
    contact = relationship("Contact", back_populates="emails")
    deal = relationship("Deal", back_populates="emails")
    organization = relationship("Organization", back_populates="emails")
    created_by = relationship("User", foreign_keys=[created_by_id])
    
    def __repr__(self):
        return f"<Email(id={self.id}, subject={self.subject}, to={self.to_email}, status={self.status})>"


class EmailTemplate(Base, TimestampMixin):
    """Email template for reusable email content"""
    
    __tablename__ = "email_templates"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    body_html = Column(Text, nullable=True)
    
    # Template metadata
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # welcome, follow-up, newsletter, etc.
    variables = Column(Text, nullable=True)  # JSON string of available variables
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<EmailTemplate(id={self.id}, name={self.name}, category={self.category})>"
