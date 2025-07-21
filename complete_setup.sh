#!/bin/bash

echo "🚀 HARV v2.0 - COMPLETE SETUP SCRIPT"
echo "====================================="
echo "Creating ALL files with ALL code..."
echo ""

# Make sure we're in the harv-v2 directory
if [[ ! -d "backend" || ! -d "frontend" ]]; then
    echo "❌ Error: Run this from the harv-v2 directory"
    echo "Expected directory structure with backend/ and frontend/ folders"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo "✅ Detected harv-v2 project structure"
echo ""

# =============================================================================
# BACKEND CORE FILES
# =============================================================================

echo "🔧 Creating backend core files..."

# backend/app/core/config.py
cat > backend/app/core/config.py << 'EOF'
"""
Core configuration for Harv v2.0
Clean, production-ready settings management
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets

class Settings(BaseSettings):
    # App Info
    app_name: str = "Harv v2.0 - Intelligent Tutoring System"
    version: str = "2.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./harv_v2.db"

    # Security
    secret_key: str = secrets.token_urlsafe(32)  # Auto-generate if not provided
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # CORS - Allow frontend access
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # API Settings
    api_prefix: str = "/api/v1"
    
    # Memory System Settings
    memory_max_context_length: int = 4000
    memory_fallback_enabled: bool = True
    
    # Socratic Teaching Settings
    socratic_mode_enabled: bool = True
    prevent_direct_answers: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
EOF

# backend/app/core/database.py
cat > backend/app/core/database.py << 'EOF'
"""
Database configuration and session management
Clean SQLAlchemy setup with proper connection handling
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from .config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug  # SQL query logging in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    Ensures proper session cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables
    Used for initial setup and testing
    """
    Base.metadata.create_all(bind=engine)
EOF

# backend/app/core/security.py
cat > backend/app/core/security.py << 'EOF'
"""
Security utilities for authentication and password handling
Clean JWT and password hashing implementation
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    Clean implementation with proper expiration
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify JWT token and return payload
    Raises HTTPException if invalid
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
EOF

echo "✅ Core files created"

# =============================================================================
# DATABASE MODELS
# =============================================================================

echo "🗄️  Creating database models..."

# backend/app/models/__init__.py
cat > backend/app/models/__init__.py << 'EOF'
"""
Database models for Harv v2.0
Clean, well-structured models preserving your existing schema
"""

from .base import Base
from .user import User, OnboardingSurvey
from .course import Module
from .conversation import Conversation, Message
from .memory import MemorySummary, UserProgress

__all__ = [
    "Base",
    "User", 
    "OnboardingSurvey",
    "Module",
    "Conversation",
    "Message", 
    "MemorySummary",
    "UserProgress"
]
EOF

# backend/app/models/base.py
cat > backend/app/models/base.py << 'EOF'
"""
Base model class with common functionality
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
EOF

# backend/app/models/user.py
cat > backend/app/models/user.py << 'EOF'
"""
User-related models
Ported from your existing schema with enhancements
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    """
    User model - core user information
    Compatible with your existing database
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    onboarding_data = Column(Text)  # JSON string for onboarding responses
    is_active = Column(Boolean, default=True)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    memory_summaries = relationship("MemorySummary", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    onboarding_survey = relationship("OnboardingSurvey", back_populates="user", uselist=False, cascade="all, delete-orphan")

class OnboardingSurvey(Base, TimestampMixin):
    """
    Onboarding survey responses
    Used by the memory system for personalization
    """
    __tablename__ = "onboarding_surveys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Survey responses (used by memory system)
    learning_style = Column(String)  # "visual", "auditory", "kinesthetic", "reading"
    prior_experience = Column(Text)  # JSON string
    goals = Column(Text)
    preferred_pace = Column(String)  # "slow", "medium", "fast"
    interaction_preference = Column(String)  # "questions", "examples", "practice"
    
    # Additional context for memory system
    background_info = Column(Text)
    motivation_level = Column(String)
    time_availability = Column(String)
    
    # Relationship
    user = relationship("User", back_populates="onboarding_survey")
EOF

# backend/app/models/course.py
cat > backend/app/models/course.py << 'EOF'
"""
Course and module models
Your 15 communication modules with Socratic configuration
"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Module(Base, TimestampMixin):
    """
    Learning module model
    Contains your 15 communication modules with Socratic prompts
    """
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Socratic teaching configuration
    system_prompt = Column(Text, nullable=False)  # Core Socratic instructions
    module_prompt = Column(Text)  # Module-specific guidance
    learning_objectives = Column(Text)  # What students should discover
    
    # Content and resources
    resources = Column(Text)  # Additional learning materials
    system_corpus = Column(Text)  # Background knowledge
    module_corpus = Column(Text)  # Module-specific knowledge
    dynamic_corpus = Column(Text)  # Adaptive content
    
    # Configuration
    difficulty_level = Column(String, default="intermediate")
    estimated_duration = Column(Integer)  # Minutes
    prerequisites = Column(Text)  # JSON list of required modules
    is_active = Column(Boolean, default=True)
    
    # API configuration (for future extensibility)
    api_endpoint = Column(String, default="https://api.openai.com/v1/chat/completions")
    
    # Relationships
    conversations = relationship("Conversation", back_populates="module")
    memory_summaries = relationship("MemorySummary", back_populates="module")
    progress_records = relationship("UserProgress", back_populates="module")
