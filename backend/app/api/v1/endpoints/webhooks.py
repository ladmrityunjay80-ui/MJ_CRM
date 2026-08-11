"""
Webhook Endpoints
CRUD operations for webhook management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
import httpx
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.webhook import WebhookCreate, WebhookUpdate, Webhook, WebhookListResponse, WebhookLogListResponse
from app.models.user import User as UserModel
from app.models.webhook import Webhook as WebhookModel, WebhookLog as WebhookLogModel

router = APIRouter()


@router.post("/", response_model=Webhook, status_code=status.HTTP_201_CREATED)
def create_webhook(
    webhook_data: WebhookCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new webhook"""
    new_webhook = WebhookModel(
        id=str(uuid.uuid4()),
        name=webhook_data.name,
        description=webhook_data.description,
        url=str(webhook_data.url),
        method=webhook_data.method,
        headers=json.dumps(webhook_data.headers) if webhook_data.headers else None,
        secret=webhook_data.secret,
        events=json.dumps(webhook_data.events),
        is_active=True,
        organization_id=current_user.organization_id,
        created_by_id=current_user.id
    )
    
    db.add(new_webhook)
    db.commit()
    db.refresh(new_webhook)
    
    return new_webhook


@router.get("/", response_model=WebhookListResponse)
def get_webhooks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all webhooks with filtering and pagination"""
    # Build query
    query = db.query(WebhookModel).filter(WebhookModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(WebhookModel.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    webhooks = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "webhooks": webhooks,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{webhook_id}", response_model=Webhook)
def get_webhook(
    webhook_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific webhook"""
    webhook = db.query(WebhookModel).filter(
        WebhookModel.id == webhook_id,
        WebhookModel.organization_id == current_user.organization_id
    ).first()
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    
    return webhook


@router.put("/{webhook_id}", response_model=Webhook)
def update_webhook(
    webhook_id: str,
    webhook_data: WebhookUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a webhook"""
    webhook = db.query(WebhookModel).filter(
        WebhookModel.id == webhook_id,
        WebhookModel.organization_id == current_user.organization_id
    ).first()
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    
    # Update webhook fields
    update_data = webhook_data.model_dump(exclude_unset=True)
    
    if "url" in update_data and update_data["url"] is not None:
        update_data["url"] = str(update_data["url"])
    
    if "headers" in update_data and update_data["headers"] is not None:
        update_data["headers"] = json.dumps(update_data["headers"])
    
    if "events" in update_data and update_data["events"] is not None:
        update_data["events"] = json.dumps(update_data["events"])
    
    for field, value in update_data.items():
        setattr(webhook, field, value)
    
    db.commit()
    db.refresh(webhook)
    
    return webhook


@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_webhook(
    webhook_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a webhook"""
    webhook = db.query(WebhookModel).filter(
        WebhookModel.id == webhook_id,
        WebhookModel.organization_id == current_user.organization_id
    ).first()
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    
    db.delete(webhook)
    db.commit()
    
    return None


@router.post("/{webhook_id}/test", response_model=dict)
async def trigger_webhook_test(
    webhook_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Test a webhook by sending a test payload"""
    webhook = db.query(WebhookModel).filter(
        WebhookModel.id == webhook_id,
        WebhookModel.organization_id == current_user.organization_id
    ).first()
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    
    # Prepare test payload
    test_payload = {
        "event": "test",
        "timestamp": "2026-08-11T09:32:00Z",
        "data": {
            "message": "This is a test webhook payload"
        }
    }
    
    # Prepare headers
    headers = {"Content-Type": "application/json"}
    if webhook.headers:
        headers.update(json.loads(webhook.headers))
    
    # Send test request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=webhook.method,
                url=webhook.url,
                json=test_payload,
                headers=headers,
                timeout=10.0
            )
            
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "response": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/{webhook_id}/logs", response_model=WebhookLogListResponse)
def get_webhook_logs(
    webhook_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get webhook execution logs"""
    # Verify webhook belongs to organization
    webhook = db.query(WebhookModel).filter(
        WebhookModel.id == webhook_id,
        WebhookModel.organization_id == current_user.organization_id
    ).first()
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    
    # Build query
    query = db.query(WebhookLogModel).filter(WebhookLogModel.webhook_id == webhook_id)
    
    # Apply filters
    if status:
        query = query.filter(WebhookLogModel.status == status)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    logs = query.order_by(WebhookLogModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "logs": logs,
        "total": total,
        "page": page,
        "page_size": page_size
    }
