"""
Authentication Endpoints
Handles user registration, login, and token management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.schemas.user import UserCreate, User, UserLogin, Token
from app.models.user import User as UserModel
from app.models.organization import Organization as OrganizationModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    """Dependency to get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create organization if not provided
    organization_id = user_data.organization_id
    if not organization_id:
        # Create a new organization for the user
        new_org = OrganizationModel(
            id=str(uuid.uuid4()),
            name=f"{user_data.full_name}'s Organization",
            slug=f"{user_data.full_name.lower().replace(' ', '-')}-{str(uuid.uuid4())[:8]}"
        )
        db.add(new_org)
        db.commit()
        db.refresh(new_org)
        organization_id = new_org.id
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = UserModel(
        id=str(uuid.uuid4()),
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        phone=user_data.phone,
        role=user_data.role,
        organization_id=organization_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    # Find user by email
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id, "email": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=User)
def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    """Get current user information"""
    return current_user
