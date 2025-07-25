from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import json
import logging

from app.models import (
    User, OnboardingSurvey, Module, Conversation, 
    Message, MemorySummary, UserProgress
)

logger = logging.getLogger(__name__)

class EnhancedMemoryService:
    """
    4-Layer Enhanced Memory System - COMPLETE FIXED VERSION
    Compatible with existing database schema and chat integration
    
    Features:
    - Layer 1: User Learning Profile & Cross-Module Mastery
    - Layer 2: Current Module Context & Socratic Configuration
    - Layer 3: Real-time Conversation State
    - Layer 4: Prior Knowledge & Cross-Module Connections
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def assemble_memory_context(
        self, 
        user_id: int, 
        module_id: int, 
        current_message: str = "", 
        conversation_id: str = None
    ) -> Dict[str, Any]:
        """
        Assemble complete 4-layer memory context for AI chat
        FIXED: Now includes conversation_id parameter for chat integration
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            logger.info(f"🧠 Assembling memory for user {user_id}, module {module_id}")
            
            # Assemble all 4 layers
            layer1 = await self._assemble_layer1_user_profile(user_id)
            layer2 = await self._assemble_layer2_module_context(module_id)
            layer3 = await self._assemble_layer3_conversation_state(user_id, module_id, conversation_id)
            layer4 = await self._assemble_layer4_knowledge_connections(user_id, module_id)
            
            # Construct final prompt
            assembled_prompt = self._construct_memory_prompt(layer1, layer2, layer3, layer4, current_message)
            
            # Calculate context metrics
            context_size = len(assembled_prompt)
            layers_active = sum([
                bool(layer1.get('content')),
                bool(layer2.get('content')),
                bool(layer3.get('content')),
                bool(layer4.get('content'))
            ])
            
            # Build comprehensive response
            result = {
                "assembled_prompt": assembled_prompt,
                "context_size": context_size,
                "layers_active": layers_active,
                "layer1_profile": layer1,
                "layer2_module": layer2,
                "layer3_conversation": layer3,
                "layer4_connections": layer4,
                "metrics": {
                    "assembly_time_ms": 42,  # Simulated - replace with actual timing
                    "layers_active": layers_active,
                    "context_length": context_size,
                    "user_id": user_id,
                    "module_id": module_id,
                    "conversation_id": conversation_id
                },
                "assembly_timestamp": datetime.utcnow().isoformat(),
                "success": True
            }
            
            logger.info(f"✅ Memory assembled: {context_size} chars, {layers_active}/4 layers active")
            return result
            
        except Exception as e:
            logger.error(f"❌ Memory assembly failed for user {user_id}, module {module_id}: {str(e)}")
            return {
                "assembled_prompt": self._get_fallback_prompt(module_id, current_message),
                "context_size": 0,
                "layers_active": 0,
                "metrics": {
                    "layers_active": 0,
                    "context_length": 0,
                    "error": str(e)
                },
                "error": str(e),
                "assembly_timestamp": datetime.utcnow().isoformat(),
                "success": False
            }
    
    async def _assemble_layer1_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Layer 1: User Learning Profile & Cross-Module Mastery"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            # Get onboarding survey if exists
            try:
                survey = self.db.query(OnboardingSurvey).filter(OnboardingSurvey.user_id == user_id).first()
            except:
                survey = None
            
            # Get cross-module progress if table exists
            try:
                progress_records = self.db.query(UserProgress).filter(
                    UserProgress.user_id == user_id,
                    UserProgress.completion_percentage > 0
                ).all()
            except:
                progress_records = []
            
            # Calculate mastery overview
            total_modules = len(progress_records)
            avg_completion = sum(getattr(p, 'completion_percentage', 0) for p in progress_records) / max(total_modules, 1)
            mastery_levels = [getattr(p, 'mastery_level', 'beginner') for p in progress_records]
            
            # Build profile content
            profile_content = f"""🎓 STUDENT LEARNING PROFILE:
Name: {user.name}
Learning Style: {getattr(survey, 'learning_style', 'Visual') if survey else 'Visual + Interactive'}
Preferred Pace: {getattr(survey, 'preferred_pace', 'Moderate') if survey else 'Moderate'}
Interaction Style: {getattr(survey, 'interaction_preference', 'Socratic questioning') if survey else 'Socratic questioning'}

📊 CROSS-MODULE MASTERY:
Modules Started: {total_modules}
Average Completion: {avg_completion:.1f}%
Mastery Levels: {', '.join(set(mastery_levels)) if mastery_levels else 'Beginning learner'}

🎯 LEARNING GOALS:
{getattr(survey, 'goals', 'Improve communication skills and build confidence') if survey else 'Improve communication skills and build confidence'}

💡 PERSONALIZATION NOTES:
- Responds well to question-based learning
- Prefers practical examples and real-world applications
- Benefits from connecting concepts across modules"""
            
            return {
                "layer": "user_profile",
                "content": profile_content,
                "metadata": {
                    "modules_started": total_modules,
                    "average_completion": avg_completion,
                    "mastery_levels": mastery_levels,
                    "learning_style": getattr(survey, 'learning_style', 'visual') if survey else "visual",
                    "preferred_pace": getattr(survey, 'preferred_pace', 'moderate') if survey else "moderate"
                }
            }
            
        except Exception as e:
            logger.error(f"Layer 1 assembly failed: {str(e)}")
            return {
                "layer": "user_profile", 
                "content": "🎓 New learner beginning their communication journey. Ready to discover through questions and dialogue.",
                "error": str(e)
            }
    
    async def _assemble_layer2_module_context(self, module_id: int) -> Dict[str, Any]:
        """Layer 2: Current Module Context & Socratic Configuration"""
        try:
            module = self.db.query(Module).filter(Module.id == module_id).first()
            if not module:
                return {
                    "layer": "module_context", 
                    "content": f"📚 Module {module_id}: Communication fundamentals with Socratic methodology active.",
                    "error": "Module not found"
                }
            
            # Use description field safely
            module_description = getattr(module, 'description', f'Communication skills module focusing on practical learning')
            
            # Create learning objectives based on module
            objectives_map = {
                1: ["Master verbal communication techniques", "Understand nonverbal communication", "Apply active listening skills"],
                2: ["Develop persuasive communication", "Build professional presentation skills", "Handle difficult conversations"],
                3: ["Practice group communication", "Lead effective meetings", "Facilitate team discussions"]
            }
            
            objectives = objectives_map.get(module_id, ["Develop communication skills", "Apply theoretical knowledge", "Build practical competence"])
            
            # Create key concepts
            concepts_map = {
                1: ["Message clarity", "Active listening", "Nonverbal awareness", "Feedback loops"],
                2: ["Persuasion techniques", "Professional tone", "Conflict resolution", "Presentation skills"],
                3: ["Group dynamics", "Meeting facilitation", "Team communication", "Leadership presence"]
            }
            
            key_concepts = concepts_map.get(module_id, ["Communication theory", "Practical application", "Socratic dialogue"])
            
            module_content = f"""📚 CURRENT MODULE CONTEXT:
Module {module_id}: {module.title}
Description: {module_description}

🎯 LEARNING OBJECTIVES:
{chr(10).join(f'• {obj}' for obj in objectives)}

🔑 KEY CONCEPTS:
{', '.join(key_concepts)}

🗣️ SOCRATIC TEACHING MODE: ACTIVE
Teaching Approach:
• Use questioning to guide discovery rather than providing direct answers
• Challenge assumptions respectfully and constructively
• Build on student's existing knowledge and experiences
• Encourage critical thinking about communication principles
• Connect theoretical concepts to real-world applications
• Maintain 70%+ questions in responses to promote active learning"""
            
            return {
                "layer": "module_context",
                "content": module_content,
                "metadata": {
                    "module_id": module_id,
                    "module_title": module.title,
                    "objectives_count": len(objectives),
                    "concepts_count": len(key_concepts),
                    "socratic_mode": True
                }
            }
            
        except Exception as e:
            logger.error(f"Layer 2 assembly failed: {str(e)}")
            return {
                "layer": "module_context", 
                "content": f"📚 Module {module_id}: Communication skills with Socratic methodology. Focus on guided discovery through questions.",
                "error": str(e)
            }
    
    async def _assemble_layer3_conversation_state(self, user_id: int, module_id: int, conversation_id: str = None) -> Dict[str, Any]:
        """Layer 3: Real-time Conversation State"""
        try:
            # Try to get conversation by ID first, then fall back to most recent
            conversation = None
            
            if conversation_id:
                try:
                    conversation = self.db.query(Conversation).filter(
                        Conversation.id == conversation_id
                    ).first()
                except:
                    pass
            
            # Fall back to most recent conversation for this user/module
            if not conversation:
                try:
                    conversation = self.db.query(Conversation).filter(
                        Conversation.user_id == user_id,
                        Conversation.module_id == module_id
                    ).order_by(desc(Conversation.created_at)).first()
                except:
                    conversation = None
            
            if not conversation:
                return {
                    "layer": "conversation_state",
                    "content": """💬 CONVERSATION STATE: NEW SESSION
This is a fresh conversation. Start with engaging questions to:
• Assess current understanding of communication concepts
• Identify specific areas of interest or challenge
• Establish rapport and learning objectives
• Use Socratic questioning to guide discovery""",
                    "metadata": {
                        "messages_count": 0, 
                        "conversation_id": conversation_id,
                        "session_type": "new"
                    }
                }
            
            # Get recent messages if Message table exists
            recent_messages = []
            try:
                messages = self.db.query(Message).filter(
                    Message.conversation_id == conversation.id
                ).order_by(desc(Message.created_at)).limit(10).all()
                recent_messages = list(reversed(messages))
            except:
                pass
            
            # Build conversation context
            message_history = []
            for msg in recent_messages:
                role = "Student" if getattr(msg, 'is_user', True) else "AI Tutor"
                content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                message_history.append(f"{role}: {content}")
            
            # Determine conversation phase
            message_count = len(recent_messages)
            if message_count < 3:
                phase = "Opening - Building rapport and assessing understanding"
            elif message_count < 8:
                phase = "Exploration - Guiding discovery through questions"
            else:
                phase = "Deepening - Advanced concepts and application"
            
            conversation_content = f"""💬 CONVERSATION STATE: ONGOING SESSION
Conversation ID: {conversation.id}
Current Phase: {phase}
Messages Exchanged: {message_count}
Topic Focus: {getattr(conversation, 'current_topic', 'Communication skill development')}

📝 RECENT DIALOGUE:
{chr(10).join(message_history[-6:]) if message_history else 'No previous messages in this session'}

🎯 NEXT STEPS:
Continue the Socratic dialogue by:
• Building on previous exchanges
• Asking follow-up questions that deepen understanding
• Connecting current topic to broader communication principles
• Encouraging practical application and reflection"""
            
            return {
                "layer": "conversation_state", 
                "content": conversation_content,
                "metadata": {
                    "conversation_id": conversation.id,
                    "messages_count": message_count,
                    "current_topic": getattr(conversation, 'current_topic', None),
                    "phase": phase
                }
            }
            
        except Exception as e:
            logger.error(f"Layer 3 assembly failed: {str(e)}")
            return {
                "layer": "conversation_state", 
                "content": "💬 Ready to begin meaningful learning dialogue. Focus on asking engaging questions to guide discovery.",
                "error": str(e)
            }
    
    async def _assemble_layer4_knowledge_connections(self, user_id: int, module_id: int) -> Dict[str, Any]:
        """Layer 4: Prior Knowledge & Cross-Module Connections"""
        try:
            # Get memory summaries from other modules
            memory_summaries = []
            try:
                summaries = self.db.query(MemorySummary).filter(
                    MemorySummary.user_id == user_id,
                    MemorySummary.module_id != module_id
                ).order_by(desc(MemorySummary.created_at)).limit(5).all()
                memory_summaries = summaries
            except:
                pass
            
            # Get progress from other modules
            other_progress = []
            try:
                progress = self.db.query(UserProgress).filter(
                    UserProgress.user_id == user_id,
                    UserProgress.module_id != module_id,
                    UserProgress.completion_percentage > 20
                ).all()
                other_progress = progress
            except:
                pass
            
            # Build connections
            learning_connections = []
            for summary in memory_summaries:
                insights = getattr(summary, 'key_insights', f'Completed learning in Module {summary.module_id}')
                learning_connections.append(f"Module {summary.module_id}: {insights}")
            
            progress_insights = []
            for prog in other_progress:
                mastery = getattr(prog, 'mastery_level', 'developing')
                completion = getattr(prog, 'completion_percentage', 0)
                progress_insights.append(f"Module {prog.module_id}: {mastery} level ({completion:.0f}% complete)")
            
            # Create module-specific connections
            connection_map = {
                1: {
                    "builds_on": [],
                    "connects_to": ["Module 2: Advanced verbal techniques", "Module 3: Group communication"],
                    "foundational_for": "All subsequent communication modules"
                },
                2: {
                    "builds_on": ["Module 1: Basic communication principles"],
                    "connects_to": ["Module 3: Team dynamics", "Module 4: Leadership communication"],
                    "foundational_for": "Professional communication skills"
                },
                3: {
                    "builds_on": ["Module 1: Individual communication", "Module 2: Persuasive techniques"],
                    "connects_to": ["Module 4: Leadership", "Module 5: Conflict resolution"],
                    "foundational_for": "Advanced team leadership"
                }
            }
            
            module_connections = connection_map.get(module_id, {
                "builds_on": ["Previous communication concepts"],
                "connects_to": ["Related communication modules"],
                "foundational_for": "Advanced communication skills"
            })
            
            knowledge_content = f"""🔗 KNOWLEDGE CONNECTIONS & PRIOR LEARNING:

📚 CROSS-MODULE LEARNING PATTERNS:
{chr(10).join(learning_connections[:3]) if learning_connections else '• Building foundational communication understanding'}

📈 RELATED PROGRESS:
{chr(10).join(progress_insights[:3]) if progress_insights else '• Early in comprehensive communication learning journey'}

🌉 MODULE CONNECTIONS:
Builds On: {', '.join(module_connections['builds_on']) if module_connections['builds_on'] else 'Core communication principles'}
Connects To: {', '.join(module_connections['connects_to'])}
Foundation For: {module_connections['foundational_for']}

💡 TEACHING INTEGRATION:
Use these connections to:
• Reference previously mastered concepts when explaining new ideas
• Build conceptual bridges between modules for deeper understanding
• Personalize examples based on their demonstrated knowledge areas
• Reinforce learning through strategic cross-module references
• Help them see the bigger picture of communication competency"""
            
            return {
                "layer": "knowledge_connections",
                "content": knowledge_content,
                "metadata": {
                    "connections_count": len(learning_connections),
                    "related_modules": len(progress_insights),
                    "cross_module_insights": learning_connections[:2],
                    "module_connections": module_connections
                }
            }
            
        except Exception as e:
            logger.error(f"Layer 4 assembly failed: {str(e)}")
            return {
                "layer": "knowledge_connections", 
                "content": "🔗 Ready to build new learning connections and integrate knowledge across communication modules.",
                "error": str(e)
            }
    
    def _construct_memory_prompt(self, layer1: Dict, layer2: Dict, layer3: Dict, layer4: Dict, current_message: str) -> str:
        """Construct the final memory-enhanced prompt for AI"""
        prompt_parts = [
            "=== ENHANCED MEMORY CONTEXT FOR PERSONALIZED AI TUTORING ===",
            "",
            layer1.get('content', ''),
            "",
            layer2.get('content', ''),
            "",
            layer3.get('content', ''),
            "",
            layer4.get('content', ''),
            "",
            "=== CURRENT STUDENT MESSAGE ===",
            f"Student asks: {current_message}" if current_message else "Student is beginning a new interaction",
            "",
            "=== AI TUTOR INSTRUCTIONS ===",
            "You are an expert communication tutor using the Socratic method powered by GPT-4o.",
            "Use the comprehensive memory context above to provide personalized, intelligent tutoring.",
            "",
            "CORE PRINCIPLES:",
            "• Ask thoughtful questions that build on their specific learning journey",
            "• Reference their progress, preferences, and previous learning when relevant", 
            "• Guide discovery rather than providing direct answers",
            "• Maintain encouraging, supportive tone throughout",
            "• Connect new concepts to their existing knowledge base",
            "• Use 70%+ questions in your response to promote active learning"
        ]
        
        return "\n".join(part for part in prompt_parts if part is not None)
    
    def _get_fallback_prompt(self, module_id: int, current_message: str = "") -> str:
        """Fallback prompt when memory assembly fails"""
        return f"""You are an expert communication tutor for Module {module_id}.

Student message: {current_message if current_message else 'Beginning new interaction'}

Use Socratic questioning to guide student learning:
• Ask thoughtful questions to assess understanding
• Promote critical thinking about communication concepts  
• Build confidence through guided discovery
• Maintain encouraging, supportive tone
• Focus on practical application of concepts"""
    
    async def save_conversation_insights(
        self,
        user_id: int,
        module_id: int,
        conversation_id: str,
        user_message: str,
        ai_response: str,
        socratic_score: float,
        key_insights: List[str] = None,
        learning_connections: List[str] = None
    ) -> bool:
        """Save conversation insights to memory system"""
        try:
            # Create or update memory summary
            summary = self.db.query(MemorySummary).filter(
                MemorySummary.user_id == user_id,
                MemorySummary.module_id == module_id
            ).first()
            
            if not summary:
                summary = MemorySummary(
                    user_id=user_id,
                    module_id=module_id,
                    what_learned="; ".join(key_insights) if key_insights else "Communication learning in progress",
                    connections_made="; ".join(learning_connections) if learning_connections else "",
                    conversation_count=1,
                    last_interaction=datetime.utcnow()
                )
                self.db.add(summary)
            else:
                # Update existing summary
                if hasattr(summary, 'conversation_count'):
                    summary.conversation_count += 1
                summary.last_interaction = datetime.utcnow()
                if key_insights:
                    summary.what_learned = "; ".join(key_insights)
                if learning_connections:
                    summary.connections_made = "; ".join(learning_connections)
            
            self.db.commit()
            logger.info(f"💾 Saved conversation insights for user {user_id}, module {module_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save conversation insights: {str(e)}")
            self.db.rollback()
            return False
    
    async def get_memory_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive memory system analytics"""
        try:
            # Get memory summaries
            summaries = []
            try:
                summaries = self.db.query(MemorySummary).filter(MemorySummary.user_id == user_id).all()
            except:
                pass
            
            # Get progress records
            progress = []
            try:
                progress = self.db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
            except:
                pass
            
            # Calculate analytics
            total_conversations = sum(getattr(s, 'conversation_count', 0) for s in summaries)
            modules_with_memory = len(summaries)
            modules_completed = len([p for p in progress if getattr(p, 'completion_percentage', 0) >= 100])
            avg_completion = sum(getattr(p, 'completion_percentage', 0) for p in progress) / max(len(progress), 1)
            
            # Get recent activity
            recent_summaries = sorted(summaries, key=lambda x: getattr(x, 'last_interaction', datetime.min), reverse=True)
            last_interaction = recent_summaries[0].last_interaction if recent_summaries else None
            
            return {
                "user_id": user_id,
                "total_conversations": total_conversations,
                "modules_with_memory": modules_with_memory,
                "modules_completed": modules_completed,
                "average_completion": avg_completion,
                "memory_summaries": len(summaries),
                "last_interaction": last_interaction.isoformat() if last_interaction else None,
                "cross_module_connections": modules_with_memory,
                "memory_system_health": "active" if summaries else "initializing"
            }
            
        except Exception as e:
            logger.error(f"Failed to get memory analytics: {str(e)}")
            return {
                "user_id": user_id,
                "error": str(e),
                "memory_system_health": "error"
            }
    
    async def get_conversation_data(self, conversation_id: str, user_id: int) -> Optional[Dict[str, Any]]:
        """Get conversation data for analytics"""
        try:
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            
            if not conversation:
                return None
            
            # Get messages
            messages = []
            try:
                msgs = self.db.query(Message).filter(
                    Message.conversation_id == conversation_id
                ).order_by(Message.created_at).all()
                messages = msgs
            except:
                pass
            
            return {
                "conversation_id": conversation_id,
                "module_id": conversation.module_id,
                "message_count": len(messages),
                "created_at": conversation.created_at,
                "messages": [{"content": m.content, "is_user": getattr(m, 'is_user', True)} for m in messages]
            }
            
        except Exception as e:
            logger.error(f"Failed to get conversation data: {str(e)}")
            return None
