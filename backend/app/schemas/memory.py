"""
Memory System Schemas - Phase 2 Data Validation
Pydantic models for enhanced memory API endpoints

File: backend/app/schemas/memory.py
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

# === REQUEST MODELS ===

class MemoryContextRequest(BaseModel):
    """Request model for enhanced memory chat"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message for AI tutor")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is mass communication?",
                "conversation_id": "conv-123-456"
            }
        }

class MemorySummaryCreate(BaseModel):
    """Request model for saving learning memory summaries"""
    module_id: int = Field(..., description="Module ID where learning occurred")
    what_learned: str = Field(..., min_length=10, max_length=500, description="Key concepts or insights learned")
    how_learned: str = Field(..., min_length=10, max_length=500, description="Learning process or methodology")
    connections_made: str = Field(..., min_length=10, max_length=500, description="Connections to other concepts")
    confidence_level: float = Field(0.8, ge=0.0, le=1.0, description="Confidence in learning (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "module_id": 1,
                "what_learned": "Mass communication involves reaching large audiences through media channels",
                "how_learned": "Discovered through Socratic questioning about daily media experiences",
                "connections_made": "Connects to interpersonal communication from Module 2",
                "confidence_level": 0.85
            }
        }

class UserProgressUpdate(BaseModel):
    """Request model for updating user learning progress"""
    completion_percentage: float = Field(..., ge=0.0, le=100.0, description="Module completion percentage")
    insights_gained: int = Field(0, ge=0, description="Number of new insights gained")
    questions_asked: int = Field(0, ge=0, description="Number of questions asked by AI")
    
    class Config:
        json_schema_extra = {
            "example": {
                "completion_percentage": 45.5,
                "insights_gained": 3,
                "questions_asked": 8
            }
        }

# === RESPONSE MODELS ===

class LearningProfile(BaseModel):
    """User learning profile data"""
    style: str = Field(..., description="Learning style (visual, auditory, kinesthetic, adaptive)")
    pace: str = Field(..., description="Learning pace preference (slow, moderate, fast)")
    background: str = Field(..., description="Background knowledge level")
    goals: List[str] = Field(default_factory=list, description="Learning goals")

class ModuleInfo(BaseModel):
    """Module information for memory context"""
    id: int
    title: str
    description: str
    objectives: str
    progress: float = Field(..., ge=0.0, le=100.0)

class TeachingConfiguration(BaseModel):
    """Teaching configuration for Socratic methodology"""
    system_prompt: str
    module_prompt: str
    socratic_intensity: str = "moderate"
    allowed_topics: List[str] = Field(default_factory=list)
    memory_context_template: Optional[str] = None
    cross_module_references: Optional[str] = None

class ConversationAnalysis(BaseModel):
    """Conversation pattern analysis results"""
    topic_focus: str
    engagement_level: str
    question_count: Optional[int] = 0
    user_response_length: Optional[float] = 0.0

class PriorModuleInsight(BaseModel):
    """Prior learning insights from other modules"""
    module_id: int
    module_title: str
    key_insight: str
    message_count: int
    last_activity: Optional[str] = None
    connection_strength: float = Field(..., ge=0.0, le=1.0)

class ContextMetrics(BaseModel):
    """Memory context assembly metrics"""
    total_chars: int = Field(..., ge=0)
    word_count: int = Field(..., ge=0)
    optimization_score: float = Field(..., ge=0.0, le=1.0)
    layer_breakdown: Dict[str, int] = Field(default_factory=dict)
    timestamp: str

class DatabaseStatus(BaseModel):
    """Database loading status for memory layers"""
    user_found: bool
    module_found: bool
    onboarding_loaded: bool
    module_config_loaded: bool
    conversation_analyzed: bool
    cross_module_connections: bool

class SystemData(BaseModel):
    """Layer 1: System memory data"""
    learning_profile: LearningProfile
    cross_module_mastery: List[Dict[str, Any]] = Field(default_factory=list)
    learning_strengths: List[str] = Field(default_factory=list)
    mastered_concepts: List[str] = Field(default_factory=list)

class ModuleData(BaseModel):
    """Layer 2: Module-specific memory data"""
    module_info: ModuleInfo
    teaching_configuration: TeachingConfiguration
    socratic_strategy: str
    context_rules: Dict[str, bool] = Field(default_factory=dict)

class ConversationData(BaseModel):
    """Layer 3: Real-time conversation memory data"""
    state: str
    message_history: List[Dict[str, Any]] = Field(default_factory=list)
    dialogue_context: str
    conversation_analysis: ConversationAnalysis
    conversation_id: Optional[str] = None

class PriorKnowledge(BaseModel):
    """Layer 4: Cross-module prior knowledge data"""
    prior_module_insights: List[PriorModuleInsight] = Field(default_factory=list)
    mastered_concepts: List[str] = Field(default_factory=list)
    cross_module_connections: List[str] = Field(default_factory=list)

class MemoryLayers(BaseModel):
    """Complete 4-layer memory structure"""
    system_data: SystemData
    module_data: ModuleData
    conversation_data: ConversationData
    prior_knowledge: PriorKnowledge

