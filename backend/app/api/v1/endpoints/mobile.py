"""
Mobile API Endpoints
Optimized endpoints for mobile applications with lightweight responses
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.lead import Lead
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.activity import Activity

router = APIRouter()


@router.get("/dashboard")
def get_mobile_dashboard(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get mobile-optimized dashboard summary"""
    # Get counts
    lead_count = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id
    ).count()
    
    contact_count = db.query(Contact).filter(
        Contact.organization_id == current_user.organization_id
    ).count()
    
    deal_count = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id
    ).count()
    
    # Get today's activities
    today = datetime.utcnow().date()
    today_activities = db.query(Activity).filter(
        Activity.organization_id == current_user.organization_id,
        Activity.scheduled_at >= today,
        Activity.scheduled_at < today + timedelta(days=1)
    ).count()
    
    # Get open deals value
    pipeline_value = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["prospecting", "qualification", "proposal", "negotiation"])
    ).all()
    
    total_pipeline = sum(deal.value for deal in pipeline_value)
    
    return {
        "lead_count": lead_count,
        "contact_count": contact_count,
        "deal_count": deal_count,
        "today_activities": today_activities,
        "pipeline_value": round(total_pipeline, 2),
        "greeting": get_greeting()
    }


def get_greeting():
    """Get time-based greeting"""
    hour = datetime.utcnow().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


@router.get("/leads/recent")
def get_recent_leads(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get recent leads for mobile list view"""
    leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id
    ).order_by(Lead.created_at.desc()).limit(limit).all()
    
    return {
        "leads": [
            {
                "id": lead.id,
                "name": f"{lead.first_name} {lead.last_name}",
                "email": lead.email,
                "phone": lead.phone,
                "status": lead.status,
                "created_at": lead.created_at.isoformat()
            }
            for lead in leads
        ]
    }


@router.get("/deals/priority")
def get_priority_deals(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get high-priority deals for mobile focus"""
    deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["proposal", "negotiation"]),
        Deal.expected_close_date >= datetime.utcnow()
    ).order_by(Deal.expected_close_date.asc()).limit(10).all()
    
    return {
        "deals": [
            {
                "id": deal.id,
                "name": deal.name,
                "value": deal.value,
                "stage": deal.stage,
                "expected_close_date": deal.expected_close_date.isoformat() if deal.expected_close_date else None,
                "probability": deal.probability
            }
            for deal in deals
        ]
    }


@router.get("/activities/today")
def get_today_activities(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get today's activities for mobile calendar"""
    today = datetime.utcnow().date()
    activities = db.query(Activity).filter(
        Activity.organization_id == current_user.organization_id,
        Activity.scheduled_at >= today,
        Activity.scheduled_at < today + timedelta(days=1)
    ).order_by(Activity.scheduled_at.asc()).all()
    
    return {
        "activities": [
            {
                "id": activity.id,
                "subject": activity.subject,
                "type": activity.type,
                "status": activity.status,
                "scheduled_at": activity.scheduled_at.isoformat() if activity.scheduled_at else None,
                "duration_minutes": activity.duration_minutes
            }
            for activity in activities
        ]
    }


@router.get("/contacts/favorites")
def get_favorite_contacts(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get frequently contacted leads/contacts for mobile quick access"""
    # Get recent contacts (simulated favorites)
    contacts = db.query(Contact).filter(
        Contact.organization_id == current_user.organization_id
    ).order_by(Contact.updated_at.desc()).limit(limit).all()
    
    return {
        "contacts": [
            {
                "id": contact.id,
                "name": f"{contact.first_name} {contact.last_name}",
                "email": contact.email,
                "phone": contact.phone,
                "company": contact.company.name if contact.company else None
            }
            for contact in contacts
        ]
    }


@router.get("/stats/quick")
def get_quick_stats(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get quick statistics for mobile widgets"""
    # This month's won deals
    this_month = datetime.utcnow().replace(day=1)
    won_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage == "won",
        Deal.created_at >= this_month
    ).all()
    
    monthly_revenue = sum(deal.value for deal in won_deals)
    
    # Active leads
    active_leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id,
        Lead.status.in_(["new", "contacted", "qualified"])
    ).count()
    
    # Pending activities
    pending_activities = db.query(Activity).filter(
        Activity.organization_id == current_user.organization_id,
        Activity.status == "scheduled",
        Activity.scheduled_at >= datetime.utcnow()
    ).count()
    
    return {
        "monthly_revenue": round(monthly_revenue, 2),
        "active_leads": active_leads,
        "pending_activities": pending_activities,
        "won_deals_count": len(won_deals)
    }


@router.get("/search")
def mobile_search(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Quick search across entities for mobile"""
    search_term = f"%{q}%"
    
    # Search leads
    leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id,
        Lead.first_name.ilike(search_term) | Lead.last_name.ilike(search_term) | Lead.email.ilike(search_term)
    ).limit(5).all()
    
    # Search contacts
    contacts = db.query(Contact).filter(
        Contact.organization_id == current_user.organization_id,
        Contact.first_name.ilike(search_term) | Contact.last_name.ilike(search_term) | Contact.email.ilike(search_term)
    ).limit(5).all()
    
    # Search deals
    deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.name.ilike(search_term)
    ).limit(5).all()
    
    return {
        "leads": [{"id": l.id, "name": f"{l.first_name} {l.last_name}", "type": "lead"} for l in leads],
        "contacts": [{"id": c.id, "name": f"{c.first_name} {c.last_name}", "type": "contact"} for c in contacts],
        "deals": [{"id": d.id, "name": d.name, "type": "deal"} for d in deals]
    }
