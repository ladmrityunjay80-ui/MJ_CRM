"""
Forecasting Endpoints
Advanced sales forecasting and revenue predictions
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.deal import Deal

router = APIRouter()


@router.get("/revenue")
def get_revenue_forecast(
    months: int = Query(6, ge=1, le=24, description="Number of months to forecast"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get revenue forecast based on historical deal data"""
    # Get historical deals for the past 12 months
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=365)
    
    historical_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage == "won",
        Deal.created_at >= start_date,
        Deal.created_at <= end_date
    ).all()
    
    # Calculate monthly revenue from historical data
    monthly_revenue = {}
    for deal in historical_deals:
        month_key = deal.created_at.strftime("%Y-%m")
        if month_key not in monthly_revenue:
            monthly_revenue[month_key] = 0
        monthly_revenue[month_key] += deal.value
    
    # Calculate average monthly revenue
    if monthly_revenue:
        avg_monthly_revenue = sum(monthly_revenue.values()) / len(monthly_revenue)
    else:
        avg_monthly_revenue = 0
    
    # Generate forecast for future months
    forecast = []
    for i in range(1, months + 1):
        forecast_date = end_date + timedelta(days=30 * i)
        month_key = forecast_date.strftime("%Y-%m")
        
        # Simple linear forecast with slight growth assumption
        growth_factor = 1.0 + (i * 0.02)  # 2% growth per month
        predicted_revenue = avg_monthly_revenue * growth_factor
        
        forecast.append({
            "month": month_key,
            "predicted_revenue": round(predicted_revenue, 2),
            "confidence": "medium" if i <= 3 else "low"
        })
    
    return {
        "historical_data": monthly_revenue,
        "average_monthly_revenue": round(avg_monthly_revenue, 2),
        "forecast": forecast,
        "total_forecasted_revenue": round(sum(f["predicted_revenue"] for f in forecast), 2)
    }


@router.get("/pipeline")
def get_pipeline_forecast(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get pipeline forecast based on current deals"""
    # Get all open deals
    open_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["prospecting", "qualification", "proposal", "negotiation"])
    ).all()
    
    # Calculate weighted pipeline value by stage
    stage_weights = {
        "prospecting": 0.1,
        "qualification": 0.2,
        "proposal": 0.5,
        "negotiation": 0.8
    }
    
    pipeline_by_stage = {}
    total_weighted_value = 0
    total_unweighted_value = 0
    
    for deal in open_deals:
        stage = deal.stage
        weight = stage_weights.get(stage, 0.5)
        weighted_value = deal.value * weight
        
        if stage not in pipeline_by_stage:
            pipeline_by_stage[stage] = {
                "count": 0,
                "total_value": 0,
                "weighted_value": 0
            }
        
        pipeline_by_stage[stage]["count"] += 1
        pipeline_by_stage[stage]["total_value"] += deal.value
        pipeline_by_stage[stage]["weighted_value"] += weighted_value
        
        total_weighted_value += weighted_value
        total_unweighted_value += deal.value
    
    # Calculate expected close dates
    expected_revenue_by_month = {}
    for deal in open_deals:
        if deal.expected_close_date:
            month_key = deal.expected_close_date.strftime("%Y-%m")
            weight = stage_weights.get(deal.stage, 0.5)
            if month_key not in expected_revenue_by_month:
                expected_revenue_by_month[month_key] = 0
            expected_revenue_by_month[month_key] += deal.value * weight
    
    return {
        "pipeline_by_stage": pipeline_by_stage,
        "total_deals": len(open_deals),
        "total_unweighted_value": round(total_unweighted_value, 2),
        "total_weighted_value": round(total_weighted_value, 2),
        "expected_revenue_by_month": expected_revenue_by_month
    }


@router.get("/conversion")
def get_conversion_forecast(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get conversion rate analysis and forecast"""
    # Get all deals
    all_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id
    ).all()
    
    # Calculate conversion rates by stage
    stage_conversion = {}
    total_deals = len(all_deals)
    
    if total_deals > 0:
        for stage in ["prospecting", "qualification", "proposal", "negotiation", "won", "lost"]:
            stage_count = sum(1 for deal in all_deals if deal.stage == stage)
            stage_conversion[stage] = {
                "count": stage_count,
                "percentage": round((stage_count / total_deals) * 100, 2)
            }
    
    # Calculate win rate
    won_deals = sum(1 for deal in all_deals if deal.stage == "won")
    lost_deals = sum(1 for deal in all_deals if deal.stage == "lost")
    total_closed = won_deals + lost_deals
    
    win_rate = round((won_deals / total_closed) * 100, 2) if total_closed > 0 else 0
    
    # Calculate average deal value
    if won_deals > 0:
        avg_deal_value = sum(deal.value for deal in all_deals if deal.stage == "won") / won_deals
    else:
        avg_deal_value = 0
    
    return {
        "stage_conversion": stage_conversion,
        "total_deals": total_deals,
        "win_rate": win_rate,
        "average_deal_value": round(avg_deal_value, 2),
        "won_deals": won_deals,
        "lost_deals": lost_deals
    }


@router.get("/summary")
def get_forecasting_summary(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get comprehensive forecasting summary"""
    # Get basic deal statistics
    total_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id
    ).count()
    
    won_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage == "won"
    ).count()
    
    open_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["prospecting", "qualification", "proposal", "negotiation"])
    ).count()
    
    # Calculate total revenue
    total_revenue = db.query(func.sum(Deal.value)).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage == "won"
    ).scalar() or 0
    
    # Calculate pipeline value
    pipeline_value = db.query(func.sum(Deal.value)).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["prospecting", "qualification", "proposal", "negotiation"])
    ).scalar() or 0
    
    return {
        "total_deals": total_deals,
        "won_deals": won_deals,
        "open_deals": open_deals,
        "total_revenue": round(total_revenue, 2),
        "pipeline_value": round(pipeline_value, 2),
        "win_rate": round((won_deals / total_deals) * 100, 2) if total_deals > 0 else 0
    }
