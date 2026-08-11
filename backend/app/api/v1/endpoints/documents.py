"""
Document Endpoints
CRUD operations for document management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import os
from datetime import datetime
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.document import DocumentCreate, DocumentUpdate, Document, DocumentListResponse
from app.models.user import User as UserModel
from app.models.document import Document as DocumentModel
from app.core.config import settings

router = APIRouter()

# Ensure upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=Document, status_code=status.HTTP_201_CREATED)
def create_document(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    description: Optional[str] = None,
    document_type: str = "other",
    lead_id: Optional[str] = None,
    contact_id: Optional[str] = None,
    deal_id: Optional[str] = None,
    company_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Upload and create a new document"""
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Create document record
    new_document = DocumentModel(
        id=str(uuid.uuid4()),
        name=name or file.filename,
        description=description,
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file.content_type or "application/octet-stream",
        document_type=document_type,
        storage_provider="local",
        storage_key=unique_filename,
        lead_id=lead_id,
        contact_id=contact_id,
        deal_id=deal_id,
        company_id=company_id,
        organization_id=current_user.organization_id,
        uploaded_by_id=current_user.id
    )
    
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    return new_document


@router.get("/", response_model=DocumentListResponse)
def get_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    document_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all documents with filtering and pagination"""
    # Build query
    query = db.query(DocumentModel).filter(DocumentModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if document_type:
        query = query.filter(DocumentModel.document_type == document_type)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    documents = query.order_by(DocumentModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "documents": documents,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{document_id}", response_model=Document)
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific document"""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.organization_id == current_user.organization_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document


@router.put("/{document_id}", response_model=Document)
def update_document(
    document_id: str,
    document_data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a document"""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.organization_id == current_user.organization_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Update document fields
    update_data = document_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(document, field, value)
    
    db.commit()
    db.refresh(document)
    
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a document"""
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.organization_id == current_user.organization_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file from storage
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.delete(document)
    db.commit()
    
    return None


@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Download a document file"""
    from fastapi.responses import FileResponse
    
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id,
        DocumentModel.organization_id == current_user.organization_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return FileResponse(
        document.file_path,
        media_type=document.file_type,
        filename=document.file_name
    )
