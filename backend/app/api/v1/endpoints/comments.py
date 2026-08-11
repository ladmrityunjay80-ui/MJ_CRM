"""
Comment Endpoints
CRUD operations for team collaboration comments
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.comment import CommentCreate, CommentUpdate, Comment, CommentWithUser, CommentListResponse
from app.models.user import User as UserModel
from app.models.comment import Comment as CommentModel

router = APIRouter()


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new comment"""
    new_comment = CommentModel(
        id=str(uuid.uuid4()),
        content=comment_data.content,
        entity_type=comment_data.entity_type,
        entity_id=comment_data.entity_id,
        parent_id=comment_data.parent_id,
        mentions=json.dumps(comment_data.mentions) if comment_data.mentions else None,
        organization_id=current_user.organization_id,
        user_id=current_user.id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment


@router.get("/", response_model=CommentListResponse)
def get_comments(
    entity_type: str = Query(..., description="Entity type to filter comments"),
    entity_id: str = Query(..., description="Entity ID to filter comments"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get comments for a specific entity with pagination"""
    # Build query
    query = db.query(CommentModel).filter(
        CommentModel.organization_id == current_user.organization_id,
        CommentModel.entity_type == entity_type,
        CommentModel.entity_id == entity_id,
        CommentModel.parent_id.is_(None)  # Only top-level comments
    )
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    comments = query.order_by(CommentModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # Add user details
    comments_with_user = []
    for comment in comments:
        comment_dict = comment.__dict__.copy()
        comment_dict['user_name'] = current_user.full_name
        comment_dict['user_email'] = current_user.email
        comments_with_user.append(CommentWithUser(**comment_dict))
    
    return {
        "comments": comments_with_user,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{comment_id}", response_model=Comment)
def get_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific comment"""
    comment = db.query(CommentModel).filter(
        CommentModel.id == comment_id,
        CommentModel.organization_id == current_user.organization_id
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    return comment


@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update a comment"""
    comment = db.query(CommentModel).filter(
        CommentModel.id == comment_id,
        CommentModel.organization_id == current_user.organization_id
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Only allow user to update their own comments
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own comments"
        )
    
    # Update comment fields
    update_data = comment_data.model_dump(exclude_unset=True)
    
    if "mentions" in update_data and update_data["mentions"] is not None:
        update_data["mentions"] = json.dumps(update_data["mentions"])
    
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    db.commit()
    db.refresh(comment)
    
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete a comment"""
    comment = db.query(CommentModel).filter(
        CommentModel.id == comment_id,
        CommentModel.organization_id == current_user.organization_id
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Only allow user to delete their own comments
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )
    
    db.delete(comment)
    db.commit()
    
    return None


@router.get("/{comment_id}/replies", response_model=CommentListResponse)
def get_comment_replies(
    comment_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get replies to a specific comment"""
    # Build query
    query = db.query(CommentModel).filter(
        CommentModel.organization_id == current_user.organization_id,
        CommentModel.parent_id == comment_id
    )
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    comments = query.order_by(CommentModel.created_at.asc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # Add user details
    comments_with_user = []
    for comment in comments:
        comment_dict = comment.__dict__.copy()
        comment_dict['user_name'] = current_user.full_name
        comment_dict['user_email'] = current_user.email
        comments_with_user.append(CommentWithUser(**comment_dict))
    
    return {
        "comments": comments_with_user,
        "total": total,
        "page": page,
        "page_size": page_size
    }
