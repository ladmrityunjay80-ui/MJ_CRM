"""
Company Model
Represents customer companies/accounts
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Company(Base, TimestampMixin):
    """Company model"""
    
    __tablename__ = "companies"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    website = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    size = Column(String, nullable=True)  # e.g., "1-10", "11-50", "51-200", etc.
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    
    # Contact info
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # Additional info
    notes = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags
    logo_url = Column(String, nullable=True)
    
    # Foreign Keys
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="companies")
    contacts = relationship("Contact", back_populates="company")
    deals = relationship("Deal", back_populates="company")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name})>"
