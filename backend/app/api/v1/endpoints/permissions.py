"""
Permission Endpoints
CRUD operations for RBAC permissions
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.permission import PermissionCreate, PermissionUpdate, Permission, RolePermissionCreate, RolePermission, PermissionListResponse, RolePermissionListResponse, UserPermissionsResponse
from app.models.user import User as UserModel
from app.models.permission import Permission as PermissionModel, RolePermission as RolePermissionModel

router = APIRouter()


@router.post("/", response_model=Permission, status_code=status.HTTP_201_CREATED)
def create_permission(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new permission (admin only)"""
    # Check if user is admin
    if current_user.role.value not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create permissions"
        )
    
    new_permission = PermissionModel(
        id=str(uuid.uuid4()),
        name=permission_data.name,
        description=permission_data.description,
        resource=permission_data.resource,
        action=permission_data.action,
        scope=permission_data.scope,
        is_active=True,
        organization_id=current_user.organization_id
    )
    
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    
    return new_permission


@router.get("/", response_model=PermissionListResponse)
def get_permissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    resource: Optional[str] = None,
    action: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all permissions with filtering and pagination"""
    # Build query
    query = db.query(PermissionModel)
    
    # Filter by organization if not admin
    if current_user.role.value not in ["admin", "owner"]:
        query = query.filter(PermissionModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if resource:
        query = query.filter(PermissionModel.resource == resource)
    if action:
        query = query.filter(PermissionModel.action == action)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    permissions = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "permissions": permissions,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{permission_id}", response_model=Permission)
def get_permission(
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific permission"""
    query = db.query(PermissionModel).filter(PermissionModel.id == permission_id)
    
    # Filter by organization if not admin
    if current_user.role.value not in ["admin", "owner"]:
        query = query.filter(PermissionModel.organization_id == current_user.organization_id)
    
    permission = query.first()
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    
    return permission


@router.put("/{permission_id}", response_model=Permission)
def update_permission(
    permission_id: str,
    permission_data: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a permission (admin only)"""
    # Check if user is admin
    if current_user.role.value not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update permissions"
        )
    
    query = db.query(PermissionModel).filter(PermissionModel.id == permission_id)
    
    # Filter by organization if not admin
    if current_user.role.value not in ["admin", "owner"]:
        query = query.filter(PermissionModel.organization_id == current_user.organization_id)
    
    permission = query.first()
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    
    # Update permission fields
    update_data = permission_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(permission, field, value)
    
    db.commit()
    db.refresh(permission)
    
    return permission


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a permission (admin only)"""
    # Check if user is admin
    if current_user.role.value not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete permissions"
        )
    
    query = db.query(PermissionModel).filter(PermissionModel.id == permission_id)
    
    # Filter by organization if not admin
    if current_user.role.value not in ["admin", "owner"]:
        query = query.filter(PermissionModel.organization_id == current_user.organization_id)
    
    permission = query.first()
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    
    db.delete(permission)
    db.commit()
    
    return None


# Role Permission Endpoints

@router.post("/role-permissions/", response_model=RolePermission, status_code=status.HTTP_201_CREATED)
def create_role_permission(
    role_permission_data: RolePermissionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Assign a permission to a role (admin only)"""
    # Check if user is admin
    if current_user.role.value not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can assign permissions"
        )
    
    # Verify permission exists
    permission = db.query(PermissionModel).filter(PermissionModel.id == role_permission_data.permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    
    new_role_permission = RolePermissionModel(
        id=str(uuid.uuid4()),
        role=role_permission_data.role,
        permission_id=role_permission_data.permission_id,
        organization_id=current_user.organization_id
    )
    
    db.add(new_role_permission)
    db.commit()
    db.refresh(new_role_permission)
    
    return new_role_permission


@router.get("/role-permissions/", response_model=RolePermissionListResponse)
def get_role_permissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all role permissions with filtering and pagination"""
    # Build query
    query = db.query(RolePermissionModel).filter(
        RolePermissionModel.organization_id == current_user.organization_id
    )
    
    # Apply filters
    if role:
        query = query.filter(RolePermissionModel.role == role)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    role_permissions = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "role_permissions": role_permissions,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/role-permissions/{role_permission_id}", response_model=RolePermission)
def get_role_permission(
    role_permission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific role permission"""
    role_permission = db.query(RolePermissionModel).filter(
        RolePermissionModel.id == role_permission_id,
        RolePermissionModel.organization_id == current_user.organization_id
    ).first()
    
    if not role_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role permission not found"
        )
    
    return role_permission


@router.delete("/role-permissions/{role_permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_permission(
    role_permission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a role permission (admin only)"""
    # Check if user is admin
    if current_user.role.value not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can remove permissions"
        )
    
    role_permission = db.query(RolePermissionModel).filter(
        RolePermissionModel.id == role_permission_id,
        RolePermissionModel.organization_id == current_user.organization_id
    ).first()
    
    if not role_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role permission not found"
        )
    
    db.delete(role_permission)
    db.commit()
    
    return None


@router.get("/my-permissions/", response_model=UserPermissionsResponse)
def get_my_permissions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get current user's permissions"""
    # Get role permissions for user's role
    role_permissions = db.query(RolePermissionModel).filter(
        RolePermissionModel.role == current_user.role.value,
        RolePermissionModel.organization_id == current_user.organization_id
    ).all()
    
    # Get permission names
    permission_ids = [rp.permission_id for rp in role_permissions]
    permissions = db.query(PermissionModel).filter(PermissionModel.id.in_(permission_ids)).all()
    permission_names = [p.name for p in permissions]
    
    return {
        "permissions": permission_names,
        "role": current_user.role.value
    }