class MemoryContextResponse(BaseModel):
    """Complete enhanced memory context response"""
    assembled_prompt: str = Field(..., description="Optimized prompt with 4-layer memory context")
    context_metrics: ContextMetrics
    memory_layers: MemoryLayers
    conversation_id: Optional[str] = None
    database_status: DatabaseStatus
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "assembled_prompt": "=== HARV ENHANCED MEMORY CONTEXT ===\nSTUDENT PROFILE: adaptive learner, moderate pace, beginner background...",
                "context_metrics": {
                    "total_chars": 1543,
                    "word_count": 287,
                    "optimization_score": 0.77,
                    "layer_breakdown": {
                        "system_data": 1,
                        "module_data": 1,
                        "conversation_data": 1,
                        "prior_knowledge": 1
                    },
                    "timestamp": "2025-07-21T12:00:00Z"
                },
                "database_status": {
                    "user_found": True,
                    "module_found": True,
                    "onboarding_loaded": True,
                    "module_config_loaded": True,
                    "conversation_analyzed": True,
                    "cross_module_connections": True
                }
            }
        }

class MemorySummaryResponse(BaseModel):
    """Response model for memory summary operations"""
    status: str = Field(..., description="Operation status")
    message: str = Field(..., description="Human-readable message")
    user_id: int
    module_id: int
    timestamp: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "saved",
                "message": "Memory summary saved successfully",
                "user_id": 1,
                "module_id": 3,
                "timestamp": "2025-07-21T12:00:00Z"
            }
        }

# === ENHANCED CHAT MODELS ===

class EnhancedChatRequest(BaseModel):
    """Request model for chat with enhanced memory"""
    module_id: int = Field(..., description="Learning module ID")
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuity")
    memory_options: Optional[Dict[str, bool]] = Field(
        default_factory=lambda: {
            "include_system_memory": True,
            "include_module_progress": True,
            "include_conversation_history": True,
            "include_cross_module_connections": True
        },
        description="Memory inclusion options"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "module_id": 1,
                "message": "I'm confused about the difference between mass media and social media",
                "conversation_id": "conv-abc-123",
                "memory_options": {
                    "include_system_memory": True,
                    "include_module_progress": True,
                    "include_conversation_history": True,
                    "include_cross_module_connections": True
                }
            }
        }

class SocraticAnalysis(BaseModel):
    """Analysis of Socratic teaching effectiveness"""
    question_type: str = Field(..., description="Type of question used (exploratory, clarifying, assumption)")
    engagement_level: str = Field(..., description="Student engagement level (low, moderate, high)")
    learning_objective: str = Field(..., description="Current learning objective focus")
    next_strategy: Optional[str] = Field(None, description="Recommended next teaching strategy")

class MemoryMetrics(BaseModel):
    """Metrics for memory context usage in chat"""
    context_used: int = Field(..., description="Characters of memory context used")
    layers_active: int = Field(..., description="Number of memory layers actively contributing")
    connections_found: int = Field(..., description="Cross-module connections identified")
    optimization_score: float = Field(..., ge=0.0, le=1.0, description="Memory context optimization score")

class EnhancedChatResponse(BaseModel):
    """Response model for enhanced chat with memory"""
    reply: str = Field(..., description="AI tutor response using Socratic methodology")
    conversation_id: str = Field(..., description="Conversation ID for continuity")
    module_id: int = Field(..., description="Learning module ID")
    memory_metrics: MemoryMetrics
    socratic_analysis: SocraticAnalysis
    enhanced: bool = Field(True, description="Indicates enhanced memory was used")
    timestamp: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "reply": "That's an excellent question! What experiences have you had with both mass media and social media today? Can you think of specific examples where you encountered each?",
                "conversation_id": "conv-abc-123",
                "module_id": 1,
                "memory_metrics": {
                    "context_used": 1543,
                    "layers_active": 4,
                    "connections_found": 2,
                    "optimization_score": 0.85
                },
                "socratic_analysis": {
                    "question_type": "exploratory",
                    "engagement_level": "high", 
                    "learning_objective": "conceptual_understanding",
                    "next_strategy": "guide_to_examples"
                },
                "enhanced": True,
                "timestamp": "2025-07-21T12:00:00Z"
            }
        }

# === VALIDATION MODELS ===

class MemorySystemHealth(BaseModel):
    """Memory system health check response"""
    status: str = Field(..., description="Overall system health status")
    memory_system: str = Field(..., description="Memory system operational status")
    database: str = Field(..., description="Database connectivity status")
    users_in_system: Optional[int] = Field(None, description="Number of users in system")
    timestamp: str = Field(..., description="Health check timestamp")
    error: Optional[str] = Field(None, description="Error message if unhealthy")

# === VALIDATORS ===

class MemoryContextRequest(MemoryContextRequest):
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or only whitespace')
        return v.strip()

class MemorySummaryCreate(MemorySummaryCreate):
    @validator('what_learned', 'how_learned', 'connections_made')
    def validate_learning_fields(cls, v):
        if not v.strip():
            raise ValueError('Learning fields cannot be empty')
        return v.strip()
    
    @validator('confidence_level')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence level must be between 0.0 and 1.0')
        return v

class UserProgressUpdate(UserProgressUpdate):
    @validator('completion_percentage')
    def validate_completion(cls, v):
        if not 0.0 <= v <= 100.0:
            raise ValueError('Completion percentage must be between 0.0 and 100.0')
        return v
