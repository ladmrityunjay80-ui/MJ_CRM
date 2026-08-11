"""
Analytics Model
Represents analytics reports and dashboards
"""

from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class ReportType(str, enum.Enum):
    """Types of analytics reports"""
    SALES_PIPELINE = "sales_pipeline"
    LEAD_CONVERSION = "lead_conversion"
    REVENUE = "revenue"
    ACTIVITY = "activity"
    TEAM_PERFORMANCE = "team_performance"
    CUSTOM = "custom"


class Report(Base, TimestampMixin):
    """Analytics report model"""
    
    __tablename__ = "reports"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Report configuration
    report_type = Column(String, nullable=False)
    config = Column(Text, nullable=True)  # JSON string for report configuration
    
    # Schedule
    is_scheduled = Column(String, nullable=False, default="false")
    schedule_frequency = Column(String, nullable=True)  # daily, weekly, monthly
    schedule_day = Column(String, nullable=True)  # day of week/month
    schedule_time = Column(String, nullable=True)  # time of day
    
    # Last run
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    created_by = relationship("User")
    
    def __repr__(self):
        return f"<Report(id={self.id}, name={self.name}, type={self.report_type})>"


class Dashboard(Base, TimestampMixin):
    """Dashboard model for organizing reports"""
    
    __tablename__ = "dashboards"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Dashboard layout
    layout = Column(Text, nullable=True)  # JSON string for widget layout
    
    # Organization
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    created_by = relationship("User")
    
    def __repr__(self):
        return f"<Dashboard(id={self.id}, name={self.name})>"