EOF

# backend/app/models/conversation.py
cat > backend/app/models/conversation.py << 'EOF'
"""
Conversation and message models
Handles chat history with memory integration
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Conversation(Base, TimestampMixin):
    """
    Conversation session between user and Harv
    Enhanced with memory tracking
    """
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String, default="New Conversation")
    
    # Legacy compatibility - JSON storage for old conversations
    messages_json = Column(Text)  # For backward compatibility
    
    # Memory and learning tracking
    memory_summary = Column(Text)  # What was learned in this conversation
    current_grade = Column(String)  # Understanding level assessment
    learning_progress = Column(JSON)  # Detailed progress metrics
    
    # Status
    is_active = Column(Boolean, default=True)
    finalized = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    module = relationship("Module", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base, TimestampMixin):
    """
    Individual message within a conversation
    Supports both user and assistant messages
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    
    # Memory system context (optional)
    memory_context = Column(JSON)  # The memory context used to generate this message
    socratic_analysis = Column(JSON)  # Analysis of Socratic effectiveness
    
    # Message metadata
    token_count = Column(Integer)
    response_time = Column(Integer)  # Milliseconds
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")
EOF

# backend/app/models/memory.py
cat > backend/app/models/memory.py << 'EOF'
"""
Memory system models
Supports your enhanced 4-layer memory architecture
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class MemorySummary(Base, TimestampMixin):
    """
    Learning memory summaries for cross-module persistence
    Core component of your enhanced memory system
    """
    __tablename__ = "memory_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    
    # Memory content (used by your memory system)
    what_learned = Column(Text, nullable=False)  # Key concepts discovered
    how_learned = Column(Text)  # Learning process and method
    connections_made = Column(Text)  # Links to other concepts
    
    # Memory metadata
    confidence_level = Column(Float, default=0.5)  # 0.0 to 1.0
    retention_strength = Column(Float, default=0.8)  # How well remembered
    last_accessed = Column(Text)  # When this memory was last used
    
    # Context for memory assembly
    context_data = Column(JSON)  # Additional context for memory system
    
    # Relationships
    user = relationship("User", back_populates="memory_summaries")
    module = relationship("Module", back_populates="memory_summaries")

class UserProgress(Base, TimestampMixin):
    """
    User progress tracking per module
    Supports learning analytics and memory system
    """
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    
    # Progress metrics
    completion_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    mastery_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    
    # Learning statistics
    total_conversations = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    time_spent = Column(Integer, default=0)  # Total minutes
    
    # Socratic effectiveness metrics
    questions_asked = Column(Integer, default=0)
    insights_gained = Column(Integer, default=0)
    connections_made = Column(Integer, default=0)
    
    # Status
    is_completed = Column(Boolean, default=False)
    current_focus = Column(Text)  # What the user is currently learning
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    module = relationship("Module", back_populates="progress_records")
EOF

echo "✅ Database models created"

# =============================================================================
# API ENDPOINTS
# =============================================================================

echo "🌐 Creating API endpoints..."

# backend/app/api/__init__.py
cat > backend/app/api/__init__.py << 'EOF'
"""
API package initialization
"""
EOF

# backend/app/api/health.py
cat > backend/app/api/health.py << 'EOF'
"""
Health check endpoints
Essential for monitoring and deployment
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..core.database import get_db
from ..core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "debug": settings.debug
    }

@router.get("/health/database")
async def database_health(db: Session = Depends(get_db)):
    """Database connectivity check"""
    try:
        # Simple query to test database connection
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "database": "healthy",
            "connection": "active",
            "query_result": result
        }
    except Exception as e:
        return {
            "database": "unhealthy", 
            "error": str(e),
            "status_code": 503
        }

