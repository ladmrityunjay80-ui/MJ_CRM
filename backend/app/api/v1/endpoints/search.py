"""
Search Endpoints
Advanced search across all CRM entities
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.lead import Lead
from app.models.contact import Contact
from app.models.company import Company
from app.models.deal import Deal
from app.models.activity import Activity
from app.models.product import Product

router = APIRouter()


@router.get("/")
def global_search(
    q: str = Query(..., min_length=1, description="Search query"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Global search across all CRM entities"""
    search_term = f"%{q}%"
    org_id = current_user.organization_id
    results = []
    
    # Search leads
    if not entity_type or entity_type == "leads":
        leads = db.query(Lead).filter(
            Lead.organization_id == org_id,
            or_(
                Lead.first_name.ilike(search_term),
                Lead.last_name.ilike(search_term),
                Lead.email.ilike(search_term),
                Lead.company.ilike(search_term),
                Lead.notes.ilike(search_term)
            )
        ).limit(5).all()
        
        for lead in leads:
            results.append({
                "type": "lead",
                "id": lead.id,
                "title": f"{lead.first_name} {lead.last_name}",
                "subtitle": lead.email or lead.company or "",
                "status": lead.status,
                "url": f"/leads/{lead.id}"
            })
    
    # Search contacts
    if not entity_type or entity_type == "contacts":
        contacts = db.query(Contact).filter(
            Contact.organization_id == org_id,
            or_(
                Contact.first_name.ilike(search_term),
                Contact.last_name.ilike(search_term),
                Contact.email.ilike(search_term),
                Contact.job_title.ilike(search_term),
                Contact.notes.ilike(search_term)
            )
        ).limit(5).all()
        
        for contact in contacts:
            results.append({
                "type": "contact",
                "id": contact.id,
                "title": f"{contact.first_name} {contact.last_name}",
                "subtitle": contact.email or contact.job_title or "",
                "url": f"/contacts/{contact.id}"
            })
    
    # Search companies
    if not entity_type or entity_type == "companies":
        companies = db.query(Company).filter(
            Company.organization_id == org_id,
            or_(
                Company.name.ilike(search_term),
                Company.industry.ilike(search_term),
                Company.website.ilike(search_term),
                Company.notes.ilike(search_term)
            )
        ).limit(5).all()
        
        for company in companies:
            results.append({
                "type": "company",
                "id": company.id,
                "title": company.name,
                "subtitle": company.industry or company.website or "",
                "url": f"/companies/{company.id}"
            })
    
    # Search deals
    if not entity_type or entity_type == "deals":
        deals = db.query(Deal).filter(
            Deal.organization_id == org_id,
            or_(
                Deal.name.ilike(search_term),
                Deal.description.ilike(search_term),
                Deal.notes.ilike(search_term)
            )
        ).limit(5).all()
        
        for deal in deals:
            results.append({
                "type": "deal",
                "id": deal.id,
                "title": deal.name,
                "subtitle": f"{deal.currency} {deal.value} - {deal.stage}",
                "status": deal.stage,
                "url": f"/deals/{deal.id}"
            })
    
    # Search activities
    if not entity_type or entity_type == "activities":
        activities = db.query(Activity).filter(
            Activity.organization_id == org_id,
            or_(
                Activity.subject.ilike(search_term),
                Activity.description.ilike(search_term),
                Activity.notes.ilike(search_term)
            )
        ).limit(5).all()
        
        for activity in activities:
            results.append({
                "type": "activity",
                "id": activity.id,
                "title": activity.subject,
                "subtitle": f"{activity.type} - {activity.status}",
                "url": f"/activities/{activity.id}"
            })
    
    # Search products
    if not entity_type or entity_type == "products":
        products = db.query(Product).filter(
            Product.organization_id == org_id,
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.sku.ilike(search_term)
            )
        ).limit(5).all()
        
        for product in products:
            results.append({
                "type": "product",
                "id": product.id,
                "title": product.name,
                "subtitle": f"{product.currency} {product.price} - {product.product_type}",
                "url": f"/products/{product.id}"
            })
    
    # Paginate results
    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = results[start:end]
    
    return {
        "results": paginated_results,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/leads")
def search_leads(
    q: str = Query(..., min_length=1),
    status: Optional[str] = None,
    source: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Advanced search for leads"""
    search_term = f"%{q}%"
    query = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id,
        or_(
            Lead.first_name.ilike(search_term),
            Lead.last_name.ilike(search_term),
            Lead.email.ilike(search_term),
            Lead.company.ilike(search_term),
            Lead.notes.ilike(search_term)
        )
    )
    
    if status:
        query = query.filter(Lead.status == status)
    if source:
        query = query.filter(Lead.source == source)
    
    total = query.count()
    leads = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "results": leads,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/contacts")
def search_contacts(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Advanced search for contacts"""
    search_term = f"%{q}%"
    query = db.query(Contact).filter(
        Contact.organization_id == current_user.organization_id,
        or_(
            Contact.first_name.ilike(search_term),
            Contact.last_name.ilike(search_term),
            Contact.email.ilike(search_term),
            Contact.job_title.ilike(search_term),
            Contact.notes.ilike(search_term)
        )
    )
    
    total = query.count()
    contacts = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "results": contacts,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/deals")
def search_deals(
    q: str = Query(..., min_length=1),
    stage: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Advanced search for deals"""
    search_term = f"%{q}%"
    query = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        or_(
            Deal.name.ilike(search_term),
            Deal.description.ilike(search_term),
            Deal.notes.ilike(search_term)
        )
    )
    
    if stage:
        query = query.filter(Deal.stage == stage)
    if min_value:
        query = query.filter(Deal.value >= min_value)
    if max_value:
        query = query.filter(Deal.value <= max_value)
    
    total = query.count()
    deals = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "results": deals,
        "total": total,
        "page": page,
        "page_size": page_size
    }
