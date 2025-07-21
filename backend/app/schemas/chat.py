"""
Chat API Schemas - Phase 2.5 Complete
Type-safe models for live AI tutoring with memory integration
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    """Request for chat with enhanced memory"""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is mass communication?",
                "conversation_id": "conv-123-456"
            }
        }

class SocraticAnalysis(BaseModel):
    """Analysis of Socratic teaching effectiveness"""
    question_count: int = Field(..., description="Number of questions in response")
    socratic_compliance: str = Field(..., description="high/moderate/low")
    engagement_level: str = Field(..., description="Student engagement assessment")
    teaching_approach: str = Field(..., description="questioning/explanatory/mixed")
    has_direct_answers: bool = Field(False, description="Whether response contains direct answers")
    fallback: bool = Field(False, description="Whether fallback response was used")

class MemoryMetrics(BaseModel):
    """Metrics for memory context usage in chat"""
    context_chars: int = Field(..., description="Characters of memory context used")
    layers_active: int = Field(..., description="Number of active memory layers")
    optimization_score: float = Field(..., description="Context optimization score")

class ModelInfo(BaseModel):
    """Information about AI model usage"""
    model: str = Field(..., description="OpenAI model used")
    tokens: Dict[str, int] = Field(default_factory=dict, description="Token usage stats")
    success: bool = Field(..., description="Whether OpenAI call succeeded")

class ChatResponse(BaseModel):
    """Response from live AI tutor with memory integration"""
    message: str = Field(..., description="AI tutor Socratic response")
    conversation_id: Optional[str] = Field(None, description="Conversation identifier")
    module_id: int = Field(..., description="Learning module ID")
    enhanced_memory_used: bool = Field(True, description="Whether 4-layer memory was used")
    memory_metrics: MemoryMetrics
    socratic_analysis: SocraticAnalysis  
    model_info: ModelInfo
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "That's a fascinating question! What forms of communication do you encounter in your daily life? Can you think of examples where information reaches many people at once?",
                "conversation_id": "conv-abc-123",
                "module_id": 1,
                "enhanced_memory_used": True,
                "memory_metrics": {
                    "context_chars": 1543,
                    "layers_active": 4,
                    "optimization_score": 0.85
                },
                "socratic_analysis": {
                    "question_count": 3,
                    "socratic_compliance": "high", 
                    "engagement_level": "high",
                    "teaching_approach": "questioning"
                },
                "model_info": {
                    "model": "gpt-4",
                    "success": True
                },
                "timestamp": "2025-07-21T13:00:00Z"
            }
        }
