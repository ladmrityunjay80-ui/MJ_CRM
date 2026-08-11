"""
Notification Model
Represents user notifications
"""

from sqlalchemy import Column, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class NotificationType(str, enum.Enum):
    """Types of notifications"""
    LEAD_ASSIGNED = "lead_assigned"
    DEAL_UPDATED = "deal_updated"
    DEAL_WON = "deal_won"
    DEAL_LOST = "deal_lost"
    ACTIVITY_DUE = "activity_due"
    MENTION = "mention"
    COMMENT = "comment"
    SYSTEM = "system"


class Notification(Base, TimestampMixin):
    """Notification model for user notifications"""
    
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    
    # Notification details
    notification_type = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # Related entity
    entity_type = Column(String, nullable=True)  # lead, deal, activity, etc.
    entity_id = Column(String, nullable=True)
    action_url = Column(String, nullable=True)  # URL to navigate to
    
    # User
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Relationships
    user = relationship("User")
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, title={self.title}, user_id={self.user_id}, is_read={self.is_read})>"
