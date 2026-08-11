"""
Campaign Endpoints
CRUD operations for email marketing campaigns
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.campaign import CampaignCreate, CampaignUpdate, Campaign, CampaignListResponse, CampaignStats
from app.models.user import User as UserModel
from app.models.campaign import Campaign as CampaignModel, CampaignRecipient as CampaignRecipientModel

router = APIRouter()


@router.post("/", response_model=Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new email campaign"""
    new_campaign = CampaignModel(
        id=str(uuid.uuid4()),
        name=campaign_data.name,
        subject=campaign_data.subject,
        description=campaign_data.description,
        template_id=campaign_data.template_id,
        content=campaign_data.content,
        target_audience=str(campaign_data.target_audience) if campaign_data.target_audience else None,
        scheduled_at=campaign_data.scheduled_at,
        status="draft",
        organization_id=current_user.organization_id,
        created_by_id=current_user.id
    )
    
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    
    return new_campaign


@router.get("/", response_model=CampaignListResponse)
def get_campaigns(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all campaigns with filtering and pagination"""
    # Build query
    query = db.query(CampaignModel).filter(
        CampaignModel.organization_id == current_user.organization_id
    )
    
    # Apply filters
    if status:
        query = query.filter(CampaignModel.status == status)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    campaigns = query.order_by(CampaignModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "campaigns": campaigns,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(
    campaign_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific campaign"""
    campaign = db.query(CampaignModel).filter(
        CampaignModel.id == campaign_id,
        CampaignModel.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    return campaign


@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a campaign"""
    campaign = db.query(CampaignModel).filter(
        CampaignModel.id == campaign_id,
        CampaignModel.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Prevent updates if campaign is already sent
    if campaign.status in ["sending", "sent"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update a campaign that has been sent"
        )
    
    # Update campaign fields
    update_data = campaign_data.model_dump(exclude_unset=True)
    
    if "target_audience" in update_data and update_data["target_audience"] is not None:
        update_data["target_audience"] = str(update_data["target_audience"])
    
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a campaign"""
    campaign = db.query(CampaignModel).filter(
        CampaignModel.id == campaign_id,
        CampaignModel.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Prevent deletion if campaign is already sent
    if campaign.status in ["sending", "sent"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a campaign that has been sent"
        )
    
    db.delete(campaign)
    db.commit()
    
    return None


@router.post("/{campaign_id}/send", response_model=Campaign)
def send_campaign(
    campaign_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Send a campaign"""
    campaign = db.query(CampaignModel).filter(
        CampaignModel.id == campaign_id,
        CampaignModel.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    if campaign.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft campaigns can be sent"
        )
    
    # Update campaign status
    campaign.status = "sending"
    campaign.sent_at = datetime.utcnow()
    
    db.commit()
    db.refresh(campaign)
    
    # In a real implementation, this would trigger an async job to send emails
    # For now, we'll mark it as sent immediately
    campaign.status = "sent"
    campaign.sent_count = campaign.recipient_count
    campaign.delivered_count = campaign.recipient_count
    
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.get("/{campaign_id}/stats", response_model=CampaignStats)
def get_campaign_stats(
    campaign_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get campaign statistics"""
    campaign = db.query(CampaignModel).filter(
        CampaignModel.id == campaign_id,
        CampaignModel.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Calculate rates
    total_recipients = campaign.recipient_count or 1
    open_rate = (campaign.opened_count / total_recipients * 100) if total_recipients > 0 else 0
    click_rate = (campaign.clicked_count / total_recipients * 100) if total_recipients > 0 else 0
    delivery_rate = (campaign.delivered_count / total_recipients * 100) if total_recipients > 0 else 0
    
    return {
        "total_recipients": campaign.recipient_count,
        "sent_count": campaign.sent_count,
        "delivered_count": campaign.delivered_count,
        "opened_count": campaign.opened_count,
        "clicked_count": campaign.clicked_count,
        "bounced_count": campaign.bounced_count,
        "open_rate": round(open_rate, 2),
        "click_rate": round(click_rate, 2),
        "delivery_rate": round(delivery_rate, 2)
    }
