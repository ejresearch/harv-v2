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
