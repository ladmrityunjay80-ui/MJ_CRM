"""
Import/Export Endpoints
Handles importing and exporting CRM data
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import csv
import io
import json
from datetime import datetime
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.lead import Lead
from app.models.contact import Contact
from app.models.company import Company
from app.models.deal import Deal
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/export/leads")
def export_leads(
    format: str = Query("csv", pattern="^(csv|json)$"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Export leads to CSV or JSON"""
    leads = db.query(Lead).filter(Lead.organization_id == current_user.organization_id).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "first_name", "last_name", "email", "phone", "company", "status", "source", "created_at"])
        
        for lead in leads:
            writer.writerow([
                lead.id,
                lead.first_name,
                lead.last_name,
                lead.email,
                lead.phone,
                lead.company,
                lead.status,
                lead.source,
                lead.created_at.isoformat()
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=leads_export.csv"}
        )
    
    elif format == "json":
        data = []
        for lead in leads:
            data.append({
                "id": lead.id,
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "email": lead.email,
                "phone": lead.phone,
                "company": lead.company,
                "status": lead.status,
                "source": lead.source,
                "created_at": lead.created_at.isoformat()
            })
        
        return StreamingResponse(
            io.BytesIO(json.dumps(data, indent=2).encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=leads_export.json"}
        )


@router.get("/export/contacts")
def export_contacts(
    format: str = Query("csv", pattern="^(csv|json)$"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Export contacts to CSV or JSON"""
    contacts = db.query(Contact).filter(Contact.organization_id == current_user.organization_id).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "first_name", "last_name", "email", "phone", "mobile", "job_title", "created_at"])
        
        for contact in contacts:
            writer.writerow([
                contact.id,
                contact.first_name,
                contact.last_name,
                contact.email,
                contact.phone,
                contact.mobile,
                contact.job_title,
                contact.created_at.isoformat()
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=contacts_export.csv"}
        )
    
    elif format == "json":
        data = []
        for contact in contacts:
            data.append({
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email,
                "phone": contact.phone,
                "mobile": contact.mobile,
                "job_title": contact.job_title,
                "created_at": contact.created_at.isoformat()
            })
        
        return StreamingResponse(
            io.BytesIO(json.dumps(data, indent=2).encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=contacts_export.json"}
        )


@router.get("/export/companies")
def export_companies(
    format: str = Query("csv", pattern="^(csv|json)$"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Export companies to CSV or JSON"""
    companies = db.query(Company).filter(Company.organization_id == current_user.organization_id).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "industry", "website", "size", "created_at"])
        
        for company in companies:
            writer.writerow([
                company.id,
                company.name,
                company.industry,
                company.website,
                company.size,
                company.created_at.isoformat()
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=companies_export.csv"}
        )
    
    elif format == "json":
        data = []
        for company in companies:
            data.append({
                "id": company.id,
                "name": company.name,
                "industry": company.industry,
                "website": company.website,
                "size": company.size,
                "created_at": company.created_at.isoformat()
            })
        
        return StreamingResponse(
            io.BytesIO(json.dumps(data, indent=2).encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=companies_export.json"}
        )


@router.get("/export/deals")
def export_deals(
    format: str = Query("csv", pattern="^(csv|json)$"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Export deals to CSV or JSON"""
    deals = db.query(Deal).filter(Deal.organization_id == current_user.organization_id).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "value", "currency", "stage", "probability", "created_at"])
        
        for deal in deals:
            writer.writerow([
                deal.id,
                deal.name,
                deal.value,
                deal.currency,
                deal.stage,
                deal.probability,
                deal.created_at.isoformat()
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=deals_export.csv"}
        )
    
    elif format == "json":
        data = []
        for deal in deals:
            data.append({
                "id": deal.id,
                "name": deal.name,
                "value": deal.value,
                "currency": deal.currency,
                "stage": deal.stage,
                "probability": deal.probability,
                "created_at": deal.created_at.isoformat()
            })
        
        return StreamingResponse(
            io.BytesIO(json.dumps(data, indent=2).encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=deals_export.json"}
        )


@router.post("/import/leads")
def import_leads(
    data: list[dict],
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Import leads from JSON data"""
    import uuid
    
    imported_count = 0
    errors = []
    
    for item in data:
        try:
            new_lead = Lead(
                id=str(uuid.uuid4()),
                first_name=item.get("first_name", ""),
                last_name=item.get("last_name", ""),
                email=item.get("email"),
                phone=item.get("phone"),
                company=item.get("company"),
                status=item.get("status", "new"),
                source=item.get("source", "other"),
                organization_id=current_user.organization_id
            )
            db.add(new_lead)
            imported_count += 1
        except Exception as e:
            errors.append({"row": item, "error": str(e)})
    
    db.commit()
    
    return {
        "imported": imported_count,
        "errors": errors,
        "total": len(data)
    }


@router.post("/import/contacts")
def import_contacts(
    data: list[dict],
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Import contacts from JSON data"""
    import uuid
    
    imported_count = 0
    errors = []
    
    for item in data:
        try:
            new_contact = Contact(
                id=str(uuid.uuid4()),
                first_name=item.get("first_name", ""),
                last_name=item.get("last_name", ""),
                email=item.get("email"),
                phone=item.get("phone"),
                mobile=item.get("mobile"),
                job_title=item.get("job_title"),
                organization_id=current_user.organization_id,
                created_by_id=current_user.id
            )
            db.add(new_contact)
            imported_count += 1
        except Exception as e:
            errors.append({"row": item, "error": str(e)})
    
    db.commit()
    
    return {
        "imported": imported_count,
        "errors": errors,
        "total": len(data)
    }
