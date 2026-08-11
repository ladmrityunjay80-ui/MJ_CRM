"""
Workflow Schemas
Pydantic models for workflow request/response validation
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
import json
from app.models.workflow import TriggerType, ActionType, WorkflowStatus


class WorkflowActionBase(BaseModel):
    """Base workflow action schema"""
    action_type: ActionType
    action_config: dict[str, Any] = Field(..., description="Action parameters as JSON")
    order: int = Field(..., ge=0, description="Execution order")


class WorkflowActionCreate(WorkflowActionBase):
    """Schema for creating a workflow action"""
    pass


class WorkflowAction(WorkflowActionBase):
    """Schema for workflow action response"""
    id: str
    workflow_id: str
    created_at: datetime
    updated_at: datetime
    
    @field_validator('action_config', mode='before')
    @classmethod
    def parse_action_config(cls, v):
        """Parse JSON string to dict if needed"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v
    
    model_config = ConfigDict(from_attributes=True)


class WorkflowBase(BaseModel):
    """Base workflow schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    trigger_type: TriggerType
    trigger_config: Optional[dict[str, Any]] = None
    status: WorkflowStatus = WorkflowStatus.DRAFT


class WorkflowCreate(WorkflowBase):
    """Schema for creating a workflow"""
    actions: List[WorkflowActionCreate] = []


class WorkflowUpdate(BaseModel):
    """Schema for updating a workflow"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    trigger_type: Optional[TriggerType] = None
    trigger_config: Optional[dict[str, Any]] = None
    status: Optional[WorkflowStatus] = None
    actions: Optional[List[WorkflowActionCreate]] = None


class Workflow(WorkflowBase):
    """Schema for workflow response"""
    id: str
    organization_id: str
    actions: List[WorkflowAction] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class WorkflowExecutionBase(BaseModel):
    """Base workflow execution schema"""
    trigger_entity_id: Optional[str] = None
    trigger_entity_type: Optional[str] = None


class WorkflowExecution(WorkflowExecutionBase):
    """Schema for workflow execution response"""
    id: str
    workflow_id: str
    status: str
    result: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class WorkflowListResponse(BaseModel):
    """Schema for workflow list response"""
    workflows: List[Workflow]
    total: int
    page: int
    page_size: int
