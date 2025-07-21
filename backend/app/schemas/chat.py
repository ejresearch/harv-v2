"""
Chat API Schemas - Phase 2.5
Type-safe models for enhanced chat with memory integration
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """Request for chat with enhanced memory"""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    include_memory: bool = Field(True, description="Include 4-layer memory context")
    
class SocraticAnalysis(BaseModel):
    """Analysis of Socratic teaching effectiveness"""
    question_count: int = Field(..., description="Number of questions in response")
    socratic_compliance: str = Field(..., description="high/moderate/low")
    engagement_level: str = Field(..., description="Student engagement assessment")
    teaching_approach: str = Field(..., description="questioning/explanatory/mixed")
    fallback: bool = Field(False, description="Whether fallback response was used")

class MemoryMetrics(BaseModel):
    """Metrics for memory system usage"""
    context_chars: int = Field(..., description="Characters of memory context used")
    layers_active: int = Field(..., description="Number of active memory layers")
    optimization_score: float = Field(..., description="Context optimization score")

class ModelInfo(BaseModel):
    """Information about AI model usage"""
    model: str = Field(..., description="OpenAI model used")
    tokens: Dict[str, int] = Field(default_factory=dict, description="Token usage stats")
    success: bool = Field(..., description="Whether OpenAI call succeeded")

class ChatResponse(BaseModel):
    """Response from enhanced chat system"""
    message: str = Field(..., description="AI tutor response")
    conversation_id: str = Field(..., description="Conversation identifier")
    module_id: int = Field(..., description="Learning module ID")
    enhanced_memory_used: bool = Field(..., description="Whether 4-layer memory was used")
    memory_metrics: MemoryMetrics
    socratic_analysis: SocraticAnalysis  
    model_info: ModelInfo
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class ConversationCreateResponse(BaseModel):
    """Response for new conversation creation"""
    conversation_id: str
    module_id: int
    title: str
    created_at: str
