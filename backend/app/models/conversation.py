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
