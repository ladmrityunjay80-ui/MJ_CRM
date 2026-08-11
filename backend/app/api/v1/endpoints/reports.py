"""
Advanced Reporting Endpoints
Comprehensive reporting with custom filters and export capabilities
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
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


@router.get("/sales-performance")
def get_sales_performance_report(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate sales performance report"""
    # Default to last 30 days if no dates provided
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    # Get deals in date range
    deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.created_at >= start_dt,
        Deal.created_at < end_dt
    ).all()
    
    # Calculate metrics
    total_deals = len(deals)
    won_deals = [d for d in deals if d.stage == "won"]
    lost_deals = [d for d in deals if d.stage == "lost"]
    open_deals = [d for d in deals if d.stage in ["prospecting", "qualification", "proposal", "negotiation"]]
    
    total_value = sum(d.value for d in deals)
    won_value = sum(d.value for d in won_deals)
    lost_value = sum(d.value for d in lost_deals)
    pipeline_value = sum(d.value for d in open_deals)
    
    win_rate = (len(won_deals) / total_deals * 100) if total_deals > 0 else 0
    avg_deal_size = (total_value / total_deals) if total_deals > 0 else 0
    
    return {
        "period": {"start_date": start_date, "end_date": end_date},
        "total_deals": total_deals,
        "won_deals": len(won_deals),
        "lost_deals": len(lost_deals),
        "open_deals": len(open_deals),
        "total_value": round(total_value, 2),
        "won_value": round(won_value, 2),
        "lost_value": round(lost_value, 2),
        "pipeline_value": round(pipeline_value, 2),
        "win_rate": round(win_rate, 2),
        "avg_deal_size": round(avg_deal_size, 2)
    }


@router.get("/lead-conversion")
def get_lead_conversion_report(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate lead conversion funnel report"""
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    # Get leads in date range
    leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id,
        Lead.created_at >= start_dt,
        Lead.created_at < end_dt
    ).all()
    
    # Count by status
    status_counts = {}
    for lead in leads:
        status = lead.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    total_leads = len(leads)
    
    # Calculate conversion rates
    conversion_rates = {}
    for status, count in status_counts.items():
        conversion_rates[status] = {
            "count": count,
            "percentage": round((count / total_leads * 100), 2) if total_leads > 0 else 0
        }
    
    return {
        "period": {"start_date": start_date, "end_date": end_date},
        "total_leads": total_leads,
        "status_breakdown": conversion_rates
    }


@router.get("/activity-summary")
def get_activity_summary_report(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate activity summary report"""
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    # Get activities in date range
    activities = db.query(Activity).filter(
        Activity.organization_id == current_user.organization_id,
        Activity.created_at >= start_dt,
        Activity.created_at < end_dt
    ).all()
    
    # Count by type
    type_counts = {}
    status_counts = {}
    
    for activity in activities:
        # Count by type
        act_type = activity.type
        type_counts[act_type] = type_counts.get(act_type, 0) + 1
        
        # Count by status
        status = activity.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    total_activities = len(activities)
    
    return {
        "period": {"start_date": start_date, "end_date": end_date},
        "total_activities": total_activities,
        "by_type": type_counts,
        "by_status": status_counts
    }


@router.get("/revenue-trend")
def get_revenue_trend_report(
    months: int = Query(12, ge=1, le=24, description="Number of months to analyze"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate revenue trend analysis"""
    trend_data = []
    
    for i in range(months):
        # Calculate month start and end
        month_start = datetime.utcnow() - timedelta(days=30 * (months - i))
        month_end = month_start + timedelta(days=30)
        
        # Get won deals in this month
        won_deals = db.query(Deal).filter(
            Deal.organization_id == current_user.organization_id,
            Deal.stage == "won",
            Deal.created_at >= month_start,
            Deal.created_at < month_end
        ).all()
        
        month_revenue = sum(deal.value for deal in won_deals)
        month_name = month_start.strftime("%Y-%m")
        
        trend_data.append({
            "month": month_name,
            "revenue": round(month_revenue, 2),
            "deals_count": len(won_deals)
        })
    
    return {
        "trend_data": trend_data,
        "total_revenue": round(sum(item["revenue"] for item in trend_data), 2),
        "total_deals": sum(item["deals_count"] for item in trend_data)
    }


@router.get("/team-performance")
def get_team_performance_report(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate team performance report"""
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    # Get all users in organization
    from app.models.user import User
    users = db.query(User).filter(
        User.organization_id == current_user.organization_id
    ).all()
    
    team_data = []
    
    for user in users:
        # Get user's deals
        user_deals = db.query(Deal).filter(
            Deal.organization_id == current_user.organization_id,
            Deal.assigned_to_id == user.id,
            Deal.created_at >= start_dt,
            Deal.created_at < end_dt
        ).all()
        
        won_deals = [d for d in user_deals if d.stage == "won"]
        total_value = sum(d.value for d in user_deals)
        won_value = sum(d.value for d in won_deals)
        
        team_data.append({
            "user_id": user.id,
            "user_name": user.full_name,
            "user_email": user.email,
            "total_deals": len(user_deals),
            "won_deals": len(won_deals),
            "total_value": round(total_value, 2),
            "won_value": round(won_value, 2),
            "win_rate": round((len(won_deals) / len(user_deals) * 100), 2) if user_deals else 0
        })
    
    return {
        "period": {"start_date": start_date, "end_date": end_date},
        "team_data": team_data
    }


@router.get("/custom")
def get_custom_report(
    entity_type: str = Query(..., description="Entity type: leads, contacts, deals, activities"),
    filters: Optional[str] = Query(None, description="JSON string of filters"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate custom report based on entity type and filters"""
    # This is a simplified custom report generator
    # In production, this would support complex filtering and aggregation
    
    if entity_type == "deals":
        query = db.query(Deal).filter(
            Deal.organization_id == current_user.organization_id
        )
        results = query.all()
        
        return {
            "entity_type": entity_type,
            "total_records": len(results),
            "data": [
                {
                    "id": d.id,
                    "name": d.name,
                    "value": d.value,
                    "stage": d.stage,
                    "created_at": d.created_at.isoformat()
                }
                for d in results
            ]
        }
    
    elif entity_type == "leads":
        query = db.query(Lead).filter(
            Lead.organization_id == current_user.organization_id
        )
        results = query.all()
        
        return {
            "entity_type": entity_type,
            "total_records": len(results),
            "data": [
                {
                    "id": l.id,
                    "name": f"{l.first_name} {l.last_name}",
                    "email": l.email,
                    "status": l.status,
                    "created_at": l.created_at.isoformat()
                }
                for l in results
            ]
        }
    
    else:
        return {"error": "Unsupported entity type"}
