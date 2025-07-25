"""
User model with demo role switching capabilities
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    """Enhanced User model with demo role support"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Role management for demo
    role = Column(String, default="student")  # 'student', 'educator', 'admin', 'universal'
    demo_active_role = Column(String, nullable=True)  # Current demo role for 'universal' users
    previous_demo_role = Column(String, nullable=True)  # For role switching history
    
    # Onboarding and profile
    onboarding_data = Column(Text)  # JSON data from onboarding
    learning_profile = Column(Text)  # JSON learning style data
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    memory_summaries = relationship("MemorySummary", back_populates="user", cascade="all, delete-orphan")
    
    def get_effective_role(self):
        """Get the role user is currently acting as (for demo switching)"""
        if self.role == "universal" and self.demo_active_role:
            return self.demo_active_role
        return self.role
    
    def can_access_role(self, target_role: str) -> bool:
        """Check if user can access a specific role"""
        if self.role == "universal":
            return True  # Universal demo users can access any role
        return self.role == target_role
    
    def switch_demo_role(self, new_role: str) -> bool:
        """Switch demo role if user has universal access"""
        if self.role != "universal":
            return False
        
        valid_roles = ["student", "educator", "admin"]
        if new_role not in valid_roles:
            return False
            
        self.previous_demo_role = self.demo_active_role or self.role
        self.demo_active_role = new_role
        return True

class OnboardingSurvey(Base, TimestampMixin):
    """Onboarding survey model for learning style assessment"""
    __tablename__ = "onboarding_surveys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to User
    learning_style = Column(String)  # visual, auditory, kinesthetic, reading
    preferred_pace = Column(String)  # slow, medium, fast
    background_info = Column(Text)
    goals = Column(Text)
    interaction_preference = Column(String)  # questions, examples, practice
    motivation_level = Column(String)
    time_availability = Column(String)
