"""
Memory System Pydantic Schemas
Type-safe request/response models for enhanced memory API
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class MemoryContextResponse(BaseModel):
    """Complete memory context response"""
    assembled_prompt: str = Field(..., description="Final assembled prompt for AI")
    context_size: int = Field(..., description="Total context size in characters")
    layers_active: int = Field(..., description="Number of successfully loaded layers")
    assembly_timestamp: str = Field(..., description="When context was assembled")
    success: bool = Field(..., description="Whether assembly was successful")
    layer1_profile: Dict[str, Any]
    layer2_module: Dict[str, Any]
    layer3_conversation: Dict[str, Any]
    layer4_connections: Dict[str, Any]
    error: Optional[str] = Field(None, description="Error message if assembly failed")

class MemoryHealthResponse(BaseModel):
    """Memory system health check response"""
    status: str = Field(..., description="Overall system status")
    memory_service: str = Field(..., description="Memory service status")
    database: str = Field(..., description="Database connectivity status")
    users_in_system: int = Field(..., description="Total users in system")
    layers_available: int = Field(4, description="Memory layers available")
    timestamp: str = Field(..., description="Health check timestamp")
