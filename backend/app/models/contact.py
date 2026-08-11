"""
Contact Model
Represents individual contacts at customer companies
"""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Contact(Base, TimestampMixin):
    """Contact model"""
    
    __tablename__ = "contacts"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    department = Column(String, nullable=True)
    
    # Social media
    linkedin = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    
    # Additional info
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags
    avatar_url = Column(String, nullable=True)
    
    # Foreign Keys
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="contacts")
    company = relationship("Company", back_populates="contacts")
    created_by = relationship("User", back_populates="contacts")
    leads = relationship("Lead", back_populates="contact")
    emails = relationship("Email", back_populates="contact")
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name={self.first_name} {self.last_name})>"
