"""
Lead Model
Represents potential customers in the sales pipeline
"""

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class LeadStatus(str, Enum):
    """Lead status options"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadSource(str, Enum):
    """Lead source options"""
    WEBSITE = "website"
    REFERRAL = "referral"
    COLD_CALL = "cold_call"
    COLD_EMAIL = "cold_email"
    SOCIAL_MEDIA = "social_media"
    EVENT = "event"
    PARTNER = "partner"
    OTHER = "other"


class Lead(Base, TimestampMixin):
    """Lead model"""
    
    __tablename__ = "leads"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    
    # Lead details
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW, nullable=False, index=True)
    source = Column(SQLEnum(LeadSource), default=LeadSource.OTHER, nullable=True)
    estimated_value = Column(Float, nullable=True)
    probability = Column(Integer, default=50, nullable=True)  # 0-100
    
    # Additional info
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags
    
    # Foreign Keys
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    assigned_to_id = Column(String, ForeignKey("users.id"), nullable=True)
    contact_id = Column(String, ForeignKey("contacts.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="leads")
    assigned_to = relationship("User", back_populates="leads")
    contact = relationship("Contact", back_populates="leads")
    emails = relationship("Email", back_populates="lead")
    
    def __repr__(self):
        return f"<Lead(id={self.id}, name={self.first_name} {self.last_name}, status={self.status})>"