@router.get("/health/detailed")  
async def detailed_health(db: Session = Depends(get_db)):
    """Comprehensive health check"""
    health_status = {
        "service": settings.app_name,
        "version": settings.version,
        "status": "healthy",
        "checks": {}
    }
    
    # Database check
    try:
        db.execute(text("SELECT 1")).scalar()
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # OpenAI API key check
    if settings.openai_api_key:
        health_status["checks"]["openai_key"] = "configured"
    else:
        health_status["checks"]["openai_key"] = "missing"
        health_status["status"] = "degraded"
    
    # Memory system check (placeholder for Phase 2)
    health_status["checks"]["memory_system"] = "not_implemented_yet"
    
    return health_status
EOF

# backend/app/api/auth.py
cat > backend/app/api/auth.py << 'EOF'
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
EOF

echo "✅ API endpoints created"

# =============================================================================
# MAIN APPLICATION
# =============================================================================

echo "🚀 Creating main application..."

# backend/app/main.py
cat > backend/app/main.py << 'EOF'
"""
FastAPI application setup for Harv v2.0
Clean, production-ready application structure
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.database import create_tables
from .api import auth, health

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Intelligent tutoring system with enhanced 4-layer memory architecture",
    docs_url="/docs" if settings.debug else None,  # Disable docs in production
    redoc_url="/redoc" if settings.debug else None,
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and perform startup tasks"""
    create_tables()
    print(f"🚀 {settings.app_name} v{settings.version} starting up...")
    print(f"📊 Debug mode: {settings.debug}")
    print(f"🗄️  Database: {settings.database_url}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully"""
    if settings.debug:
        # In debug mode, show the actual error
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc),
                "debug": True
            }
        )
    else:
        # In production, hide error details
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }
        )

# Include API routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix=settings.api_prefix, tags=["Authentication"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "healthy",
        "docs": "/docs" if settings.debug else "Documentation disabled in production"
    }
EOF

echo "✅ Main application created"

# =============================================================================
# UPDATE REQUIREMENTS.TXT
# =============================================================================

echo "📦 Updating requirements.txt..."

cat > backend/requirements.txt << 'EOF'
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# AI Integration
openai==1.3.8
pydantic==2.5.0
pydantic-settings==2.1.0

# Utilities
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1

# Development
black==23.11.0
isort==5.12.0
mypy==1.7.1

# Email validation
email-validator==2.1.0
EOF

# =============================================================================
# UPDATE ENVIRONMENT FILE
# =============================================================================

echo "⚙️ Creating updated .env file..."

cat > backend/.env << 'EOF'
# Database
DATABASE_URL=sqlite:///./harv_v2.db

# Security
SECRET_KEY=super-secret-key-change-this-in-production-please
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-your-openai-key-here

# Development
DEBUG=true
CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]
EOF

echo "✅ Environment file created"

# =============================================================================
# FINAL VERIFICATION
# =============================================================================

echo ""
echo "🔍 Verifying file structure..."

# List all created files
echo "✅ Created files:"
find backend/app -name "*.py" | sort
echo ""

# Check if all key files exist
key_files=(
    "backend/app/core/config.py"
    "backend/app/core/database.py"
    "backend/app/core/security.py"
    "backend/app/models/__init__.py"
    "backend/app/models/base.py"
    "backend/app/models/user.py"
    "backend/app/models/course.py"
    "backend/app/models/conversation.py"
    "backend/app/models/memory.py"
    "backend/app/api/__init__.py"
    "backend/app/api/health.py"
    "backend/app/api/auth.py"
    "backend/app/main.py"
    "backend/requirements.txt"
    "backend/.env"
)

echo "🎯 Verifying key files:"
all_good=true
for file in "${key_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING!"
        all_good=false
    fi
done

echo ""
if [[ "$all_good" == true ]]; then
    echo "🎉 ALL FILES CREATED SUCCESSFULLY!"
    echo "====================================="
    echo ""
    echo "🚀 Next steps:"
    echo "1. ./scripts/dev-setup.sh    # Install dependencies"
    echo "2. Update backend/.env        # Add your OpenAI API key"
    echo "3. ./scripts/start-dev.sh     # Start the server"
    echo ""
    echo "🎯 Expected results:"
    echo "- Backend API: http://localhost:8000"
    echo "- API docs: http://localhost:8000/docs"
    echo "- Health check: http://localhost:8000/health"
    echo ""
    echo "✅ HARV v2.0 FOUNDATION COMPLETE!"
else
    echo "❌ Some files were not created properly."
    echo "Please check the errors above."
fi
