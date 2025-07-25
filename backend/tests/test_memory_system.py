"""
Memory System Integration Tests
Comprehensive testing of 4-layer enhanced memory system
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db, Base
from app.models import User, OnboardingSurvey, Module
from app.services.memory_service import EnhancedMemoryService

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_memory.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Set up test database with sample data"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create test user
    test_user = User(
        email="test@memory.edu",
        hashed_password="$2b$12$test_hash",
        name="Memory Test User",
        is_active=True
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    # Create onboarding survey
    survey = OnboardingSurvey(
        user_id=test_user.id,
        learning_style="visual",
        preferred_pace="moderate",
        goals="Master communication skills",
        interaction_preference="socratic",
        background_info="Student with some experience",
        prior_experience="Basic communication courses",
        communication_challenges="Public speaking anxiety",
        preferred_examples="Business scenarios"
    )
    db.add(survey)
    
    # Create test module
    module = Module(
        id=1,
        title="Test Communication Module",
        description="Module for testing memory system",
        content='{"learning_objectives": ["Test objective 1", "Test objective 2"], "key_concepts": ["Concept A", "Concept B"]}'
    )
    db.add(module)
    
    db.commit()
    db.close()
    
    yield test_user.id
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

class TestMemorySystem:
    """Test suite for enhanced memory system"""
    
    @pytest.mark.asyncio
    async def test_memory_service_initialization(self, setup_database):
        """Test memory service can be initialized"""
        db = TestingSessionLocal()
        memory_service = EnhancedMemoryService(db)
        assert memory_service is not None
        db.close()
    
    @pytest.mark.asyncio
    async def test_layer1_user_profile_assembly(self, setup_database):
        """Test Layer 1: User Profile assembly"""
        user_id = setup_database
        db = TestingSessionLocal()
        memory_service = EnhancedMemoryService(db)
        
        layer1 = await memory_service._assemble_layer1_user_profile(user_id)
        
        assert layer1['layer'] == 'user_profile'
        assert 'Memory Test User' in layer1['content']
        assert 'visual' in layer1['content']
        assert layer1['metadata']['learning_style'] == 'visual'
        
        db.close()
    
    @pytest.mark.asyncio
    async def test_layer2_module_context_assembly(self, setup_database):
        """Test Layer 2: Module Context assembly"""
        db = TestingSessionLocal()
        memory_service = EnhancedMemoryService(db)
        
        layer2 = await memory_service._assemble_layer2_module_context(1)
        
        assert layer2['layer'] == 'module_context'
        assert 'Test Communication Module' in layer2['content']
        assert 'Socratic Teaching Mode' in layer2['content']
        assert layer2['metadata']['socratic_mode'] is True
        
        db.close()
    
    @pytest.mark.asyncio
    async def test_full_memory_context_assembly(self, setup_database):
        """Test complete 4-layer memory context assembly"""
        user_id = setup_database
        db = TestingSessionLocal()
        memory_service = EnhancedMemoryService(db)
        
        context = await memory_service.assemble_memory_context(
            user_id=user_id,
            module_id=1,
            current_message="Test message for memory context"
        )
        
        assert context['success'] is True
        assert context['layers_active'] >= 2  # At least user profile and module context
        assert 'assembled_prompt' in context
        assert len(context['assembled_prompt']) > 0
        assert 'ENHANCED MEMORY CONTEXT' in context['assembled_prompt']
        
        db.close()
    
    def test_memory_health_endpoint(self):
        """Test memory system health endpoint"""
        response = client.get("/api/v1/memory/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert data['layers_available'] == 4

def test_memory_endpoints_without_auth():
    """Test that memory endpoints require authentication"""
    response = client.get("/api/v1/memory/context/1")
    assert response.status_code == 401
    
    response = client.post("/api/v1/memory/chat/1", json={"message": "test"})
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
