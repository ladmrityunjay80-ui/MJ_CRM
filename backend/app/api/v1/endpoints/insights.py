"""
AI-Powered Insights Endpoints
Machine learning-based insights and recommendations
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User as UserModel
from app.models.lead import Lead
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.activity import Activity

router = APIRouter()


@router.get("/lead-scoring")
def get_lead_scoring_insights(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate AI-powered lead scoring insights"""
    # Get all leads
    leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id
    ).all()
    
    scored_leads = []
    
    for lead in leads:
        # Simple lead scoring algorithm
        score = 0
        factors = []
        
        # Score based on status
        if lead.status == "qualified":
            score += 30
            factors.append("Qualified status")
        elif lead.status == "contacted":
            score += 20
            factors.append("Contacted status")
        elif lead.status == "new":
            score += 10
            factors.append("New lead")
        
        # Score based on source
        if lead.source == "referral":
            score += 25
            factors.append("Referral source")
        elif lead.source == "website":
            score += 15
            factors.append("Website source")
        
        # Score based on completeness
        if lead.email:
            score += 10
            factors.append("Has email")
        if lead.phone:
            score += 10
            factors.append("Has phone")
        if lead.company:
            score += 15
            factors.append("Has company")
        
        # Cap score at 100
        score = min(score, 100)
        
        scored_leads.append({
            "id": lead.id,
            "name": f"{lead.first_name} {lead.last_name}",
            "email": lead.email,
            "score": score,
            "factors": factors,
            "priority": "high" if score >= 70 else "medium" if score >= 40 else "low"
        })
    
    # Sort by score
    scored_leads.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "total_leads": len(leads),
        "high_priority": len([l for l in scored_leads if l["priority"] == "high"]),
        "medium_priority": len([l for l in scored_leads if l["priority"] == "medium"]),
        "low_priority": len([l for l in scored_leads if l["priority"] == "low"]),
        "top_leads": scored_leads[:10]
    }


@router.get("/deal-predictions")
def get_deal_predictions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate AI-powered deal closing predictions"""
    # Get open deals
    open_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["prospecting", "qualification", "proposal", "negotiation"])
    ).all()
    
    predictions = []
    
    for deal in open_deals:
        # Simple prediction algorithm
        win_probability = deal.probability or 50
        
        # Adjust based on stage
        stage_weights = {
            "prospecting": 0.8,
            "qualification": 0.9,
            "proposal": 1.1,
            "negotiation": 1.2
        }
        
        win_probability *= stage_weights.get(deal.stage, 1.0)
        
        # Adjust based on value (larger deals are harder to close)
        if deal.value > 100000:
            win_probability *= 0.9
        elif deal.value > 50000:
            win_probability *= 0.95
        
        # Cap probability
        win_probability = min(max(win_probability, 10), 95)
        
        # Predict close date
        predicted_close = None
        if deal.expected_close_date:
            predicted_close = deal.expected_close_date
        
        predictions.append({
            "id": deal.id,
            "name": deal.name,
            "value": deal.value,
            "stage": deal.stage,
            "win_probability": round(win_probability, 1),
            "predicted_close_date": predicted_close.isoformat() if predicted_close else None,
            "confidence": "high" if win_probability >= 70 else "medium" if win_probability >= 40 else "low"
        })
    
    # Sort by win probability
    predictions.sort(key=lambda x: x["win_probability"], reverse=True)
    
    return {
        "total_deals": len(open_deals),
        "high_probability": len([d for d in predictions if d["confidence"] == "high"]),
        "medium_probability": len([d for d in predictions if d["confidence"] == "medium"]),
        "low_probability": len([d for d in predictions if d["confidence"] == "low"]),
        "predictions": predictions
    }


@router.get("/activity-recommendations")
def get_activity_recommendations(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate AI-powered activity recommendations"""
    recommendations = []
    
    # Check for overdue activities
    overdue_activities = db.query(Activity).filter(
        Activity.organization_id == current_user.organization_id,
        Activity.status == "scheduled",
        Activity.scheduled_at < datetime.utcnow()
    ).all()
    
    if overdue_activities:
        recommendations.append({
            "type": "urgent",
            "title": f"{len(overdue_activities)} overdue activities",
            "description": "You have overdue activities that need attention",
            "priority": "high",
            "count": len(overdue_activities)
        })
    
    # Check for deals nearing close date
    upcoming_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["proposal", "negotiation"]),
        Deal.expected_close_date >= datetime.utcnow(),
        Deal.expected_close_date <= datetime.utcnow() + timedelta(days=7)
    ).all()
    
    if upcoming_deals:
        recommendations.append({
            "type": "opportunity",
            "title": f"{len(upcoming_deals)} deals closing soon",
            "description": "Focus on these deals to maximize revenue",
            "priority": "high",
            "count": len(upcoming_deals)
        })
    
    # Check for leads without recent activity
    recent_date = datetime.utcnow() - timedelta(days=7)
    stale_leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id,
        Lead.status.in_(["new", "contacted"]),
        Lead.created_at < recent_date
    ).all()
    
    if stale_leads:
        recommendations.append({
            "type": "followup",
            "title": f"{len(stale_leads)} leads need follow-up",
            "description": "These leads haven't been contacted recently",
            "priority": "medium",
            "count": len(stale_leads)
        })
    
    # General recommendation based on deal pipeline
    total_pipeline = db.query(func.sum(Deal.value)).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage.in_(["prospecting", "qualification", "proposal", "negotiation"])
    ).scalar() or 0
    
    if total_pipeline > 100000:
        recommendations.append({
            "type": "growth",
            "title": "Strong pipeline opportunity",
            "description": f"Your pipeline value is ${round(total_pipeline, 2)} - focus on closing deals",
            "priority": "medium",
            "count": 0
        })
    
    return {
        "total_recommendations": len(recommendations),
        "recommendations": recommendations
    }


