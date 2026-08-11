"""
Contact Endpoints
CRUD operations for contacts
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.contact import ContactCreate, ContactUpdate, Contact, ContactListResponse
from app.models.user import User as UserModel
from app.models.contact import Contact as ContactModel

router = APIRouter()


@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new contact"""
    contact_dict = contact_data.model_dump(exclude={"tags"})
    new_contact = ContactModel(
        id=str(uuid.uuid4()),
        **contact_dict,
        organization_id=current_user.organization_id,
        created_by_id=current_user.id,
        tags=json.dumps(contact_data.tags) if contact_data.tags else None
    )
    
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    
    return new_contact


@router.get("/", response_model=ContactListResponse)
def get_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    company_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all contacts with filtering and pagination"""
    # Build query
    query = db.query(ContactModel).filter(ContactModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if company_id:
        query = query.filter(ContactModel.company_id == company_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    contacts = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "contacts": contacts,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{contact_id}", response_model=Contact)
def get_contact(
    contact_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific contact"""
    contact = db.query(ContactModel).filter(
        ContactModel.id == contact_id,
        ContactModel.organization_id == current_user.organization_id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    return contact


@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: str,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a contact"""
    contact = db.query(ContactModel).filter(
        ContactModel.id == contact_id,
        ContactModel.organization_id == current_user.organization_id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Update contact fields
    update_data = contact_data.model_dump(exclude_unset=True)
    if "tags" in update_data:
        update_data["tags"] = json.dumps(update_data["tags"]) if update_data["tags"] else None
    
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a contact"""
    contact = db.query(ContactModel).filter(
        ContactModel.id == contact_id,
        ContactModel.organization_id == current_user.organization_id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()
    
    return None
