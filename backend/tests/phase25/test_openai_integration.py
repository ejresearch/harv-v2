"""
Phase 2.5 Testing Suite - OpenAI Integration Tests
Comprehensive tests for memory + OpenAI + WebSocket integration
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from app.services.openai_service import OpenAIService
from app.services.memory_service import EnhancedMemoryService

class TestOpenAIIntegration:
    """Test OpenAI service integration with enhanced memory"""
    
    @pytest.fixture
    def openai_service(self):
        return OpenAIService()
    
    @pytest.fixture
    def sample_memory_context(self):
        return """
        User Learning Profile: Visual learner, intermediate level
        Module Context: Communication skills, Socratic mode active
        Conversation State: Discussing effective communication techniques
        Knowledge Connections: Previous learning in modules 1-2
        """
    
    @pytest.mark.asyncio
    async def test_socratic_response_generation(self, openai_service, sample_memory_context):
        """Test Socratic response generation with memory context"""
        
        with patch('openai.ChatCompletion.acreate') as mock_openai:
            # Mock OpenAI response
            mock_openai.return_value = Mock(
                choices=[Mock(message=Mock(content="What do you think makes communication effective?"))],
                usage=Mock(prompt_tokens=100, completion_tokens=50, total_tokens=150)
            )
            
            response = await openai_service.generate_socratic_response(
                enhanced_memory_context=sample_memory_context,
                user_message="How can I improve my communication?",
                conversation_history=[],
                module_id=1
            )
            
            assert response.success == True
            assert "?" in response.response  # Should contain questions
            assert response.socratic_analysis.question_count > 0
            assert response.token_usage.total_tokens == 150
    
    @pytest.mark.asyncio
    async def test_socratic_compliance_analysis(self, openai_service):
        """Test Socratic methodology compliance analysis"""
        
        # Test high compliance response
        high_compliance_response = "What do you think makes communication effective? How might you apply this in your daily interactions? Can you think of examples?"
        
        analysis = await openai_service._analyze_socratic_compliance(
            high_compliance_response, "How to communicate better?"
        )
        
        assert analysis.socratic_compliance == "HIGH"
        assert analysis.question_count >= 3
        assert analysis.effectiveness_score > 0.8
        assert not analysis.has_direct_answers
    
    @pytest.mark.asyncio
    async def test_demo_mode_functionality(self):
        """Test demo mode when OpenAI API key is not configured"""
        
        demo_service = OpenAIService()
        demo_service.demo_mode = True
        
        response = await demo_service.generate_socratic_response(
            enhanced_memory_context="Demo context",
            user_message="Test question",
            conversation_history=[],
            module_id=1
        )
        
        assert response.success == True
        assert response.token_usage.model_used == "demo-mode"
        assert "?" in response.response

class TestMemoryOpenAIIntegration:
    """Test integration between memory system and OpenAI"""
    
    @pytest.mark.asyncio
    async def test_complete_integration_flow(self):
        """Test complete flow: memory assembly -> OpenAI -> response"""
        
        # This would test the full integration
        # Requires database setup and mocking
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
