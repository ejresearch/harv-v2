# backend/app/api/v1/endpoints/admin.py
"""
Admin Content Management - Claude Projects Style Editor
In-browser content editing with file upload/download capabilities
"""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import json
import io
import tempfile
import os
from pathlib import Path

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.course import Module

router = APIRouter()

# =========================================================================
# PYDANTIC SCHEMAS
# =========================================================================

class ModuleContentUpdate(BaseModel):
    title: str
    description: str
    system_prompt: str
    module_prompt: str
    learning_objectives: List[str]
    resources: Optional[str] = None
    difficulty_level: str = "intermediate"
    estimated_duration: int = 45
    is_active: bool = True

class BulkContentUpdate(BaseModel):
    modules: List[ModuleContentUpdate]

class ContentExportFormat(BaseModel):
    include_system_prompts: bool = True
    include_module_prompts: bool = True
    include_objectives: bool = True
    include_metadata: bool = True
    format_type: str = "structured_text"  # "structured_text", "json", "yaml"

class FileUploadResult(BaseModel):
    filename: str
    modules_processed: int
    modules_updated: List[int]
    errors: List[str]
    warnings: List[str]

# =========================================================================
# CONTENT PARSING FUNCTIONS
# =========================================================================

def parse_structured_text_content(content: str) -> List[Dict[str, Any]]:
    """
    Parse Claude Projects style structured text content
    Format:
    # MODULE: Module Title
    # DESCRIPTION: Module description
    # DIFFICULTY: beginner|intermediate|advanced
    # DURATION: 45
    # SYSTEM_PROMPT:
    Content here...
    # END
    # MODULE_PROMPT:
    Content here...
    # END
    # LEARNING_OBJECTIVES:
    - Objective 1
    - Objective 2
    # END
    # RESOURCES:
    Additional resources...
    # END
    ---
    # MODULE: Next Module...
    """
    
    modules = []
    lines = content.strip().split('\n')
    
    current_module = {}
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        
        # Module separator
        if line == "---":
            if current_module:
                modules.append(current_module)
            current_module = {}
            current_section = None
            current_content = []
            continue
        
        # Section headers
        if line.startswith("# MODULE:"):
            if current_section and current_content:
                current_module[current_section] = process_section_content(current_section, current_content)
            current_module["title"] = line.replace("# MODULE:", "").strip()
            current_section = None
            current_content = []
            
        elif line.startswith("# DESCRIPTION:"):
            current_module["description"] = line.replace("# DESCRIPTION:", "").strip()
            
        elif line.startswith("# DIFFICULTY:"):
            current_module["difficulty_level"] = line.replace("# DIFFICULTY:", "").strip()
            
        elif line.startswith("# DURATION:"):
            try:
                current_module["estimated_duration"] = int(line.replace("# DURATION:", "").strip())
            except ValueError:
                current_module["estimated_duration"] = 45
                
        elif line.startswith("# SYSTEM_PROMPT:"):
            if current_section and current_content:
                current_module[current_section] = process_section_content(current_section, current_content)
            current_section = "system_prompt"
            current_content = []
            
        elif line.startswith("# MODULE_PROMPT:"):
            if current_section and current_content:
                current_module[current_section] = process_section_content(current_section, current_content)
            current_section = "module_prompt"
            current_content = []
            
        elif line.startswith("# LEARNING_OBJECTIVES:"):
            if current_section and current_content:
                current_module[current_section] = process_section_content(current_section, current_content)
            current_section = "learning_objectives"
            current_content = []
            
        elif line.startswith("# RESOURCES:"):
            if current_section and current_content:
                current_module[current_section] = process_section_content(current_section, current_content)
            current_section = "resources"
            current_content = []
            
        elif line == "# END":
            if current_section and current_content:
                current_module[current_section] = process_section_content(current_section, current_content)
            current_section = None
            current_content = []
            
        else:
            # Content line
            if current_section:
                current_content.append(line)
    
    # Handle last section and module
    if current_section and current_content:
        current_module[current_section] = process_section_content(current_section, current_content)
    
    if current_module:
        modules.append(current_module)
    
    return modules

def process_section_content(section_type: str, content_lines: List[str]) -> Any:
    """Process content based on section type"""
    
    if section_type == "learning_objectives":
        # Parse list items
        objectives = []
        for line in content_lines:
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                objectives.append(line[1:].strip())
            elif line:  # Non-empty line without bullet
                objectives.append(line)
        return objectives
    else:
        # Text content
        return '\n'.join(content_lines).strip()

