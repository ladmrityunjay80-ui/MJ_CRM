"""
Analytics Endpoints
CRUD operations for analytics reports and dashboards
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from typing import Optional
import uuid
import json
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.analytics import ReportCreate, ReportUpdate, Report, DashboardCreate, DashboardUpdate, Dashboard, ReportListResponse, DashboardListResponse, AnalyticsSummary
from app.models.user import User as UserModel
from app.models.analytics import Report as ReportModel, Dashboard as DashboardModel
from app.models.lead import Lead
from app.models.contact import Contact
from app.models.deal import Deal

router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get analytics summary for the organization"""
    org_id = current_user.organization_id
    
    # Get current month
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Total leads
    total_leads = db.query(Lead).filter(Lead.organization_id == org_id).count()
    
    # Total contacts
    total_contacts = db.query(Contact).filter(Contact.organization_id == org_id).count()
    
    # Total deals
    total_deals = db.query(Deal).filter(Deal.organization_id == org_id).count()
    
    # Total pipeline value
    total_pipeline_value = db.query(func.sum(Deal.value)).filter(
        Deal.organization_id == org_id,
        Deal.stage.in_(["prospecting", "qualification", "proposal", "negotiation"])
    ).scalar() or 0
    
    # Won deals this month
    won_deals_this_month = db.query(Deal).filter(
        Deal.organization_id == org_id,
        Deal.stage == "won",
        Deal.actual_close_date >= month_start
    ).count()
    
    # Conversion rate (leads to won deals)
    total_won_deals = db.query(Deal).filter(
        Deal.organization_id == org_id,
        Deal.stage == "won"
    ).count()
    conversion_rate = (total_won_deals / total_leads * 100) if total_leads > 0 else 0
    
    # Average deal size
    avg_deal_size = db.query(func.avg(Deal.value)).filter(
        Deal.organization_id == org_id,
        Deal.stage == "won"
    ).scalar() or 0
    
    return AnalyticsSummary(
        total_leads=total_leads,
        total_contacts=total_contacts,
        total_deals=total_deals,
        total_pipeline_value=float(total_pipeline_value),
        won_deals_this_month=won_deals_this_month,
        conversion_rate=float(conversion_rate),
        average_deal_size=float(avg_deal_size)
    )


# Report Endpoints

@router.post("/reports/", response_model=Report, status_code=status.HTTP_201_CREATED)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new analytics report"""
    new_report = ReportModel(
        id=str(uuid.uuid4()),
        name=report_data.name,
        description=report_data.description,
        report_type=report_data.report_type,
        config=json.dumps(report_data.config) if report_data.config else None,
        is_scheduled=str(report_data.is_scheduled).lower(),
        schedule_frequency=report_data.schedule_frequency,
        schedule_day=report_data.schedule_day,
        schedule_time=report_data.schedule_time,
        organization_id=current_user.organization_id,
        created_by_id=current_user.id
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report


@router.get("/reports/", response_model=ReportListResponse)
def get_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    report_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all reports with filtering and pagination"""
    # Build query
    query = db.query(ReportModel).filter(ReportModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if report_type:
        query = query.filter(ReportModel.report_type == report_type)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    reports = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "reports": reports,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/reports/{report_id}", response_model=Report)
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific report"""
    report = db.query(ReportModel).filter(
        ReportModel.id == report_id,
        ReportModel.organization_id == current_user.organization_id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report


@router.put("/reports/{report_id}", response_model=Report)
def update_report(
    report_id: str,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a report"""
    report = db.query(ReportModel).filter(
        ReportModel.id == report_id,
        ReportModel.organization_id == current_user.organization_id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Update report fields
    update_data = report_data.model_dump(exclude_unset=True)
    
    if "config" in update_data and update_data["config"] is not None:
        update_data["config"] = json.dumps(update_data["config"])
    
    if "is_scheduled" in update_data:
        update_data["is_scheduled"] = str(update_data["is_scheduled"]).lower()
    
    for field, value in update_data.items():
        setattr(report, field, value)
    
    db.commit()
    db.refresh(report)
    
    return report


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a report"""
    report = db.query(ReportModel).filter(
        ReportModel.id == report_id,
        ReportModel.organization_id == current_user.organization_id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    db.delete(report)
    db.commit()
    
    return None


# Dashboard Endpoints

@router.post("/dashboards/", response_model=Dashboard, status_code=status.HTTP_201_CREATED)
def create_dashboard(
    dashboard_data: DashboardCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new dashboard"""
    new_dashboard = DashboardModel(
        id=str(uuid.uuid4()),
        name=dashboard_data.name,
        description=dashboard_data.description,
        layout=json.dumps(dashboard_data.layout) if dashboard_data.layout else None,
        organization_id=current_user.organization_id,
        created_by_id=current_user.id
    )
    
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    
    return new_dashboard


@router.get("/dashboards/", response_model=DashboardListResponse)
def get_dashboards(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all dashboards with pagination"""
    # Build query
    query = db.query(DashboardModel).filter(DashboardModel.organization_id == current_user.organization_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    dashboards = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "dashboards": dashboards,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/dashboards/{dashboard_id}", response_model=Dashboard)
def get_dashboard(
    dashboard_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific dashboard"""
    dashboard = db.query(DashboardModel).filter(
        DashboardModel.id == dashboard_id,
        DashboardModel.organization_id == current_user.organization_id
    ).first()
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    return dashboard


@router.put("/dashboards/{dashboard_id}", response_model=Dashboard)
def update_dashboard(
    dashboard_id: str,
    dashboard_data: DashboardUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a dashboard"""
    dashboard = db.query(DashboardModel).filter(
        DashboardModel.id == dashboard_id,
        DashboardModel.organization_id == current_user.organization_id
    ).first()
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    # Update dashboard fields
    update_data = dashboard_data.model_dump(exclude_unset=True)
    
    if "layout" in update_data and update_data["layout"] is not None:
        update_data["layout"] = json.dumps(update_data["layout"])
    
    for field, value in update_data.items():
        setattr(dashboard, field, value)
    
    db.commit()
    db.refresh(dashboard)
    
    return dashboard


@router.delete("/dashboards/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dashboard(
    dashboard_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a dashboard"""
    dashboard = db.query(DashboardModel).filter(
        DashboardModel.id == dashboard_id,
        DashboardModel.organization_id == current_user.organization_id
    ).first()
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    db.delete(dashboard)
    db.commit()
    
    return None
