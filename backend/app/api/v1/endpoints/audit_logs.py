"""
Audit Log Endpoints
CRUD operations for audit logs
"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.audit_log import AuditLogCreate, AuditLog, AuditLogListResponse
from app.models.user import User as UserModel
from app.models.audit_log import AuditLog as AuditLogModel

router = APIRouter()


def create_audit_log(
    action: str,
    entity_type: str,
    entity_id: Optional[str],
    user_id: str,
    user_email: str,
    user_name: Optional[str],
    organization_id: str,
    old_values: Optional[dict] = None,
    new_values: Optional[dict] = None,
    description: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    db: Session = None
):
    """Helper function to create an audit log entry"""
    log = AuditLogModel(
        id=str(uuid.uuid4()),
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_values=json.dumps(old_values) if old_values else None,
        new_values=json.dumps(new_values) if new_values else None,
        description=description,
        user_id=user_id,
        user_email=user_email,
        user_name=user_name,
        organization_id=organization_id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    if db:
        db.add(log)
        db.commit()
    
    return log


@router.get("/", response_model=AuditLogListResponse)
def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get audit logs with filtering and pagination"""
    # Check if user has permission to view audit logs
    if current_user.role.value not in ["admin", "owner", "manager"]:
        return {"logs": [], "total": 0, "page": page, "page_size": page_size}
    
    # Build query
    query = db.query(AuditLogModel).filter(
        AuditLogModel.organization_id == current_user.organization_id
    )
    
    # Apply filters
    if action:
        query = query.filter(AuditLogModel.action == action)
    if entity_type:
        query = query.filter(AuditLogModel.entity_type == entity_type)
    if user_id:
        query = query.filter(AuditLogModel.user_id == user_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    logs = query.order_by(AuditLogModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "logs": logs,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{log_id}", response_model=AuditLog)
def get_audit_log(
    log_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific audit log"""
    # Check if user has permission to view audit logs
    if current_user.role.value not in ["admin", "owner", "manager"]:
        raise Exception("Insufficient permissions")
    
    log = db.query(AuditLogModel).filter(
        AuditLogModel.id == log_id,
        AuditLogModel.organization_id == current_user.organization_id
    ).first()
    
    if not log:
        raise Exception("Audit log not found")
    
    return log


@router.get("/entity/{entity_type}/{entity_id}", response_model=AuditLogListResponse)
def get_entity_audit_logs(
    entity_type: str,
    entity_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get audit logs for a specific entity"""
    # Check if user has permission to view audit logs
    if current_user.role.value not in ["admin", "owner", "manager"]:
        return {"logs": [], "total": 0, "page": page, "page_size": page_size}
    
    # Build query
    query = db.query(AuditLogModel).filter(
        AuditLogModel.organization_id == current_user.organization_id,
        AuditLogModel.entity_type == entity_type,
        AuditLogModel.entity_id == entity_id
    )
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    logs = query.order_by(AuditLogModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "logs": logs,
        "total": total,
        "page": page,
        "page_size": page_size
    }
