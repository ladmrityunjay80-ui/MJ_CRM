"""
Workflow Endpoints
CRUD operations for workflow automation
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, Workflow, WorkflowListResponse, WorkflowExecution
from app.models.user import User as UserModel
from app.models.workflow import Workflow as WorkflowModel, WorkflowAction as WorkflowActionModel, WorkflowExecution as WorkflowExecutionModel

router = APIRouter()


@router.post("/", response_model=Workflow, status_code=status.HTTP_201_CREATED)
def create_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new workflow"""
    new_workflow = WorkflowModel(
        id=str(uuid.uuid4()),
        name=workflow_data.name,
        description=workflow_data.description,
        trigger_type=workflow_data.trigger_type,
        trigger_config=json.dumps(workflow_data.trigger_config) if workflow_data.trigger_config else None,
        status=workflow_data.status,
        organization_id=current_user.organization_id
    )
    
    db.add(new_workflow)
    db.flush()
    
    # Create workflow actions
    for action_data in workflow_data.actions:
        action = WorkflowActionModel(
            id=str(uuid.uuid4()),
            workflow_id=new_workflow.id,
            action_type=action_data.action_type,
            action_config=json.dumps(action_data.action_config),
            order=action_data.order
        )
        db.add(action)
    
    db.commit()
    db.refresh(new_workflow)
    
    return new_workflow


@router.get("/", response_model=WorkflowListResponse)
def get_workflows(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all workflows with filtering and pagination"""
    # Build query
    query = db.query(WorkflowModel).filter(WorkflowModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if status:
        query = query.filter(WorkflowModel.status == status)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    workflows = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "workflows": workflows,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{workflow_id}", response_model=Workflow)
def get_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific workflow"""
    workflow = db.query(WorkflowModel).filter(
        WorkflowModel.id == workflow_id,
        WorkflowModel.organization_id == current_user.organization_id
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    return workflow


@router.put("/{workflow_id}", response_model=Workflow)
def update_workflow(
    workflow_id: str,
    workflow_data: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a workflow"""
    workflow = db.query(WorkflowModel).filter(
        WorkflowModel.id == workflow_id,
        WorkflowModel.organization_id == current_user.organization_id
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    # Update workflow fields
    update_data = workflow_data.model_dump(exclude_unset=True, exclude={"actions"})
    
    if "trigger_config" in update_data and update_data["trigger_config"] is not None:
        update_data["trigger_config"] = json.dumps(update_data["trigger_config"])
    
    for field, value in update_data.items():
        setattr(workflow, field, value)
    
    # Update actions if provided
    if workflow_data.actions is not None:
        # Delete existing actions
        db.query(WorkflowActionModel).filter(WorkflowActionModel.workflow_id == workflow_id).delete()
        
        # Create new actions
        for action_data in workflow_data.actions:
            action = WorkflowActionModel(
                id=str(uuid.uuid4()),
                workflow_id=workflow.id,
                action_type=action_data.action_type,
                action_config=json.dumps(action_data.action_config),
                order=action_data.order
            )
            db.add(action)
    
    db.commit()
    db.refresh(workflow)
    
    return workflow


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a workflow"""
    workflow = db.query(WorkflowModel).filter(
        WorkflowModel.id == workflow_id,
        WorkflowModel.organization_id == current_user.organization_id
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    db.delete(workflow)
    db.commit()
    
    return None


@router.post("/{workflow_id}/execute", response_model=WorkflowExecution)
def execute_workflow(
    workflow_id: str,
    trigger_entity_id: Optional[str] = None,
    trigger_entity_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Manually trigger workflow execution"""
    workflow = db.query(WorkflowModel).filter(
        WorkflowModel.id == workflow_id,
        WorkflowModel.organization_id == current_user.organization_id
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    if workflow.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workflow is not active"
        )
    
    # Create execution record
    from datetime import datetime
    execution = WorkflowExecutionModel(
        id=str(uuid.uuid4()),
        workflow_id=workflow.id,
        trigger_entity_id=trigger_entity_id,
        trigger_entity_type=trigger_entity_type,
        status="running",
        started_at=datetime.utcnow()
    )
    
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    # TODO: Implement actual workflow execution logic
    # This would involve processing each action in order
    
    # For now, mark as completed
    execution.status = "completed"
    execution.completed_at = datetime.utcnow()
    execution.result = json.dumps({"message": "Workflow executed successfully"})
    db.commit()
    db.refresh(execution)
    
    return execution


@router.get("/{workflow_id}/executions", response_model=list[WorkflowExecution])
def get_workflow_executions(
    workflow_id: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get execution history for a workflow"""
    workflow = db.query(WorkflowModel).filter(
        WorkflowModel.id == workflow_id,
        WorkflowModel.organization_id == current_user.organization_id
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    executions = db.query(WorkflowExecutionModel).filter(
        WorkflowExecutionModel.workflow_id == workflow_id
    ).order_by(WorkflowExecutionModel.created_at.desc()).limit(limit).all()
    
    return executions
