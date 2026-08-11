"""
User Endpoints
CRUD operations for users
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.user import UserCreate, UserUpdate, User, UserListResponse
from app.models.user import User as UserModel

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new user (admin/manager only)"""
    # Check permissions
    if current_user.role not in ["admin", "manager", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create users"
        )
    
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    from app.core.security import get_password_hash
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = UserModel(
        id=str(uuid.uuid4()),
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        phone=user_data.phone,
        role=user_data.role,
        organization_id=user_data.organization_id or current_user.organization_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/", response_model=UserListResponse)
def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all users in the organization"""
    # Build query
    query = db.query(UserModel).filter(UserModel.organization_id == current_user.organization_id)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "users": users,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific user"""
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.organization_id == current_user.organization_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a user"""
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.organization_id == current_user.organization_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if current_user.role not in ["admin", "manager", "owner"] and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    # Update user fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a user (admin/manager only)"""
    if current_user.role not in ["admin", "manager", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete users"
        )
    
    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.organization_id == current_user.organization_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return None
