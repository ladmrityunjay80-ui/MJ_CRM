"""
Bulk Operations Endpoints
Handles bulk actions on CRM entities
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.lead import Lead
from app.models.contact import Contact
from app.models.company import Company
from app.models.deal import Deal
from app.models.activity import Activity

router = APIRouter()


class BulkDeleteRequest(BaseModel):
    """Request model for bulk delete"""
    ids: List[str]


class BulkUpdateRequest(BaseModel):
    """Request model for bulk update"""
    ids: List[str]
    updates: dict


class BulkActionRequest(BaseModel):
    """Request model for bulk actions"""
    ids: List[str]
    action: str
    params: dict = {}


@router.post("/leads/delete")
def bulk_delete_leads(
    request: BulkDeleteRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk delete leads"""
    leads = db.query(Lead).filter(
        Lead.id.in_(request.ids),
        Lead.organization_id == current_user.organization_id
    ).all()
    
    if not leads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No leads found"
        )
    
    for lead in leads:
        db.delete(lead)
    
    db.commit()
    
    return {"deleted": len(leads)}


@router.post("/leads/update")
def bulk_update_leads(
    request: BulkUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk update leads"""
    leads = db.query(Lead).filter(
        Lead.id.in_(request.ids),
        Lead.organization_id == current_user.organization_id
    ).all()
    
    if not leads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No leads found"
        )
    
    updated_count = 0
    for lead in leads:
        for field, value in request.updates.items():
            if hasattr(lead, field):
                setattr(lead, field, value)
                updated_count += 1
    
    db.commit()
    
    return {"updated": len(leads), "fields_updated": updated_count}


@router.post("/leads/action")
def bulk_action_leads(
    request: BulkActionRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk action on leads"""
    leads = db.query(Lead).filter(
        Lead.id.in_(request.ids),
        Lead.organization_id == current_user.organization_id
    ).all()
    
    if not leads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No leads found"
        )
    
    if request.action == "convert_to_contact":
        # Convert leads to contacts
        from app.models.contact import Contact
        import uuid
        
        for lead in leads:
            new_contact = Contact(
                id=str(uuid.uuid4()),
                first_name=lead.first_name,
                last_name=lead.last_name,
                email=lead.email,
                phone=lead.phone,
                organization_id=current_user.organization_id,
                created_by_id=current_user.id
            )
            db.add(new_contact)
            lead.status = "converted"
        
        db.commit()
        return {"action": "converted_to_contact", "processed": len(leads)}
    
    elif request.action == "change_status":
        new_status = request.params.get("status")
        if new_status:
            for lead in leads:
                lead.status = new_status
            db.commit()
            return {"action": "status_changed", "processed": len(leads), "new_status": new_status}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid action"
    )


@router.post("/contacts/delete")
def bulk_delete_contacts(
    request: BulkDeleteRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk delete contacts"""
    contacts = db.query(Contact).filter(
        Contact.id.in_(request.ids),
        Contact.organization_id == current_user.organization_id
    ).all()
    
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No contacts found"
        )
    
    for contact in contacts:
        db.delete(contact)
    
    db.commit()
    
    return {"deleted": len(contacts)}


@router.post("/contacts/update")
def bulk_update_contacts(
    request: BulkUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk update contacts"""
    contacts = db.query(Contact).filter(
        Contact.id.in_(request.ids),
        Contact.organization_id == current_user.organization_id
    ).all()
    
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No contacts found"
        )
    
    updated_count = 0
    for contact in contacts:
        for field, value in request.updates.items():
            if hasattr(contact, field):
                setattr(contact, field, value)
                updated_count += 1
    
    db.commit()
    
    return {"updated": len(contacts), "fields_updated": updated_count}


@router.post("/deals/delete")
def bulk_delete_deals(
    request: BulkDeleteRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk delete deals"""
    deals = db.query(Deal).filter(
        Deal.id.in_(request.ids),
        Deal.organization_id == current_user.organization_id
    ).all()
    
    if not deals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No deals found"
        )
    
    for deal in deals:
        db.delete(deal)
    
    db.commit()
    
    return {"deleted": len(deals)}


@router.post("/deals/update")
def bulk_update_deals(
    request: BulkUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk update deals"""
    deals = db.query(Deal).filter(
        Deal.id.in_(request.ids),
        Deal.organization_id == current_user.organization_id
    ).all()
    
    if not deals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No deals found"
        )
    
    updated_count = 0
    for deal in deals:
        for field, value in request.updates.items():
            if hasattr(deal, field):
                setattr(deal, field, value)
                updated_count += 1
    
    db.commit()
    
    return {"updated": len(deals), "fields_updated": updated_count}


@router.post("/deals/action")
def bulk_action_deals(
    request: BulkActionRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk action on deals"""
    deals = db.query(Deal).filter(
        Deal.id.in_(request.ids),
        Deal.organization_id == current_user.organization_id
    ).all()
    
    if not deals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No deals found"
        )
    
    if request.action == "change_stage":
        new_stage = request.params.get("stage")
        if new_stage:
            for deal in deals:
                deal.stage = new_stage
            db.commit()
            return {"action": "stage_changed", "processed": len(deals), "new_stage": new_stage}
    
    elif request.action == "mark_won":
        for deal in deals:
            deal.stage = "won"
        db.commit()
        return {"action": "marked_won", "processed": len(deals)}
    
    elif request.action == "mark_lost":
        for deal in deals:
            deal.stage = "lost"
        db.commit()
        return {"action": "marked_lost", "processed": len(deals)}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid action"
    )


@router.post("/activities/delete")
def bulk_delete_activities(
    request: BulkDeleteRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk delete activities"""
    activities = db.query(Activity).filter(
        Activity.id.in_(request.ids),
        Activity.organization_id == current_user.organization_id
    ).all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found"
        )
    
    for activity in activities:
        db.delete(activity)
    
    db.commit()
    
    return {"deleted": len(activities)}


@router.post("/activities/update")
def bulk_update_activities(
    request: BulkUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk update activities"""
    activities = db.query(Activity).filter(
        Activity.id.in_(request.ids),
        Activity.organization_id == current_user.organization_id
    ).all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found"
        )
    
    updated_count = 0
    for activity in activities:
        for field, value in request.updates.items():
            if hasattr(activity, field):
                setattr(activity, field, value)
                updated_count += 1
    
    db.commit()
    
    return {"updated": len(activities), "fields_updated": updated_count}


@router.post("/activities/action")
def bulk_action_activities(
    request: BulkActionRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Bulk action on activities"""
    activities = db.query(Activity).filter(
        Activity.id.in_(request.ids),
        Activity.organization_id == current_user.organization_id
    ).all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found"
        )
    
    if request.action == "mark_completed":
        from datetime import datetime
        for activity in activities:
            activity.status = "completed"
            activity.completed_at = datetime.utcnow()
        db.commit()
        return {"action": "marked_completed", "processed": len(activities)}
    
    elif request.action == "mark_cancelled":
        for activity in activities:
            activity.status = "cancelled"
        db.commit()
        return {"action": "marked_cancelled", "processed": len(activities)}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid action"
    )
