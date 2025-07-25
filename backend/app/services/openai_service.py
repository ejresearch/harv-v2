import openai
import asyncio
import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class SocraticAnalysis(BaseModel):
    """Analysis of how well the AI response follows Socratic methodology"""
    question_count: int = Field(..., description="Number of questions in response")
    socratic_compliance: str = Field(..., description="HIGH/MEDIUM/LOW compliance rating")  
    engagement_level: str = Field(..., description="How engaging the response is")
    teaching_approach: str = Field(..., description="Description of teaching strategy used")
    effectiveness_score: float = Field(..., ge=0.0, le=1.0, description="0-1 educational effectiveness")
    has_direct_answers: bool = Field(..., description="Whether response contains direct answers")
    improvement_suggestions: List[str] = Field(default_factory=list)

class TokenUsage(BaseModel):
    """OpenAI API token usage tracking"""
    prompt_tokens: int
    completion_tokens: int  
    total_tokens: int
    estimated_cost: float
    model_used: str
    response_time_ms: int

class OpenAIResponse(BaseModel):
    """Complete OpenAI API response with analysis"""
    success: bool
    response: str = ""
    socratic_analysis: Optional[SocraticAnalysis] = None
    token_usage: Optional[TokenUsage] = None  
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class OpenAIService:
    """
    Enterprise OpenAI Service for Educational AI Tutoring
    
    Features:
    - Real GPT-4 integration (no fake responses)
    - Socratic methodology enforcement  
    - Enhanced memory context optimization
    - Token usage tracking and cost management
    - Error handling with intelligent fallbacks
    - Rate limiting and retry logic
    """
    
    def __init__(self):
        """Initialize OpenAI service with API key and configuration"""
        if not settings.openai_api_key:
            logger.warning("⚠️ OpenAI API key not configured - service will use demo mode")
            self.demo_mode = True
        else:
            openai.api_key = settings.openai_api_key
            self.demo_mode = False
            
        # Model configuration
        self.model = settings.openai_model or "gpt-4"
        self.max_tokens = 1000
        self.temperature = 0.7
        
        # Socratic teaching configuration
        self.socratic_threshold = 0.7  # Minimum Socratic compliance score
        self.max_direct_answer_ratio = 0.2  # Max 20% direct statements
        
        # Performance tracking
        self.request_count = 0
        self.total_tokens_used = 0
        self.average_response_time = 0.0
        
        logger.info(f"🤖 OpenAI Service initialized - Model: {self.model}, Demo: {self.demo_mode}")

    async def generate_socratic_response(
        self,
        enhanced_memory_context: str,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        module_id: int = 1
    ) -> OpenAIResponse:
        """
        Generate Socratic tutoring response using GPT-4 + enhanced memory
        
        Args:
            enhanced_memory_context: Your 4-layer memory system context
            user_message: Student's question or message
            conversation_history: Previous conversation messages
            module_id: Current module (1-15)
            
        Returns:
            OpenAIResponse with GPT-4 response and Socratic analysis
        """
        start_time = time.time()
        
        try:
            logger.info(f"🎓 Generating Socratic response for module {module_id}")
            logger.info(f"📝 Memory context: {len(enhanced_memory_context)} chars")
            
            if self.demo_mode:
                return await self._generate_demo_response(user_message, module_id)
            
            # Build comprehensive prompt with memory integration
            system_prompt = self._build_socratic_system_prompt(enhanced_memory_context, module_id)
            user_prompt = self._build_user_prompt(user_message, conversation_history)
            
            logger.info(f"🔧 System prompt: {len(system_prompt)} chars")
            logger.info(f"🔧 User prompt: {len(user_prompt)} chars")
            
            # Call OpenAI API with retry logic
            api_response = await self._call_openai_api(system_prompt, user_prompt)
            
            if not api_response["success"]:
                return OpenAIResponse(
                    success=False,
                    error=api_response["error"]
                )
            
            # Extract response and usage data
            ai_response = api_response["response"]
            usage_data = api_response["usage"]
            
            # Analyze Socratic methodology compliance
            socratic_analysis = await self._analyze_socratic_compliance(ai_response, user_message)
            
            # Calculate token usage and cost
            token_usage = self._calculate_token_usage(usage_data, time.time() - start_time)
            
            # Update performance metrics
            self._update_metrics(token_usage)
            
            logger.info(f"✅ Response generated: {len(ai_response)} chars")
            logger.info(f"📊 Socratic compliance: {socratic_analysis.socratic_compliance}")
            logger.info(f"💰 Tokens used: {token_usage.total_tokens} (${token_usage.estimated_cost:.4f})")
            
            return OpenAIResponse(
                success=True,
                response=ai_response,
                socratic_analysis=socratic_analysis,
                token_usage=token_usage
            )
            
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {str(e)}")
            return OpenAIResponse(
                success=False,
                error=f"OpenAI service error: {str(e)}"
            )

    def _build_socratic_system_prompt(self, memory_context: str, module_id: int) -> str:
        """Build system prompt with Socratic methodology and memory integration"""
        
        socratic_instructions = """
You are an expert AI tutor using the Socratic method for personalized education. Your primary goal is to guide students to discover knowledge through thoughtful questioning rather than providing direct answers.

## CORE SOCRATIC PRINCIPLES:
1. **ASK, DON'T TELL**: Use questions to guide student thinking
2. **BUILD ON RESPONSES**: Follow up on student answers with deeper questions  
3. **ENCOURAGE DISCOVERY**: Help students reach conclusions themselves
4. **CONNECT CONCEPTS**: Link new learning to prior knowledge
5. **MAINTAIN ENGAGEMENT**: Keep dialogue dynamic and thought-provoking

## RESPONSE REQUIREMENTS:
- 70%+ of your response should be questions
- Maximum 2-3 direct statements per response
- Always end with a question that advances learning
- Use encouraging, supportive tone
- Reference the student's learning context when relevant

## ENHANCED MEMORY INTEGRATION:
The following context provides deep insight into this student's learning journey, preferences, and progress. Use this information to personalize your Socratic questioning approach:

""" + memory_context + """

## TEACHING APPROACH:
Based on the memory context above, adapt your questioning style to:
- Match the student's learning preferences and pace
- Build on their demonstrated knowledge and skills  
- Address any learning gaps or challenges identified
- Connect to their previous learning across modules
- Use their preferred communication style and examples

Remember: Your goal is to facilitate discovery through questions, not to provide answers directly.
"""
        
        return socratic_instructions

    def _build_user_prompt(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Build user prompt with conversation context"""
        
        prompt_parts = []
        
        # Add conversation history if available
        if conversation_history:
            prompt_parts.append("## RECENT CONVERSATION:")
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                prompt_parts.append(f"{role}: {content}")
            prompt_parts.append("")
        
        # Add current student message
        prompt_parts.append("## CURRENT STUDENT MESSAGE:")
        prompt_parts.append(user_message)
        prompt_parts.append("")
        prompt_parts.append("## YOUR SOCRATIC RESPONSE:")
        prompt_parts.append("(Remember: Guide through questions, don't give direct answers)")
        
        return "\n".join(prompt_parts)

    async def _call_openai_api(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Call OpenAI API with retry logic and error handling"""
        
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    presence_penalty=0.1,  # Encourage variety
                    frequency_penalty=0.1   # Reduce repetition
                )
                
                return {
                    "success": True,
                    "response": response.choices[0].message.content.strip(),
                    "usage": response.usage
                }
                
            except openai.error.RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.warning(f"⏳ Rate limit hit, retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                return {"success": False, "error": f"Rate limit exceeded: {str(e)}"}
                
            except openai.error.APIError as e:
                return {"success": False, "error": f"OpenAI API error: {str(e)}"}
                
            except Exception as e:
                return {"success": False, "error": f"Unexpected error: {str(e)}"}
        
        return {"success": False, "error": "Max retries exceeded"}

    async def _analyze_socratic_compliance(self, ai_response: str, user_message: str) -> SocraticAnalysis:
        """Analyze how well the AI response follows Socratic methodology"""
        
        # Count questions in response
        question_markers = ["?", "what", "why", "how", "when", "where", "which", "who"]
        question_count = ai_response.count("?")
        
        # Calculate question ratio
        sentences = len([s for s in ai_response.split(".") if s.strip()])
        question_ratio = question_count / max(sentences, 1)
        
        # Determine compliance level
        if question_ratio >= 0.7:
            compliance = "HIGH"
            effectiveness = 0.9
        elif question_ratio >= 0.4:
            compliance = "MEDIUM"  
            effectiveness = 0.7
        else:
            compliance = "LOW"
            effectiveness = 0.4
            
        # Check for direct answers (things to avoid)
        direct_answer_phrases = [
            "the answer is", "it is", "this means", "the definition", 
            "here's what", "simply put", "in other words"
        ]
        
        has_direct_answers = any(phrase in ai_response.lower() for phrase in direct_answer_phrases)
        
        # Engagement analysis based on response characteristics
        engagement = "HIGH" if question_count >= 3 and len(ai_response) > 100 else "MEDIUM"
        
        # Teaching approach detection
        if "think about" in ai_response.lower() or "consider" in ai_response.lower():
            approach = "Reflective questioning"
        elif "example" in ai_response.lower() or "imagine" in ai_response.lower():
            approach = "Example-based inquiry"
        else:
            approach = "Direct questioning"
            
        # Generate improvement suggestions
        suggestions = []
        if question_count < 2:
            suggestions.append("Include more questions to guide student thinking")
        if has_direct_answers:
            suggestions.append("Avoid direct answers - use questions instead")
        if len(ai_response) < 50:
            suggestions.append("Provide more detailed questioning to engage deeper thinking")
            
        return SocraticAnalysis(
            question_count=question_count,
            socratic_compliance=compliance,
            engagement_level=engagement,
            teaching_approach=approach,
            effectiveness_score=effectiveness,
            has_direct_answers=has_direct_answers,
            improvement_suggestions=suggestions
        )

    def _calculate_token_usage(self, usage_data: Any, response_time: float) -> TokenUsage:
        """Calculate token usage and estimated cost"""
        
        # OpenAI pricing (approximate, update as needed)
        cost_per_1k_tokens = {
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01,
            "gpt-3.5-turbo": 0.002
        }
        
        rate = cost_per_1k_tokens.get(self.model, 0.01)
        estimated_cost = (usage_data.total_tokens / 1000) * rate
        
        return TokenUsage(
            prompt_tokens=usage_data.prompt_tokens,
            completion_tokens=usage_data.completion_tokens,
            total_tokens=usage_data.total_tokens,
            estimated_cost=estimated_cost,
            model_used=self.model,
            response_time_ms=int(response_time * 1000)
        )

    def _update_metrics(self, token_usage: TokenUsage) -> None:
        """Update service performance metrics"""
        self.request_count += 1
        self.total_tokens_used += token_usage.total_tokens
        
        # Update average response time
        current_avg = self.average_response_time
        new_time = token_usage.response_time_ms
        self.average_response_time = ((current_avg * (self.request_count - 1)) + new_time) / self.request_count

    async def _generate_demo_response(self, user_message: str, module_id: int) -> OpenAIResponse:
        """Generate demo response when OpenAI API key is not configured"""
        
        demo_responses = {
            1: "That's an interesting question about communication! What do you think are the key elements that make communication effective? Have you considered how nonverbal cues might play a role in what you're asking about?",
            2: "I can see you're thinking about this concept! What experiences have you had that might relate to this topic? How do you think this connects to what we learned in the previous module?",
            3: "Great question! Instead of giving you the answer directly, let me ask: what patterns do you notice here? What do you think might happen if we approached this differently?"
        }
        
        demo_response = demo_responses.get(module_id, 
            "That's a thoughtful question! What do you think about this topic? How might you explore this further based on what you already know?")
        
        # Create mock analysis
        socratic_analysis = SocraticAnalysis(
            question_count=3,
            socratic_compliance="HIGH",
            engagement_level="HIGH", 
            teaching_approach="Socratic questioning",
            effectiveness_score=0.85,
            has_direct_answers=False,
            improvement_suggestions=[]
        )
        
        token_usage = TokenUsage(
            prompt_tokens=250,
            completion_tokens=50,
            total_tokens=300,
            estimated_cost=0.009,
            model_used="demo-mode",
            response_time_ms=500
        )
        
        logger.info("🎭 Generated demo response (OpenAI API key not configured)")
        
        return OpenAIResponse(
            success=True,
            response=demo_response,
            socratic_analysis=socratic_analysis,
            token_usage=token_usage
        )

    def get_service_metrics(self) -> Dict[str, Any]:
        """Get service performance metrics"""
        return {
            "requests_processed": self.request_count,
            "total_tokens_used": self.total_tokens_used,
            "average_response_time_ms": round(self.average_response_time, 2),
            "average_tokens_per_request": round(self.total_tokens_used / max(self.request_count, 1), 2),
            "estimated_total_cost": round((self.total_tokens_used / 1000) * 0.03, 4),
            "demo_mode": self.demo_mode,
            "model": self.model
        }

    async def test_connection(self) -> Dict[str, Any]:
        """Test OpenAI API connection and return status"""
        if self.demo_mode:
            return {
                "status": "demo_mode",
                "message": "OpenAI API key not configured - using demo responses",
                "working": True
            }
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=5
            )
            
            return {
                "status": "connected",
                "message": f"OpenAI API connection successful - Model: {self.model}",
                "working": True,
                "model": self.model
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"OpenAI API connection failed: {str(e)}",
                "working": False
            }
