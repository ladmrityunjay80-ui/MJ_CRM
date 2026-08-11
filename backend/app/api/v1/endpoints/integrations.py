"""
Integration Endpoints
CRUD operations for third-party integrations
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from datetime import datetime
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.integration import IntegrationCreate, IntegrationUpdate, Integration, IntegrationListResponse
from app.models.user import User as UserModel
from app.models.integration import Integration as IntegrationModel

router = APIRouter()


@router.post("/", response_model=Integration, status_code=status.HTTP_201_CREATED)
def create_integration(
    integration_data: IntegrationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new integration"""
    new_integration = IntegrationModel(
        id=str(uuid.uuid4()),
        name=integration_data.name,
        provider=integration_data.provider,
        description=integration_data.description,
        config=json.dumps(integration_data.config) if integration_data.config else None,
        api_key=integration_data.api_key,
        webhook_url=integration_data.webhook_url,
        status="pending",
        organization_id=current_user.organization_id,
        created_by_id=current_user.id
    )
    
    db.add(new_integration)
    db.commit()
    db.refresh(new_integration)
    
    return new_integration


@router.get("/", response_model=IntegrationListResponse)
def get_integrations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    provider: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get integrations with filtering and pagination"""
    # Build query
    query = db.query(IntegrationModel).filter(
        IntegrationModel.organization_id == current_user.organization_id
    )
    
    # Apply filters
    if provider:
        query = query.filter(IntegrationModel.provider == provider)
    if status:
        query = query.filter(IntegrationModel.status == status)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    integrations = query.order_by(IntegrationModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "integrations": integrations,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{integration_id}", response_model=Integration)
def get_integration(
    integration_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific integration"""
    integration = db.query(IntegrationModel).filter(
        IntegrationModel.id == integration_id,
        IntegrationModel.organization_id == current_user.organization_id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    return integration


@router.put("/{integration_id}", response_model=Integration)
def update_integration(
    integration_id: str,
    integration_data: IntegrationUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update an integration"""
    integration = db.query(IntegrationModel).filter(
        IntegrationModel.id == integration_id,
        IntegrationModel.organization_id == current_user.organization_id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    # Update integration fields
    update_data = integration_data.model_dump(exclude_unset=True)
    
    if "config" in update_data and update_data["config"] is not None:
        update_data["config"] = json.dumps(update_data["config"])
    
    for field, value in update_data.items():
        setattr(integration, field, value)
    
    db.commit()
    db.refresh(integration)
    
    return integration


@router.delete("/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_integration(
    integration_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete an integration"""
    integration = db.query(IntegrationModel).filter(
        IntegrationModel.id == integration_id,
        IntegrationModel.organization_id == current_user.organization_id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    db.delete(integration)
    db.commit()
    
    return None


@router.post("/{integration_id}/sync", response_model=Integration)
def sync_integration(
    integration_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Trigger integration sync"""
    integration = db.query(IntegrationModel).filter(
        IntegrationModel.id == integration_id,
        IntegrationModel.organization_id == current_user.organization_id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    # Update last sync time
    integration.last_sync_at = datetime.utcnow()
    integration.status = "active"
    
    db.commit()
    db.refresh(integration)
    
    # In a real implementation, this would trigger an async sync job
    return integration


@router.get("/providers/available")
def get_available_providers():
    """Get list of available integration providers"""
    providers = [
        {
            "id": "slack",
            "name": "Slack",
            "description": "Team communication and notifications",
            "icon": "slack",
            "features": ["notifications", "team_updates", "alerts"]
        },
        {
            "id": "google",
            "name": "Google Workspace",
            "description": "Email, calendar, and document integration",
            "icon": "google",
            "features": ["email", "calendar", "documents"]
        },
        {
            "id": "salesforce",
            "name": "Salesforce",
            "description": "CRM data synchronization",
            "icon": "salesforce",
            "features": ["contact_sync", "deal_sync", "lead_sync"]
        },
        {
            "id": "hubspot",
            "name": "HubSpot",
            "description": "Marketing and sales automation",
            "icon": "hubspot",
            "features": ["marketing", "sales", "service"]
        },
        {
            "id": "mailchimp",
            "name": "Mailchimp",
            "description": "Email marketing campaigns",
            "icon": "mailchimp",
            "features": ["email_campaigns", "audience_management"]
        }
    ]
    
    return {"providers": providers}