def generate_structured_export(modules: List[Module], format_config: ContentExportFormat) -> str:
    """Generate structured text export in Claude Projects format"""
    
    export_lines = []
    
    for i, module in enumerate(modules):
        if i > 0:
            export_lines.append("---")
            export_lines.append("")
        
        # Basic info
        export_lines.append(f"# MODULE: {module.title}")
        export_lines.append(f"# DESCRIPTION: {module.description}")
        
        if format_config.include_metadata:
            export_lines.append(f"# DIFFICULTY: {module.difficulty_level or 'intermediate'}")
            export_lines.append(f"# DURATION: {module.estimated_duration or 45}")
        
        export_lines.append("")
        
        # System prompt
        if format_config.include_system_prompts and module.system_prompt:
            export_lines.append("# SYSTEM_PROMPT:")
            export_lines.extend(module.system_prompt.split('\n'))
            export_lines.append("# END")
            export_lines.append("")
        
        # Module prompt
        if format_config.include_module_prompts and module.module_prompt:
            export_lines.append("# MODULE_PROMPT:")
            export_lines.extend(module.module_prompt.split('\n'))
            export_lines.append("# END")
            export_lines.append("")
        
        # Learning objectives
        if format_config.include_objectives and module.learning_objectives:
            try:
                objectives = json.loads(module.learning_objectives)
                export_lines.append("# LEARNING_OBJECTIVES:")
                for objective in objectives:
                    export_lines.append(f"- {objective}")
                export_lines.append("# END")
                export_lines.append("")
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Resources
        if module.resources and module.resources.strip():
            export_lines.append("# RESOURCES:")
            export_lines.extend(module.resources.split('\n'))
            export_lines.append("# END")
            export_lines.append("")
    
    return '\n'.join(export_lines)

# =========================================================================
# API ENDPOINTS
# =========================================================================

