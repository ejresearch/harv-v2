"""
Enhanced Memory Service - Phase 2 Implementation
Ports your brilliant 4-layer memory system from legacy to clean architecture

This service preserves your crown jewel intellectual property:
- Dynamic data injection from database
- 4-layer memory context assembly
- Socratic teaching methodology integration  
- Cross-module learning connections
- Optimized prompt construction

Architecture: Clean service layer with proper error handling and type safety
"""

from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from datetime import datetime
import json
import logging

from app.models import (
    User, Module, Conversation, OnboardingSurvey, 
    MemorySummary, UserProgress
)
from app.schemas.memory import MemoryContextResponse, MemoryMetrics

logger = logging.getLogger(__name__)

class EnhancedMemoryService:
    """
    Enhanced 4-Layer Memory System - Production Ready
    
    Preserves your brilliant memory architecture while integrating 
    with clean harv-v2 service patterns
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def assemble_enhanced_context(
        self, 
        user_id: int, 
        module_id: int, 
        current_message: str = "",
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point - assembles optimized 4-layer memory context
        
        Your crown jewel method - preserves the exact logic while adding
        proper error handling and type safety
        """
        
        logger.info(f"🧠 Assembling enhanced memory context for user {user_id}, module {module_id}")
        
        try:
            # Get core entities with error handling
            user = await self._get_user_safely(user_id)
            module = await self._get_module_safely(module_id)
            
            if not user or not module:
                return await self._create_fallback_context(user_id, module_id)
            
            # PHASE 2: Your 4-layer memory system - Dynamic data injection
            system_data = await self._inject_system_data(user)
            module_data = await self._inject_module_data(module)
            conversation_data = await self._inject_conversation_data(user_id, module_id, conversation_id)
            prior_knowledge = await self._inject_prior_knowledge(user_id, module_id)
            
            # Dynamic prompt assembly - your brilliant optimization
            assembled_prompt = await self._assemble_optimized_prompt(
                system_data, module_data, conversation_data, prior_knowledge, current_message
            )
            
            # Calculate context metrics for monitoring
            context_metrics = await self._calculate_context_metrics(assembled_prompt)
            
            logger.info(f"📚 Enhanced context assembled: {context_metrics['total_chars']} chars")
            
            return {
                'assembled_prompt': assembled_prompt,
                'context_metrics': context_metrics,
                'memory_layers': {
                    'system_data': system_data,
                    'module_data': module_data,
                    'conversation_data': conversation_data,
                    'prior_knowledge': prior_knowledge
                },
                'conversation_id': conversation_id,
                'database_status': {
                    'user_found': True,
                    'module_found': True,
                    'onboarding_loaded': bool(system_data.get('learning_profile')),
                    'module_config_loaded': bool(module_data.get('teaching_configuration')),
                    'conversation_analyzed': bool(conversation_data.get('state')),
                    'cross_module_connections': bool(prior_knowledge.get('prior_module_insights'))
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Enhanced memory assembly failed: {e}")
            return await self._handle_memory_error(user_id, module_id, str(e))
    
    async def _inject_system_data(self, user: User) -> Dict[str, Any]:
        """
        Layer 1: System Data Injection - Cross-course learning profile
        
        Your brilliant system memory - preserves exact logic with async/await
        """
        
        try:
            # Get onboarding survey for learning style
            onboarding = self.db.query(OnboardingSurvey).filter(
                OnboardingSurvey.user_id == user.id
            ).first()
            
            # Get completed conversations for cross-module insights
            completed_conversations = self.db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).all()
            
            # Get memory summaries for learning history
            memory_summaries = self.db.query(MemorySummary).filter(
                MemorySummary.user_id == user.id
            ).all()
            
            return {
                'learning_profile': {
                    'style': getattr(onboarding, 'learning_style', 'adaptive') if onboarding else 'adaptive',
                    'pace': getattr(onboarding, 'preferred_pace', 'moderate') if onboarding else 'moderate',
                    'background': getattr(onboarding, 'background_knowledge', 'beginner') if onboarding else 'beginner',
                    'goals': getattr(onboarding, 'learning_goals', ['improve communication skills']) if onboarding else ['improve communication skills']
                },
                'cross_module_mastery': [
                    {
                        'module_id': conv.module_id,
                        'last_activity': conv.updated_at.isoformat() if conv.updated_at else None,
                        'message_count': len(json.loads(conv.messages_json)) if conv.messages_json else 0,
                        'insights_gained': len([m for m in memory_summaries if m.module_id == conv.module_id])
                    }
                    for conv in completed_conversations[:5]  # Recent 5 modules
                ],
                'learning_strengths': [summary.what_learned for summary in memory_summaries[:3]],
                'mastered_concepts': [summary.connections_made for summary in memory_summaries if summary.confidence_level > 0.7]
            }
            
        except Exception as e:
            logger.warning(f"⚠️ System data injection fallback: {e}")
            return {
                'learning_profile': {
                    'style': 'adaptive',
                    'pace': 'moderate', 
                    'background': 'beginner',
                    'goals': ['improve communication skills']
                },
                'cross_module_mastery': [],
                'learning_strengths': [],
                'mastered_concepts': []
            }
    
    async def _inject_module_data(self, module: Module) -> Dict[str, Any]:
        """
        Layer 2: Module Data Injection - Current module context and configuration
        
        Your module-specific memory layer with teaching configuration
        """
        
        try:
            # Get user progress for this module
            user_progress = self.db.query(UserProgress).filter(
                UserProgress.module_id == module.id
            ).first()
            
            return {
                'module_info': {
                    'id': module.id,
                    'title': module.title,
                    'description': getattr(module, 'description', f'Learning module: {module.title}'),
                    'objectives': getattr(module, 'learning_objectives', 'Master key concepts through Socratic dialogue'),
                    'progress': user_progress.completion_percentage if user_progress else 0.0
                },
                'teaching_configuration': {
                    'system_prompt': getattr(module, 'system_prompt', 'Use Socratic questioning to guide student discovery'),
                    'module_prompt': getattr(module, 'module_prompt', 'Focus on understanding through guided questions'),
                    'socratic_intensity': getattr(module, 'socratic_intensity', 'moderate'),
                    'allowed_topics': getattr(module, 'allowed_topics', 'communication,media,society').split(','),
                    'memory_context_template': getattr(module, 'memory_context_template',
                        "Remember, this student previously learned {concepts} and responds well to {methods}"),
                    'cross_module_references': getattr(module, 'cross_module_references',
                        "Consider how {concept} from Module {number} relates to what we're exploring now")
                },
                'socratic_strategy': self._generate_socratic_strategy(module),
                'context_rules': {
                    'include_system_memory': True,
                    'include_module_progress': True,
                    'include_learning_style': True,
                    'include_conversation_state': True,
                    'update_memory_on_response': True,
                    'track_understanding_level': True
                }
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Module data injection fallback: {e}")
            return {
                'module_info': {
                    'id': module.id,
                    'title': module.title,
                    'description': f'Learning module: {module.title}',
                    'objectives': 'Master key concepts through Socratic dialogue',
                    'progress': 0.0
                },
                'teaching_configuration': {
                    'system_prompt': 'Use Socratic questioning to guide student discovery',
                    'module_prompt': 'Focus on understanding through guided questions',
                    'socratic_intensity': 'moderate'
                },
                'socratic_strategy': 'Guide discovery through strategic questioning',
                'context_rules': {'include_system_memory': True}
            }
    
    async def _inject_conversation_data(self, user_id: int, module_id: int, conversation_id: Optional[str]) -> Dict[str, Any]:
        """
        Layer 3: Conversation Data Injection - Real-time dialogue context
        
        Your conversation memory with message analysis
        """
        
        try:
            # Get current conversation
            conversation = None
            if conversation_id:
                conversation = self.db.query(Conversation).filter(
                    and_(
                        Conversation.user_id == user_id,
                        Conversation.module_id == module_id,
                        Conversation.id == conversation_id
                    )
                ).first()
            
            if not conversation:
                # Get most recent conversation for this user/module
                conversation = self.db.query(Conversation).filter(
                    and_(
                        Conversation.user_id == user_id,
                        Conversation.module_id == module_id
                    )
                ).order_by(desc(Conversation.updated_at)).first()
            
            if not conversation:
                return {
                    'state': 'new_conversation',
                    'message_history': [],
                    'dialogue_context': 'Starting fresh conversation',
                    'conversation_analysis': {'topic_focus': 'introduction', 'engagement_level': 'beginning'}
                }
            
            # Parse conversation messages
            try:
                messages = json.loads(conversation.messages_json) if conversation.messages_json else []
            except (json.JSONDecodeError, TypeError):
                messages = []
            
            return {
                'state': 'active_conversation',
                'message_history': messages[-10:],  # Last 10 messages for context
                'dialogue_context': await self._extract_dialogue_context(messages),
                'conversation_analysis': await self._analyze_conversation_patterns(messages),
                'conversation_id': conversation.id
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Conversation data injection fallback: {e}")
            return {
                'state': 'error_fallback',
                'message_history': [],
                'dialogue_context': 'Unable to load conversation context',
                'conversation_analysis': {'status': 'error'}
            }
    
    async def _inject_prior_knowledge(self, user_id: int, current_module_id: int) -> Dict[str, Any]:
        """
        Layer 4: Prior Knowledge Injection - Cross-module learning connections
        
        Your brilliant cross-module memory - the crown jewel of the system
        """
        
        try:
            # Get most recent conversation from each other module (1 per module)
            other_modules_conversations = self.db.query(Conversation).filter(
                and_(
                    Conversation.user_id == user_id,
                    Conversation.module_id != current_module_id,
                    Conversation.messages_json.isnot(None)
                )
            ).order_by(desc(Conversation.updated_at)).all()
            
            # Group by module_id and take most recent per module - your exact logic
            module_insights = {}
            for conv in other_modules_conversations:
                if conv.module_id not in module_insights:
                    module = self.db.query(Module).filter(Module.id == conv.module_id).first()
                    if module:
                        try:
                            message_count = len(json.loads(conv.messages_json)) if conv.messages_json else 0
                        except:
                            message_count = 0
                            
                        module_insights[conv.module_id] = {
                            'module_id': conv.module_id,
                            'module_title': module.title,
                            'key_insight': f"Previous learning experience with {module.title}",
                            'message_count': message_count,
                            'last_activity': conv.updated_at.isoformat() if conv.updated_at else None,
                            'connection_strength': min(message_count / 10.0, 1.0)  # Normalize to 0-1
                        }
            
            # Get memory summaries for mastered concepts
            memory_summaries = self.db.query(MemorySummary).filter(
                MemorySummary.user_id == user_id
            ).order_by(desc(MemorySummary.confidence_level)).all()
            
            return {
                'prior_module_insights': list(module_insights.values())[:3],  # Top 3 most recent
                'mastered_concepts': [
                    summary.what_learned for summary in memory_summaries[:5] 
                    if summary.confidence_level > 0.6
                ],
                'cross_module_connections': [
                    summary.connections_made for summary in memory_summaries 
                    if summary.connections_made
                ][:3]
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Prior knowledge injection fallback: {e}")
            return {
                'prior_module_insights': [],
                'mastered_concepts': ['Communication fundamentals', 'Critical thinking'],
                'cross_module_connections': []
            }
    
    async def _assemble_optimized_prompt(
        self, 
        system_data: Dict, 
        module_data: Dict, 
        conversation_data: Dict, 
        prior_knowledge: Dict,
        current_message: str
    ) -> str:
        """
        Dynamic Prompt Assembly - Your brilliant optimization engine
        
        Intelligently combines all 4 memory layers into optimized prompt
        Preserves your exact prompt construction logic
        """
        
        prompt_sections = []
        
        # === HARV ENHANCED MEMORY CONTEXT ===
        prompt_sections.append("=== HARV ENHANCED MEMORY CONTEXT ===")
        
        # Layer 1: System Memory - Learning Profile Injection
        learning_profile = system_data['learning_profile']
        prompt_sections.append(f"STUDENT PROFILE: {learning_profile['style']} learner, {learning_profile['pace']} pace, {learning_profile['background']} background")
        
        if learning_profile['goals']:
            goals_str = ', '.join(learning_profile['goals'])
            prompt_sections.append(f"LEARNING GOALS: {goals_str}")
        
        # Cross-module experience
        if system_data['cross_module_mastery']:
            mastery_count = len(system_data['cross_module_mastery'])
            prompt_sections.append(f"PRIOR EXPERIENCE: {mastery_count} previous module interactions")
        
        # Layer 2: Module Memory - Current Context
        module_info = module_data['module_info']
        teaching_config = module_data['teaching_configuration']
        
        prompt_sections.append(f"\nMODULE CONTEXT: {module_info['title']} - {module_info['description']}")
        prompt_sections.append(f"LEARNING OBJECTIVES: {module_info['objectives']}")
        prompt_sections.append(f"PROGRESS: {module_info['progress']:.1f}% complete")
        
        # Teaching configuration injection
        if teaching_config.get('system_prompt'):
            prompt_sections.append(f"TEACHING APPROACH: {teaching_config['system_prompt']}")
        
        if teaching_config.get('module_prompt'):
            prompt_sections.append(f"MODULE STRATEGY: {teaching_config['module_prompt']}")
        
        # Layer 3: Conversation Memory - Real-time Context
        prompt_sections.append(f"\nCONVERSATION STATE: {conversation_data['state']}")
        prompt_sections.append(f"DIALOGUE CONTEXT: {conversation_data['dialogue_context']}")
        
        # Recent message context
        if conversation_data['message_history']:
            recent_count = len(conversation_data['message_history'])
            prompt_sections.append(f"RECENT MESSAGES: {recent_count} messages in conversation")
        
        # Layer 4: Prior Knowledge - Cross-module Connections
        if prior_knowledge['prior_module_insights']:
            prompt_sections.append("\nPRIOR LEARNING CONNECTIONS:")
            for insight in prior_knowledge['prior_module_insights'][:2]:
                prompt_sections.append(f"- {insight['module_title']}: {insight['key_insight']}")
        
        if prior_knowledge['mastered_concepts']:
            concepts_str = ', '.join(prior_knowledge['mastered_concepts'][:3])
            prompt_sections.append(f"MASTERED CONCEPTS: {concepts_str}")
        
        # === SOCRATIC STRATEGY ===
        prompt_sections.append(f"\nSOCRATIC APPROACH: {module_data['socratic_strategy']}")
        
        # === CURRENT MESSAGE ANALYSIS ===
        if current_message:
            prompt_sections.append(f"\nSTUDENT MESSAGE: {current_message}")
            approach = await self._analyze_current_message(current_message)
            prompt_sections.append(f"RESPONSE STRATEGY: {approach}")
        
        # === CORE INSTRUCTION ===
        prompt_sections.append("\n=== CORE INSTRUCTION ===")
        prompt_sections.append("Remember: Use Socratic questioning to guide discovery. Never give direct answers.")
        prompt_sections.append("Focus on asking strategic questions that lead the student to insights.")
        prompt_sections.append("Build on their prior knowledge and learning style for maximum effectiveness.")
        
        return "\n".join(prompt_sections)
    
    async def _calculate_context_metrics(self, prompt: str) -> Dict[str, Any]:
        """Calculate context metrics for monitoring and optimization"""
        
        return {
            'total_chars': len(prompt),
            'word_count': len(prompt.split()),
            'optimization_score': min(len(prompt) / 2000, 1.0),  # Optimal around 2000 chars
            'layer_breakdown': {
                'system_data': prompt.count('STUDENT PROFILE'),
                'module_data': prompt.count('MODULE CONTEXT'),
                'conversation_data': prompt.count('CONVERSATION STATE'),
                'prior_knowledge': prompt.count('PRIOR LEARNING')
            },
            'timestamp': datetime.now().isoformat()
        }
    
    # === HELPER METHODS ===
    
    async def _get_user_safely(self, user_id: int) -> Optional[User]:
        """Safely retrieve user with error handling"""
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {e}")
            return None
    
    async def _get_module_safely(self, module_id: int) -> Optional[Module]:
        """Safely retrieve module with error handling"""
        try:
            return self.db.query(Module).filter(Module.id == module_id).first()
        except Exception as e:
            logger.error(f"Error retrieving module {module_id}: {e}")
            return None
    
    async def _extract_dialogue_context(self, messages: List[Dict]) -> str:
        """Extract contextual information from message history"""
        if not messages:
            return "Beginning new dialogue"
        
        # Analyze recent message patterns
        recent_topics = []
        for message in messages[-5:]:  # Last 5 messages
            if isinstance(message, dict) and 'content' in message:
                # Simple topic extraction
                content = message['content'].lower()
                if 'communication' in content:
                    recent_topics.append('communication')
                elif 'media' in content:
                    recent_topics.append('media')
                elif 'society' in content:
                    recent_topics.append('society')
        
        if recent_topics:
            return f"Discussing: {', '.join(set(recent_topics))}"
        return "Active dialogue in progress"
    
    async def _analyze_conversation_patterns(self, messages: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation patterns for teaching optimization"""
        
        if not messages:
            return {'topic_focus': 'introduction', 'engagement_level': 'beginning'}
        
        # Simple pattern analysis
        user_messages = [m for m in messages if m.get('role') == 'user']
        ai_messages = [m for m in messages if m.get('role') == 'assistant']
        
        return {
            'topic_focus': 'communication theory',  # Could be enhanced with NLP
            'engagement_level': 'high' if len(user_messages) > 3 else 'moderate',
            'question_count': len([m for m in ai_messages if '?' in m.get('content', '')]),
            'user_response_length': sum(len(m.get('content', '').split()) for m in user_messages) / max(len(user_messages), 1)
        }
    
    async def _analyze_current_message(self, message: str) -> str:
        """Analyze current message to determine response strategy"""
        
        message_lower = message.lower()
        
        if '?' in message:
            return "Student is asking - guide with counter-questions"
        elif any(word in message_lower for word in ['what', 'how', 'why', 'when', 'where']):
            return "Exploratory inquiry - use Socratic method"
        elif any(word in message_lower for word in ['think', 'believe', 'feel']):
            return "Opinion/reflection - probe deeper reasoning"
        elif len(message.split()) < 5:
            return "Brief response - encourage elaboration"
        else:
            return "Detailed input - identify key concepts to explore"
    
    async def _generate_socratic_strategy(self, module: Module) -> str:
        """Generate Socratic teaching strategy based on module"""
        
        module_title = module.title.lower()
        
        if 'communication' in module_title:
            return "Guide discovery of communication principles through real-world examples"
        elif 'media' in module_title:
            return "Question assumptions about media influence and bias"
        elif 'society' in module_title:
            return "Explore social connections through critical questioning"
        else:
            return "Use strategic questioning to reveal underlying concepts"
    
    async def _create_fallback_context(self, user_id: int, module_id: int) -> Dict[str, Any]:
        """Create fallback context when core entities are missing"""
        
        logger.warning(f"Creating fallback context for user {user_id}, module {module_id}")
        
        return {
            'assembled_prompt': f"Error: Unable to load memory context for user {user_id}, module {module_id}. Proceeding with basic Socratic teaching approach.",
            'context_metrics': {'total_chars': 0, 'optimization_score': 0},
            'memory_layers': {
                'system_data': {'learning_profile': {'style': 'error', 'pace': 'unknown'}},
                'module_data': {'module_info': {'title': f'Module {module_id} (Error)'}},
                'conversation_data': {'state': 'error_state'},
                'prior_knowledge': {'prior_module_insights': []}
            },
            'database_status': {
                'user_found': False,
                'module_found': False,
                'onboarding_loaded': False,
                'module_config_loaded': False,
                'conversation_analyzed': False,
                'cross_module_connections': False
            }
        }
    
    async def _handle_memory_error(self, user_id: int, module_id: int, error: str) -> Dict[str, Any]:
        """Handle memory assembly errors gracefully"""
        
        return {
            'error': f"Memory assembly failed: {error}",
            'assembled_prompt': f"Unable to load enhanced memory context. Using basic teaching mode for Module {module_id}.",
            'context_metrics': {'total_chars': 0, 'error': True},
            'memory_layers': {
                'system_data': {},
                'module_data': {},
                'conversation_data': {},
                'prior_knowledge': {}
            },
            'database_status': {
                'user_found': False,
                'module_found': False,
                'error': error
            }
        }

    # === MEMORY PERSISTENCE METHODS ===
    
    async def save_memory_summary(
        self,
        user_id: int,
        module_id: int,
        what_learned: str,
        how_learned: str,
        connections_made: str,
        confidence_level: float = 0.8
    ) -> bool:
        """Save learning memory summary for future context assembly"""
        
        try:
            memory_summary = MemorySummary(
                user_id=user_id,
                module_id=module_id,
                what_learned=what_learned,
                how_learned=how_learned,
                connections_made=connections_made,
                confidence_level=confidence_level,
                retention_strength=0.9,
                last_accessed=datetime.now().isoformat()
            )
            
            self.db.add(memory_summary)
            self.db.commit()
            
            logger.info(f"💾 Memory summary saved for user {user_id}, module {module_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving memory summary: {e}")
            self.db.rollback()
            return False
    
    async def update_user_progress(
        self,
        user_id: int,
        module_id: int,
        completion_percentage: float,
        insights_gained: int = 0,
        questions_asked: int = 0
    ) -> bool:
        """Update user progress metrics"""
        
        try:
            progress = self.db.query(UserProgress).filter(
                and_(
                    UserProgress.user_id == user_id,
                    UserProgress.module_id == module_id
                )
            ).first()
            
            if not progress:
                progress = UserProgress(
                    user_id=user_id,
                    module_id=module_id,
                    completion_percentage=completion_percentage,
                    insights_gained=insights_gained,
                    questions_asked=questions_asked
                )
                self.db.add(progress)
            else:
                progress.completion_percentage = completion_percentage
                progress.insights_gained += insights_gained
                progress.questions_asked += questions_asked
                progress.updated_at = datetime.now()
            
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating user progress: {e}")
            self.db.rollback()
            return False