@router.get("/performance-trends")
def get_performance_trends(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Generate AI-powered performance trend analysis"""
    # Get deals from last 6 months
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    
    deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.created_at >= six_months_ago
    ).all()
    
    # Calculate monthly trends
    monthly_data = {}
    for deal in deals:
        month_key = deal.created_at.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {"deals": 0, "value": 0, "won": 0}
        
        monthly_data[month_key]["deals"] += 1
        monthly_data[month_key]["value"] += deal.value
        if deal.stage == "won":
            monthly_data[month_key]["won"] += 1
    
    # Calculate trends
    months = sorted(monthly_data.keys())
    if len(months) >= 2:
        recent_month = monthly_data[months[-1]]
        previous_month = monthly_data[months[-2]]
        
        deal_trend = ((recent_month["deals"] - previous_month["deals"]) / previous_month["deals"] * 100) if previous_month["deals"] > 0 else 0
        value_trend = ((recent_month["value"] - previous_month["value"]) / previous_month["value"] * 100) if previous_month["value"] > 0 else 0
        win_rate_trend = ((recent_month["won"] - previous_month["won"]) / previous_month["won"] * 100) if previous_month["won"] > 0 else 0
    else:
        deal_trend = 0
        value_trend = 0
        win_rate_trend = 0
    
    # Generate insights
    insights = []
    
    if deal_trend > 10:
        insights.append("Deal creation is increasing - good momentum")
    elif deal_trend < -10:
        insights.append("Deal creation is declining - consider lead generation")
    
    if value_trend > 10:
        insights.append("Deal values are increasing - focus on closing")
    elif value_trend < -10:
        insights.append("Deal values are decreasing - review pricing strategy")
    
    if win_rate_trend > 10:
        insights.append("Win rate is improving - continue current approach")
    elif win_rate_trend < -10:
        insights.append("Win rate is declining - review sales process")
    
    return {
        "monthly_data": monthly_data,
        "trends": {
            "deal_trend": round(deal_trend, 1),
            "value_trend": round(value_trend, 1),
            "win_rate_trend": round(win_rate_trend, 1)
        },
        "insights": insights
    }


@router.get("/summary")
def get_insights_summary(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get comprehensive AI insights summary"""
    # Get key metrics
    total_leads = db.query(Lead).filter(
        Lead.organization_id == current_user.organization_id
    ).count()
    
    total_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id
    ).count()
    
    won_deals = db.query(Deal).filter(
        Deal.organization_id == current_user.organization_id,
        Deal.stage == "won"
    ).count()
    
    # Calculate key ratios
    lead_to_deal_ratio = (total_deals / total_leads * 100) if total_leads > 0 else 0
    win_rate = (won_deals / total_deals * 100) if total_deals > 0 else 0
    
    # Generate overall health score
    health_score = 0
    
    # Lead health (0-30 points)
    if total_leads > 50:
        health_score += 30
    elif total_leads > 20:
        health_score += 20
    elif total_leads > 10:
        health_score += 10
    
    # Deal health (0-30 points)
    if total_deals > 20:
        health_score += 30
    elif total_deals > 10:
        health_score += 20
    elif total_deals > 5:
        health_score += 10
    
    # Win rate health (0-40 points)
    if win_rate > 30:
        health_score += 40
    elif win_rate > 20:
        health_score += 30
    elif win_rate > 10:
        health_score += 20
    elif win_rate > 5:
        health_score += 10
    
    health_status = "excellent" if health_score >= 80 else "good" if health_score >= 60 else "fair" if health_score >= 40 else "needs improvement"
    
    return {
        "health_score": health_score,
        "health_status": health_status,
        "key_metrics": {
            "total_leads": total_leads,
            "total_deals": total_deals,
            "won_deals": won_deals,
            "lead_to_deal_ratio": round(lead_to_deal_ratio, 1),
            "win_rate": round(win_rate, 1)
        },
        "recommendations": [
            "Focus on lead generation to increase pipeline",
            "Improve follow-up process to increase conversion",
            "Review pricing strategy to optimize deal values"
        ] if health_score < 60 else [
            "Maintain current sales processes",
            "Consider scaling successful strategies",
            "Explore new market opportunities"
        ]
    }