@router.get("/modules/{module_id}/content")
async def get_module_content_for_editing(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get module content in format suitable for editing
    Returns all editable fields for the content management interface
    """
    
    # TODO: Add admin role check
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Parse learning objectives
    try:
        learning_objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
    except (json.JSONDecodeError, TypeError):
        learning_objectives = []
    
    return {
        "module_id": module.id,
        "title": module.title,
        "description": module.description,
        "system_prompt": module.system_prompt or "",
        "module_prompt": module.module_prompt or "",
        "learning_objectives": learning_objectives,
        "resources": module.resources or "",
        "difficulty_level": module.difficulty_level or "intermediate",
        "estimated_duration": module.estimated_duration or 45,
        "is_active": module.is_active,
        "created_at": module.created_at.isoformat(),
        "updated_at": module.updated_at.isoformat(),
        "edit_session_id": f"edit_{module_id}_{int(datetime.utcnow().timestamp())}"
    }

@router.put("/modules/{module_id}/content")
async def update_module_content(
    module_id: int,
    content_update: ModuleContentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update module content through the content management interface
    Supports real-time editing with validation
    """
    
    # TODO: Add admin role check
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Store original values for change tracking
    original_values = {
        "title": module.title,
        "description": module.description,
        "system_prompt": module.system_prompt,
        "module_prompt": module.module_prompt,
        "learning_objectives": module.learning_objectives,
        "resources": module.resources,
        "difficulty_level": module.difficulty_level,
        "estimated_duration": module.estimated_duration
    }
    
    # Update fields
    module.title = content_update.title
    module.description = content_update.description
    module.system_prompt = content_update.system_prompt
    module.module_prompt = content_update.module_prompt
    module.learning_objectives = json.dumps(content_update.learning_objectives)
    module.resources = content_update.resources
    module.difficulty_level = content_update.difficulty_level
    module.estimated_duration = content_update.estimated_duration
    module.is_active = content_update.is_active
    module.updated_at = datetime.utcnow()
    
    # Track changes
    changes = []
    for field, original_value in original_values.items():
        new_value = getattr(module, field)
        if field == "learning_objectives":
            new_value = json.dumps(content_update.learning_objectives)
        
        if str(original_value) != str(new_value):
            changes.append({
                "field": field,
                "old_value": str(original_value)[:100] + "..." if len(str(original_value)) > 100 else str(original_value),
                "new_value": str(new_value)[:100] + "..." if len(str(new_value)) > 100 else str(new_value)
            })
    
    db.commit()
    db.refresh(module)
    
    return {
        "status": "updated",
        "module_id": module_id,
        "title": module.title,
        "changes_made": len(changes),
        "change_details": changes,
        "updated_at": module.updated_at.isoformat(),
        "message": f"Module '{module.title}' updated successfully with {len(changes)} changes"
    }

@router.post("/modules/upload-content")
async def upload_module_content(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload module content from structured text file (Claude Projects style)
    Supports bulk content updates with validation and error reporting
    """
    
    # TODO: Add admin role check
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="Only .txt and .md files are supported")
    
    try:
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Parse content
        parsed_modules = parse_structured_text_content(text_content)
        
        if not parsed_modules:
            raise HTTPException(status_code=400, detail="No valid module content found in file")
        
        # Process each module
        modules_updated = []
        errors = []
        warnings = []
        
        for module_data in parsed_modules:
            try:
                # Validate required fields
                if not module_data.get("title"):
                    errors.append(f"Module missing title: {module_data}")
                    continue
                
                # Find existing module by title or create new
                module = db.query(Module).filter(Module.title == module_data["title"]).first()
                
                if module:
                    # Update existing module
                    action = "updated"
                else:
                    # Create new module
                    module = Module()
                    action = "created"
                    db.add(module)
                
                # Apply updates
                module.title = module_data["title"]
                module.description = module_data.get("description", "")
                module.system_prompt = module_data.get("system_prompt", "")
                module.module_prompt = module_data.get("module_prompt", "")
                module.resources = module_data.get("resources", "")
                module.difficulty_level = module_data.get("difficulty_level", "intermediate")
                module.estimated_duration = module_data.get("estimated_duration", 45)
                module.is_active = True
                module.updated_at = datetime.utcnow()
                
                # Handle learning objectives
                objectives = module_data.get("learning_objectives", [])
                if isinstance(objectives, list):
                    module.learning_objectives = json.dumps(objectives)
                else:
                    module.learning_objectives = json.dumps([objectives] if objectives else [])
                
                modules_updated.append({
                    "id": module.id if hasattr(module, 'id') else "new",
                    "title": module.title,
                    "action": action
                })
                
            except Exception as e:
                errors.append(f"Error processing module '{module_data.get('title', 'unknown')}': {str(e)}")
        
        if modules_updated:
            db.commit()
            
            # Refresh module IDs for new modules
            for i, update_info in enumerate(modules_updated):
                if update_info["id"] == "new":
                    module = db.query(Module).filter(Module.title == update_info["title"]).first()
                    if module:
                        modules_updated[i]["id"] = module.id
        
        return FileUploadResult(
            filename=file.filename,
            modules_processed=len(parsed_modules),
            modules_updated=[info["id"] for info in modules_updated if info["id"] != "new"],
            errors=errors,
            warnings=warnings
        )
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding not supported. Please use UTF-8.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/modules/export-all")
async def export_all_modules(
    format_config: ContentExportFormat = Depends(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export all modules in structured text format
    Generates downloadable file in Claude Projects compatible format
    """
    
    # TODO: Add admin role check
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get all modules
    modules = db.query(Module).filter(Module.is_active == True).order_by(Module.id).all()
    
    if not modules:
        raise HTTPException(status_code=404, detail="No modules found")
    
    # Generate export content
    export_content = generate_structured_export(modules, format_config)
    
    # Create temporary file
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"harv_modules_export_{timestamp}.txt"
    
    # Write to temporary file and return
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
        tmp_file.write(export_content)
        tmp_file_path = tmp_file.name
    
    return FileResponse(
        path=tmp_file_path,
        filename=filename,
        media_type='text/plain',
        background=None  # Don't delete immediately
    )

@router.get("/modules/{module_id}/export")
async def export_single_module(
    module_id: int,
    format_config: ContentExportFormat = Depends(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export single module in structured text format
    """
    
    # TODO: Add admin role check
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Generate export content
    export_content = generate_structured_export([module], format_config)
    
    # Return as downloadable content
    safe_title = "".join(c for c in module.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"module_{module_id}_{safe_title.replace(' ', '_').lower()}.txt"
    
    return {
        "content": export_content,
        "filename": filename,
        "module_title": module.title,
        "generated_at": datetime.utcnow().isoformat()
    }

@router.get("/content-editor/templates")
async def get_content_templates():
    """
    Get content templates for the editor
    Provides examples and starting templates for new modules
    """
    
    templates = {
        "basic_module": {
            "title": "New Communication Module",
            "description": "A foundational module covering key communication concepts",
            "system_prompt": """You are an expert communication theory tutor using Socratic methodology. Your role is to guide students to discover concepts through strategic questioning.

CORE PRINCIPLES:
- Never give direct answers - help students discover insights themselves
- Ask probing questions that lead to breakthrough moments
- Build on student's prior knowledge and experiences
- Use real-world examples they can relate to
- Encourage critical thinking about communication

SOCRATIC STRATEGY:
- Start with student's personal experiences
- Ask "why" and "how" questions
- Help them connect concepts to their own life
- Guide them to see patterns and principles
- Celebrate their discoveries and insights""",
            "module_prompt": """Help students understand [TOPIC FOCUS]. Guide them to discover:

1. [Key concept 1]
2. [Key concept 2]
3. [Key concept 3]

Ask them to consider examples from their daily life where they've experienced these concepts. Guide them to discover how [main insight].""",
            "learning_objectives": [
                "Understand key concept through personal discovery",
                "Apply learning to real-world situations",
                "Make connections to other communication principles"
            ],
            "difficulty_level": "intermediate",
            "estimated_duration": 45
        },
        "advanced_module": {
            "title": "Advanced Communication Analysis",
            "description": "Deep exploration of complex communication phenomena",
            "system_prompt": """You are guiding an advanced student through complex communication analysis. Push them to think critically and make sophisticated connections.

ADVANCED APPROACH:
- Challenge assumptions and conventional wisdom
- Encourage multi-perspective analysis
- Push for deeper "why" questions
- Connect to broader theoretical frameworks
- Demand evidence-based reasoning""",
            "module_prompt": """Challenge students to analyze [ADVANCED TOPIC] from multiple theoretical perspectives. Guide discovery of:

1. [Complex concept 1]
2. [Theoretical framework application]
3. [Critical analysis skills]

Push them to question assumptions and provide evidence for their insights.""",
            "learning_objectives": [
                "Critically analyze complex communication phenomena",
                "Apply multiple theoretical frameworks",
                "Develop evidence-based reasoning skills",
                "Challenge conventional communication assumptions"
            ],
            "difficulty_level": "advanced",
            "estimated_duration": 60
        }
    }
    
    return {
        "templates": templates,
        "usage_guide": {
            "basic_module": "Use for introductory topics with foundational concepts",
            "advanced_module": "Use for complex topics requiring critical thinking",
            "customization_tips": [
                "Replace [TOPIC FOCUS] with your specific subject matter",
                "Adjust learning objectives to match your content goals",
                "Modify system prompts to match teaching style",
                "Set appropriate difficulty level and duration"
            ]
        }
    }

@router.post("/content-editor/validate")
async def validate_module_content(
    content: ModuleContentUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Validate module content before saving
    Provides real-time validation feedback for the content editor
    """
    
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "suggestions": []
    }
    
    # Required field validation
    if not content.title.strip():
        validation_results["errors"].append("Title is required")
        validation_results["valid"] = False
        
    if not content.description.strip():
        validation_results["errors"].append("Description is required")
        validation_results["valid"] = False
        
    if not content.system_prompt.strip():
        validation_results["warnings"].append("System prompt is empty - students won't get personalized guidance")
        
    if not content.learning_objectives:
        validation_results["warnings"].append("No learning objectives defined - progress tracking will be limited")
    
    # Content quality checks
    if len(content.title) > 100:
        validation_results["warnings"].append("Title is very long - consider shortening for better display")
        
    if len(content.description) < 50:
        validation_results["warnings"].append("Description is quite short - consider adding more detail")
        
    if content.system_prompt and len(content.system_prompt) < 100:
        validation_results["warnings"].append("System prompt is short - consider adding more teaching guidance")
        
    # Socratic methodology checks
    if content.system_prompt:
        socratic_keywords = ["question", "discover", "guide", "socratic", "why", "how"]
        if not any(keyword in content.system_prompt.lower() for keyword in socratic_keywords):
            validation_results["suggestions"].append("Consider adding Socratic questioning guidance to the system prompt")
            
        if "answer" in content.system_prompt.lower() and "don't" not in content.system_prompt.lower():
            validation_results["warnings"].append("System prompt might encourage direct answers instead of discovery")
    
    # Learning objectives validation
    if len(content.learning_objectives) > 7:
        validation_results["warnings"].append("Many learning objectives - consider focusing on 3-5 key goals")
        
    for i, objective in enumerate(content.learning_objectives):
        if len(objective.strip()) < 10:
            validation_results["warnings"].append(f"Objective {i+1} is very short - be more specific")
            
    # Duration validation
    if content.estimated_duration < 15:
        validation_results["warnings"].append("Very short estimated duration - ensure sufficient learning time")
    elif content.estimated_duration > 120:
        validation_results["warnings"].append("Very long estimated duration - consider breaking into smaller modules")
    
    return validation_results
