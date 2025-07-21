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
