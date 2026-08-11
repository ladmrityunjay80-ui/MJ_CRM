"""
Document Model
Represents documents and files in the CRM
"""

from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
import enum


class DocumentType(str, enum.Enum):
    """Types of documents"""
    CONTRACT = "contract"
    PROPOSAL = "proposal"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    REPORT = "report"
    PRESENTATION = "presentation"
    SPREADSHEET = "spreadsheet"
    IMAGE = "image"
    PDF = "pdf"
    OTHER = "other"


class Document(Base, TimestampMixin):
    """Document model for file storage"""
    
    __tablename__ = "documents"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # File details
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Path to stored file
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_type = Column(String, nullable=False)  # MIME type
    document_type = Column(String, nullable=False)  # Document category
    
    # Storage
    storage_provider = Column(String, nullable=False, default="local")  # local, s3, etc.
    storage_key = Column(String, nullable=True)  # Key for cloud storage
    
    # Related entities
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True, index=True)
    contact_id = Column(String, ForeignKey("contacts.id"), nullable=True, index=True)
    deal_id = Column(String, ForeignKey("deals.id"), nullable=True, index=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True, index=True)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False, index=True)
    uploaded_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    lead = relationship("Lead")
    contact = relationship("Contact")
    deal = relationship("Deal")
    company = relationship("Company")
    organization = relationship("Organization")
    uploaded_by = relationship("User")
    
    def __repr__(self):
        return f"<Document(id={self.id}, name={self.name}, file_name={self.file_name})>"
