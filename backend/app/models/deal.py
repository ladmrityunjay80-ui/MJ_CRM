"""
Deal Model
Represents sales opportunities/deals
"""

from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class DealStage(str, Enum):
    """Deal stage options - customizable per organization"""
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class Deal(Base, TimestampMixin):
    """Deal model"""
    
    __tablename__ = "deals"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Financials
    value = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    probability = Column(Integer, default=50, nullable=True)  # 0-100
    
    # Timeline
    expected_close_date = Column(Date, nullable=True)
    actual_close_date = Column(Date, nullable=True)
    
    # Stage
    stage = Column(SQLEnum(DealStage), default=DealStage.PROSPECTING, nullable=False, index=True)
    lost_reason = Column(Text, nullable=True)
    
    # Additional info
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags
    
    # Foreign Keys
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    assigned_to_id = Column(String, ForeignKey("users.id"), nullable=True)
    contact_id = Column(String, ForeignKey("contacts.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="deals")
    company = relationship("Company", back_populates="deals")
    assigned_to = relationship("User", back_populates="deals")
    contact = relationship("Contact")
    emails = relationship("Email", back_populates="deal")
    
    def __repr__(self):
        return f"<Deal(id={self.id}, name={self.name}, value={self.value}, stage={self.stage})>"
