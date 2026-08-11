"""
Organization Model
Represents companies/organizations using the CRM
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Organization(Base, TimestampMixin):
    """Organization model"""
    
    __tablename__ = "organizations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    industry = Column(String, nullable=True)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String, nullable=True)
    
    # Settings
    settings = Column(Text, nullable=True)  # JSON string for custom settings
    
    # Relationships
    users = relationship("User", back_populates="organization")
    companies = relationship("Company", back_populates="organization")
    contacts = relationship("Contact", back_populates="organization")
    leads = relationship("Lead", back_populates="organization")
    deals = relationship("Deal", back_populates="organization")
    activities = relationship("Activity", back_populates="organization")
    products = relationship("Product", back_populates="organization")
    workflows = relationship("Workflow", back_populates="organization")
    emails = relationship("Email", back_populates="organization")
    reports = relationship("Report", back_populates="organization")
    dashboards = relationship("Dashboard", back_populates="organization")
    documents = relationship("Document", back_populates="organization")
    webhooks = relationship("Webhook", back_populates="organization")
    notifications = relationship("Notification", back_populates="organization")
    permissions = relationship("Permission", back_populates="organization")
    role_permissions = relationship("RolePermission", back_populates="organization")
    campaigns = relationship("Campaign", back_populates="organization")
    audit_logs = relationship("AuditLog", back_populates="organization")
    comments = relationship("Comment", back_populates="organization")
    integrations = relationship("Integration", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name={self.name})>"
