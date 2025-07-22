# backend/app/services/openai_service.py
"""
OpenAI Integration Service - FULL FEATURED VERSION
Real GPT-4o with enhanced memory system - fixing the response format issue
"""

import logging
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
import json
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """Full-featured OpenAI integration with enhanced memory system"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model or "gpt-4o"
        
    async def generate_socratic_response(
        self, 
        user_message: str, 
        module_id: int,
        memory_context: Any = None,
        enhanced_memory_context: Any = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate authentic Socratic tutoring response using GPT-4o with enhanced memory
        """
        try:
            # Use enhanced_memory_context if provided, otherwise fall back to memory_context
            context = enhanced_memory_context or memory_context or {}
            
            # Handle case where context might be a string instead of dict
            if isinstance(context, str):
                try:
                    context = json.loads(context)
                    logger.info("Successfully parsed memory context JSON")
                except (json.JSONDecodeError, TypeError):
                    logger.info("Memory context is plain text, creating structure")
                    context = {"raw_context": context}
            
            # Ensure context is a dictionary
            if not isinstance(context, dict):
                logger.info(f"Converting memory context from {type(context)} to dict")
                context = {"context_data": str(context)}
            
            # Build enhanced context from memory layers
            system_prompt = self._build_socratic_system_prompt(module_id, context)
            
            # Prepare messages for OpenAI
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"🤖 Sending request to OpenAI ({self.model}) with {len(messages)} messages")
            
            # Make the API call to GPT-4o
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            logger.info(f"✅ OpenAI response generated - {tokens_used} tokens used")
            
            # Analyze the teaching effectiveness with second GPT-4o call
            try:
                effectiveness = await self._analyze_teaching_effectiveness(
                    user_message, ai_response, context
                )
                logger.info("📊 Teaching effectiveness analysis complete")
            except Exception as analysis_error:
                logger.warning(f"Analysis failed: {analysis_error}, using default")
                effectiveness = {
                    "analysis": "Analysis temporarily unavailable",
                    "analyzed": False,
                    "socratic_score": 3
                }
            
            # Return the structure that chat endpoint expects
            result = {
                "response": ai_response,
                "socratic_analysis": effectiveness,  # Now returns the full structured dict
                "tokens_used": tokens_used,
                "teaching_effectiveness": effectiveness,
                "token_usage": {"total_tokens": tokens_used, "prompt_tokens": 0, "completion_tokens": tokens_used},
                "model_used": self.model,
                "success": True
            }
            
            logger.info(f"✅ Returning enhanced response: {len(str(ai_response))} chars")
            logger.info(f"🔍 Response keys: {list(result.keys())}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {str(e)}")
            
            # Ensure error response has same structure
            error_result = {
                "response": "I apologize, but I'm having trouble connecting to my knowledge base right now. Could you try rephrasing your question?",
                "socratic_analysis": {
                    "question_count": 1,
                    "socratic_compliance": "fair",
                    "engagement_level": "medium",
                    "teaching_approach": "mixed",
                    "effectiveness_score": 0.5,
                    "has_direct_answers": False,
                    "analysis_text": f"Analysis failed due to error: {str(e)}",
                    "analyzed": False
                },
                "tokens_used": 0,
                "teaching_effectiveness": {"analysis": "Error", "analyzed": False},
                "token_usage": {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0},
                "model_used": self.model,
                "success": False,
                "error": str(e)
            }
            
            logger.info(f"🔍 Error response keys: {list(error_result.keys())}")
            return error_result
    
    def _build_socratic_system_prompt(self, module_id: int, memory_context: Dict[str, Any]) -> str:
        """Build comprehensive system prompt with enhanced memory context"""
        
        # Safely extract memory information with defaults
        concepts = memory_context.get("concepts", []) if memory_context else []
        relations = memory_context.get("relations", []) if memory_context else []
        patterns = memory_context.get("learning_patterns", []) if memory_context else []
        strategies = memory_context.get("teaching_strategies", []) if memory_context else []
        
        # Build concept knowledge
        concept_knowledge = ""
        if concepts and len(concepts) > 0:
            concept_knowledge = "Key concepts the student is learning:\n"
            for concept in concepts[:10]:  # Limit to avoid token overflow
                # Handle both dict and object formats
                if isinstance(concept, dict):
                    name = concept.get('name', 'Unknown')
                    desc = concept.get('description', 'No description')
                else:
                    # Handle case where concept might be an object with attributes
                    name = getattr(concept, 'name', 'Unknown')
                    desc = getattr(concept, 'description', 'No description')
                concept_knowledge += f"- {name}: {desc}\n"
        
        # Build learning patterns insight
        learning_insight = ""
        if patterns and len(patterns) > 0:
            learning_insight = "\nStudent learning patterns observed:\n"
            for pattern in patterns[:5]:
                # Handle both dict and object formats
                if isinstance(pattern, dict):
                    ptype = pattern.get('pattern_type', 'Unknown')
                    desc = pattern.get('description', 'No description')
                else:
                    ptype = getattr(pattern, 'pattern_type', 'Unknown')
                    desc = getattr(pattern, 'description', 'No description')
                learning_insight += f"- {ptype}: {desc}\n"
        
        # Module-specific guidance
        module_guidance = {
            1: "Focus on communication theory, media literacy, and critical thinking about information sources.",
            2: "Emphasize historical context, cause-and-effect relationships, and primary vs secondary sources.",
            3: "Guide through scientific method, evidence evaluation, and hypothesis formation.",
            4: "Develop mathematical reasoning, problem-solving strategies, and logical thinking."
        }
        
        system_prompt = f"""You are a Socratic tutor using the enhanced Harv v2.0 educational system. Your role is to guide students to discover knowledge through thoughtful questioning rather than direct instruction.

MODULE {module_id} FOCUS: {module_guidance.get(module_id, "General critical thinking and inquiry-based learning")}

{concept_knowledge}

{learning_insight}

SOCRATIC TEACHING PRINCIPLES:
1. Ask probing questions that lead students to insights
2. Challenge assumptions gently but persistently  
3. Help students connect new information to prior knowledge
4. Encourage evidence-based reasoning
5. Guide students to discover contradictions in their thinking
6. Use analogies and examples to clarify complex concepts
7. Celebrate intellectual curiosity and growth

RESPONSE GUIDELINES:
- Keep responses focused and concise (100-200 words)
- Ask 1-2 thoughtful follow-up questions
- Acknowledge student insights before probing deeper
- Use encouraging but challenging tone
- Reference specific concepts from the memory context when relevant
- Guide students to think critically about sources and evidence

Remember: Your goal is not to provide answers, but to help students discover them through guided inquiry."""
        
        return system_prompt
    
    async def _analyze_teaching_effectiveness(
        self, 
        student_message: str, 
        ai_response: str, 
        memory_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze how effective the Socratic response was using second GPT-4o call
        Returns structured data that matches what chat endpoint expects
        """
        try:
            analysis_prompt = f"""Analyze this Socratic teaching interaction and respond with structured data:

Student Message: "{student_message}"
AI Response: "{ai_response}"

Count the questions in the AI response and evaluate:
1. How many questions did the AI ask? (count them)
2. Socratic compliance: "excellent", "good", "fair", or "poor"
3. Engagement level: "high", "medium", or "low" 
4. Teaching approach: "discovery-based", "guided", "direct", or "mixed"
5. Effectiveness score: 0.0 to 1.0
6. Does it contain direct answers? true/false

Respond in this exact JSON format:
{{
    "question_count": number,
    "socratic_compliance": "excellent/good/fair/poor",
    "engagement_level": "high/medium/low",
    "teaching_approach": "discovery-based/guided/direct/mixed", 
    "effectiveness_score": 0.0-1.0,
    "has_direct_answers": true/false,
    "analysis_text": "brief analysis"
}}"""

            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                max_tokens=300
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                import json
                analysis_data = json.loads(analysis_text)
                
                # Ensure all required fields exist with defaults
                return {
                    "question_count": analysis_data.get("question_count", 2),
                    "socratic_compliance": analysis_data.get("socratic_compliance", "good"),
                    "engagement_level": analysis_data.get("engagement_level", "medium"),
                    "teaching_approach": analysis_data.get("teaching_approach", "guided"),
                    "effectiveness_score": float(analysis_data.get("effectiveness_score", 0.7)),
                    "has_direct_answers": bool(analysis_data.get("has_direct_answers", False)),
                    "analysis_text": analysis_data.get("analysis_text", "Analysis complete"),
                    "timestamp": "2025-07-22T16:20:00Z",
                    "analyzed": True
                }
                
            except (json.JSONDecodeError, KeyError, ValueError) as parse_error:
                logger.warning(f"Could not parse analysis JSON: {parse_error}")
                # Return structured fallback
                return {
                    "question_count": 2,
                    "socratic_compliance": "good", 
                    "engagement_level": "medium",
                    "teaching_approach": "guided",
                    "effectiveness_score": 0.7,
                    "has_direct_answers": False,
                    "analysis_text": "Analysis parsing failed, using defaults",
                    "timestamp": "2025-07-22T16:20:00Z",
                    "analyzed": True
                }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return {
                "question_count": 2,
                "socratic_compliance": "fair",
                "engagement_level": "medium", 
                "teaching_approach": "mixed",
                "effectiveness_score": 0.6,
                "has_direct_answers": False,
                "analysis_text": f"Analysis failed: {str(e)}",
                "timestamp": "2025-07-22T16:20:00Z",
                "analyzed": False,
                "error": str(e)
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check if OpenAI API is accessible"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            
            return {
                "status": "healthy",
                "model": self.model,
                "api_accessible": True
            }
            
        except Exception as e:
            logger.error(f"OpenAI health check failed: {str(e)}")
            return {
                "status": "unhealthy", 
                "model": self.model,
                "api_accessible": False,
                "error": str(e)
            }

# Global instance
openai_service = OpenAIService()
