"""
Analytics Schemas
Pydantic models for analytics request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from app.models.analytics import ReportType


class ReportBase(BaseModel):
    """Base report schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    report_type: ReportType
    config: Optional[dict[str, Any]] = None


class ReportCreate(ReportBase):
    """Schema for creating a report"""
    is_scheduled: bool = False
    schedule_frequency: Optional[str] = None
    schedule_day: Optional[str] = None
    schedule_time: Optional[str] = None


class ReportUpdate(BaseModel):
    """Schema for updating a report"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    report_type: Optional[ReportType] = None
    config: Optional[dict[str, Any]] = None
    is_scheduled: Optional[bool] = None
    schedule_frequency: Optional[str] = None
    schedule_day: Optional[str] = None
    schedule_time: Optional[str] = None


class Report(ReportBase):
    """Schema for report response"""
    id: str
    is_scheduled: bool
    schedule_frequency: Optional[str] = None
    schedule_day: Optional[str] = None
    schedule_time: Optional[str] = None
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    organization_id: str
    created_by_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DashboardBase(BaseModel):
    """Base dashboard schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    layout: Optional[dict[str, Any]] = None


class DashboardCreate(DashboardBase):
    """Schema for creating a dashboard"""
    pass


class DashboardUpdate(BaseModel):
    """Schema for updating a dashboard"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    layout: Optional[dict[str, Any]] = None


class Dashboard(DashboardBase):
    """Schema for dashboard response"""
    id: str
    organization_id: str
    created_by_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ReportListResponse(BaseModel):
    """Schema for report list response"""
    reports: List[Report]
    total: int
    page: int
    page_size: int


class DashboardListResponse(BaseModel):
    """Schema for dashboard list response"""
    dashboards: List[Dashboard]
    total: int
    page: int
    page_size: int


class AnalyticsSummary(BaseModel):
    """Schema for analytics summary"""
    total_leads: int
    total_contacts: int
    total_deals: int
    total_pipeline_value: float
    won_deals_this_month: int
    conversion_rate: float
    average_deal_size: float
