"""
UNIVERSAL MEMORY SERVICE ENHANCEMENT
Add this code to your existing memory_service.py to make it document-aware for ALL modules

This enhancement works with ANY module (1-15) that has uploaded documents
"""

import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# ADD TO YOUR EXISTING EnhancedMemoryService class:

async def _inject_module_data(self, module: Module) -> Dict[str, Any]:
    """
    Layer 2: Module Data Injection - UNIVERSALLY ENHANCED with document intelligence
    
    This enhanced version works with ALL 15 modules and automatically detects
    when a module has document intelligence available
    """
    
    try:
        # YOUR EXISTING CODE (unchanged) - Get user progress
        user_progress = self.db.query(UserProgress).filter(
            UserProgress.module_id == module.id
        ).first()
        
        # YOUR EXISTING TEACHING CONFIGURATION (preserved)
        teaching_config = {
            'module_id': module.id,
            'title': module.title,
            'description': module.description,
            'system_prompt': module.system_prompt,
            'module_prompt': module.module_prompt or "",
            'learning_objectives': module.learning_objectives,
            'progress_percentage': getattr(user_progress, 'completion_percentage', 0.0) if user_progress else 0.0,
            'mastery_level': getattr(user_progress, 'mastery_level', 'beginner') if user_progress else 'beginner',
            'socratic_intensity': 'moderate'
        }
        
        # NEW: UNIVERSAL DOCUMENT INTELLIGENCE (works with ANY module)
        if hasattr(module, 'has_document_intelligence') and module.has_document_intelligence():
            try:
                # Get document intelligence data
                document_concepts = module.get_document_concepts()
                document_examples = module.get_document_examples()
                socratic_questions = module.get_socratic_questions()
                document_status = module.get_document_status()
                
                # ENHANCE teaching configuration with document intelligence
                teaching_config['document_intelligence'] = {
                    'source_document': document_status.get('document_name'),
                    'document_type': document_status.get('document_type'),
                    'processed_at': document_status.get('processed_at'),
                    'extracted_concepts': document_concepts,
                    'real_world_examples': document_examples,
                    'concept_questions': socratic_questions.get('concept_questions', []),
                    'application_questions': socratic_questions.get('application_questions', []),
                    'document_summary': getattr(module, 'document_summary', ''),
                    'concepts_count': len(document_concepts),
                    'examples_count': len(document_examples),
                    'enhanced': True
                }
                
                # ENHANCE Socratic strategy with document-specific guidance
                enhanced_socratic_strategy = await self._generate_socratic_strategy(module)
                
                # Add document-specific teaching guidance
                if document_examples:
                    example_names = list(document_examples.keys())[:3]
                    enhanced_socratic_strategy += f"\n\nDOCUMENT-SPECIFIC TEACHING GUIDANCE:"
                    enhanced_socratic_strategy += f"\n- Reference these real examples from course materials: {', '.join(example_names)}"
                    
                if socratic_questions.get('concept_questions'):
                    enhanced_socratic_strategy += f"\n- Use these targeted questions: {socratic_questions['concept_questions'][:2]}"
                
                if document_concepts:
                    concept_names = list(document_concepts.keys())[:3]
                    enhanced_socratic_strategy += f"\n- Focus on these key concepts: {', '.join(concept_names)}"
                
                logger.info(f"📚 Module {module.id} ({module.title}) enhanced with document intelligence")
                logger.info(f"   - {len(document_concepts)} concepts, {len(document_examples)} examples")
                
            except Exception as e:
                logger.warning(f"Failed to parse document intelligence for Module {module.id}: {e}")
                # Fallback to standard strategy
                enhanced_socratic_strategy = await self._generate_socratic_strategy(module)
        else:
            # NO DOCUMENT INTELLIGENCE - use existing logic (backward compatible)
            enhanced_socratic_strategy = await self._generate_socratic_strategy(module)
            logger.debug(f"📝 Module {module.id} using standard teaching strategy (no document)")
        
        # RETURN ENHANCED DATA (backward compatible structure)
        return {
            'teaching_configuration': teaching_config,
            'socratic_strategy': enhanced_socratic_strategy,
            'progress_tracking': self._create_progress_context(user_progress)
        }
        
    except Exception as e:
        logger.warning(f"Module data injection error for Module {module.id}: {e}")
        # YOUR EXISTING FALLBACK (unchanged)
        return {
            'teaching_configuration': {
                'module_id': module.id,
                'title': module.title or f"Module {module.id}",
                'system_prompt': 'You are a helpful communication tutor.',
                'socratic_intensity': 'moderate'
            },
            'socratic_strategy': 'Use discovery-based questioning',
            'progress_tracking': {'status': 'error_fallback'}
        }

# ADD THIS NEW METHOD to your EnhancedMemoryService class:

def get_module_document_status(self, module_id: int) -> Dict[str, Any]:
    """Get document intelligence status for any module"""
    try:
        module = self.db.query(Module).filter(Module.id == module_id).first()
        if not module:
            return {"error": f"Module {module_id} not found"}
        
        if hasattr(module, 'get_document_status'):
            return module.get_document_status()
        else:
            return {
                "has_document": False,
                "message": "Document intelligence not available (model needs enhancement)"
            }
    except Exception as e:
        return {"error": f"Failed to get status: {str(e)}"}

# Usage example:
# status = memory_service.get_module_document_status(5)
# print(f"Module 5 has document: {status.get('has_document')}")
