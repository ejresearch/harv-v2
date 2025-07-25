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
