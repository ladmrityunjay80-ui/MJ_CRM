"""
Activity Model
Represents sales activities (calls, emails, meetings, notes)
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Integer, Boolean
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class ActivityType(str, Enum):
    """Activity type options"""
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    NOTE = "note"
    TASK = "task"
    SMS = "sms"
    OTHER = "other"


class ActivityStatus(str, Enum):
    """Activity status options"""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class Activity(Base, TimestampMixin):
    """Activity model"""
    
    __tablename__ = "activities"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    type = Column(SQLEnum(ActivityType), nullable=False, index=True)
    status = Column(SQLEnum(ActivityStatus), default=ActivityStatus.SCHEDULED, nullable=False)
    
    # Activity details
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)  # For meetings
    
    # Timeline
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Integer, nullable=True)  # For meetings/calls
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Reminder
    reminder_minutes_before = Column(Integer, nullable=True)
    reminder_sent = Column(Boolean, default=False, nullable=False)
    
    # Additional info
    notes = Column(Text, nullable=True)
    
    # Foreign Keys
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True)
    contact_id = Column(String, ForeignKey("contacts.id"), nullable=True)
    deal_id = Column(String, ForeignKey("deals.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    created_by = relationship("User", back_populates="activities")
    lead = relationship("Lead")
    contact = relationship("Contact")
    deal = relationship("Deal")
    
    def __repr__(self):
        return f"<Activity(id={self.id}, type={self.type}, subject={self.subject})>"
