"""
Document Schemas
Pydantic models for document request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.document import DocumentType


class DocumentBase(BaseModel):
    """Base document schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    file_name: str = Field(..., min_length=1)
    file_size: int = Field(..., gt=0)
    file_type: str = Field(..., min_length=1)
    document_type: DocumentType


class DocumentCreate(DocumentBase):
    """Schema for creating a document"""
    lead_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    company_id: Optional[str] = None


class DocumentUpdate(BaseModel):
    """Schema for updating a document"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    document_type: Optional[DocumentType] = None


class Document(DocumentBase):
    """Schema for document response"""
    id: str
    file_path: str
    storage_provider: str
    storage_key: Optional[str] = None
    lead_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    company_id: Optional[str] = None
    organization_id: str
    uploaded_by_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DocumentListResponse(BaseModel):
    """Schema for document list response"""
    documents: list[Document]
    total: int
    page: int
    page_size: int
