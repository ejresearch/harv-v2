"""
Authentication endpoints
Clean implementation of user registration and login
"""

from datetime import timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from ..core.database import get_db
from ..core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    verify_token
)
from ..core.config import settings
from ..models.user import User

router = APIRouter()
security = HTTPBearer()

# Request/Response schemas
class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr  
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

@router.post("/register", response_model=Token)
async def register(user_data: UserRegistration, db: Session = Depends(get_db)):
    """
    Register new user
    Creates account and returns authentication token
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email.lower(),
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        name=new_user.name,
        email=new_user.email
    )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    User login
    Authenticates user and returns access token
    """
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email.lower()).first()
    
    # Verify user and password
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        name=user.name,
        email=user.email
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current user information
    Protected endpoint requiring authentication
    """
    # Verify token and get user ID
    try:
        payload = verify_token(token.credentials)
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active
    )
