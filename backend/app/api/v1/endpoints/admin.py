# backend/app/api/v1/endpoints/admin.py
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json
import re

from ....core.database import get_db
from ....core.security import get_current_user
from ....models.user import User
from ....models.course import Module

router = APIRouter()

class ModuleContentUpdate(BaseModel):
    title: str
    description: str
    system_prompt: str
    module_prompt: str
    learning_objectives: List[str]
    resources: Optional[str] = None
    difficulty_level: str = "intermediate"
    estimated_duration: int = 45

class ContentExportResponse(BaseModel):
    content: str
    filename: str

class ContentUploadResponse(BaseModel):
    status: str
    filename: str
    module_id: int
    fields_updated: List[str]
    message: str

@router.put("/modules/{module_id}/content")
async def update_module_content(
    module_id: int,
    content: ModuleContentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update module content through admin interface"""
    
    # TODO: Add admin role check in production
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        
        # Track what fields are being updated
        updated_fields = []
        
        # Update all fields
        if module.title != content.title:
            module.title = content.title
            updated_fields.append("title")
            
        if module.description != content.description:
            module.description = content.description
            updated_fields.append("description")
            
        if module.system_prompt != content.system_prompt:
            module.system_prompt = content.system_prompt
            updated_fields.append("system_prompt")
            
        if module.module_prompt != content.module_prompt:
            module.module_prompt = content.module_prompt
            updated_fields.append("module_prompt")
            
        # Handle learning objectives (stored as JSON string)
        current_objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
        if current_objectives != content.learning_objectives:
            module.learning_objectives = json.dumps(content.learning_objectives)
            updated_fields.append("learning_objectives")
            
        if (module.resources or "") != (content.resources or ""):
            module.resources = content.resources
            updated_fields.append("resources")
            
        if module.difficulty_level != content.difficulty_level:
            module.difficulty_level = content.difficulty_level
            updated_fields.append("difficulty_level")
            
        if module.estimated_duration != content.estimated_duration:
            module.estimated_duration = content.estimated_duration
            updated_fields.append("estimated_duration")
        
        db.commit()
        db.refresh(module)
        
        return {
            "status": "success",
            "message": f"Module content updated successfully",
            "module_id": module_id,
            "title": module.title,
            "fields_updated": updated_fields,
            "updated_at": module.updated_at.isoformat(),
            "total_changes": len(updated_fields)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update module content: {str(e)}")

@router.post("/modules/{module_id}/upload-content", response_model=ContentUploadResponse)
async def upload_module_content(
    module_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload module content from text file (Claude Projects style)"""
    
    try:
        # Validate file type
        if not file.filename.endswith('.txt'):
            raise HTTPException(status_code=400, detail="Only .txt files are supported")
        
        # Validate file size (max 1MB)
        content = await file.read()
        if len(content) > 1024 * 1024:  # 1MB limit
            raise HTTPException(status_code=400, detail="File too large (max 1MB)")
        
        text_content = content.decode('utf-8')
        
        # Parse content using structured format
        parsed_content = parse_module_content_file(text_content)
        
        if not parsed_content:
            raise HTTPException(status_code=400, detail="No valid content found in file. Please check the format.")
        
        # Get module
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        
        # Track updated fields
        fields_updated = []
        
        # Apply parsed content to module
        if 'title' in parsed_content and parsed_content['title'].strip():
            module.title = parsed_content['title'].strip()
            fields_updated.append('title')
            
        if 'description' in parsed_content and parsed_content['description'].strip():
            module.description = parsed_content['description'].strip()
            fields_updated.append('description')
            
        if 'system_prompt' in parsed_content and parsed_content['system_prompt'].strip():
            module.system_prompt = parsed_content['system_prompt'].strip()
            fields_updated.append('system_prompt')
            
        if 'module_prompt' in parsed_content and parsed_content['module_prompt'].strip():
            module.module_prompt = parsed_content['module_prompt'].strip()
            fields_updated.append('module_prompt')
            
        if 'learning_objectives' in parsed_content and parsed_content['learning_objectives']:
            module.learning_objectives = json.dumps(parsed_content['learning_objectives'])
            fields_updated.append('learning_objectives')
            
        if 'resources' in parsed_content and parsed_content['resources'].strip():
            module.resources = parsed_content['resources'].strip()
            fields_updated.append('resources')
        
        db.commit()
        
        return ContentUploadResponse(
            status="success",
            filename=file.filename,
            module_id=module_id,
            fields_updated=fields_updated,
            message=f"Successfully uploaded {file.filename} and updated {len(fields_updated)} fields"
        )
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/modules/{module_id}/export-content", response_model=ContentExportResponse)
async def export_module_content(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export module content as structured text file (Claude Projects compatible)"""
    
    try:
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        
        # Parse objectives
        objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
        
        # Create structured export content
        export_content = f"""# TITLE: {module.title or 'Untitled Module'}
# DESCRIPTION: {module.description or 'No description provided'}

# SYSTEM_PROMPT:
{module.system_prompt or 'No system prompt defined'}
# END

# MODULE_PROMPT:
{module.module_prompt or 'No module prompt defined'}
# END

# LEARNING_OBJECTIVES:
{chr(10).join(f"- {obj}" for obj in objectives) if objectives else "- No objectives defined"}
# END

# RESOURCES:
{module.resources or 'No additional resources'}
# END

# METADATA:
# Difficulty Level: {module.difficulty_level}
# Estimated Duration: {module.estimated_duration} minutes
# Module ID: {module.id}
# Last Updated: {module.updated_at.isoformat() if module.updated_at else 'Never'}
# END
"""
        
        # Create safe filename
        safe_title = re.sub(r'[^\w\s-]', '', module.title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title).lower()
        filename = f"module_{module_id}_{safe_title}.txt"
        
        return ContentExportResponse(
            content=export_content,
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/modules/bulk-export")
async def bulk_export_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export all modules as structured text files in a ZIP-like format"""
    
    try:
        modules = db.query(Module).filter(Module.is_active == True).all()
        
        exports = []
        for module in modules:
            objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
            
            content = f"""# TITLE: {module.title or 'Untitled Module'}
# DESCRIPTION: {module.description or 'No description provided'}

# SYSTEM_PROMPT:
{module.system_prompt or 'No system prompt defined'}
# END

# MODULE_PROMPT:
{module.module_prompt or 'No module prompt defined'}
# END

# LEARNING_OBJECTIVES:
{chr(10).join(f"- {obj}" for obj in objectives) if objectives else "- No objectives defined"}
# END

# RESOURCES:
{module.resources or 'No additional resources'}
# END
"""
            
            safe_title = re.sub(r'[^\w\s-]', '', module.title).strip()
            safe_title = re.sub(r'[-\s]+', '_', safe_title).lower()
            filename = f"module_{module.id}_{safe_title}.txt"
            
            exports.append({
                "filename": filename,
                "content": content,
                "module_id": module.id,
                "title": module.title
            })
        
        return {
            "status": "success",
            "total_modules": len(exports),
            "exports": exports,
            "message": f"Successfully exported {len(exports)} modules"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk export failed: {str(e)}")

def parse_module_content_file(content: str) -> Dict[str, Any]:
    """Parse structured text file for module content (Claude Projects style format)"""
    lines = content.strip().split('\n')
    parsed = {}
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.rstrip()  # Remove trailing whitespace
        
        # Check for section headers
        if line.startswith('# TITLE:'):
            parsed['title'] = line.replace('# TITLE:', '').strip()
        elif line.startswith('# DESCRIPTION:'):
            parsed['description'] = line.replace('# DESCRIPTION:', '').strip()
        elif line.startswith('# SYSTEM_PROMPT:'):
            current_section = 'system_prompt'
            current_content = []
        elif line.startswith('# MODULE_PROMPT:'):
            current_section = 'module_prompt'
            current_content = []
        elif line.startswith('# LEARNING_OBJECTIVES:'):
            current_section = 'learning_objectives'
            current_content = []
        elif line.startswith('# RESOURCES:'):
            current_section = 'resources'
            current_content = []
        elif line.startswith('# END') or line.strip() == '#':
            # End of section - process accumulated content
            if current_section and current_content:
                if current_section == 'learning_objectives':
                    # Parse as list (one objective per line, remove bullets)
                    objectives = []
                    for obj_line in current_content:
                        clean_obj = obj_line.strip().lstrip('- •*').strip()
                        if clean_obj:
                            objectives.append(clean_obj)
                    parsed[current_section] = objectives
                else:
                    # Parse as text block
                    parsed[current_section] = '\n'.join(current_content).strip()
            current_section = None
            current_content = []
        elif line.startswith('# METADATA:') or line.startswith('# Difficulty') or line.startswith('# Estimated') or line.startswith('# Module ID') or line.startswith('# Last Updated'):
            # Skip metadata lines
            continue
        else:
            # Content line - add to current section if we're in one
            if current_section:
                current_content.append(line)
    
    # Handle case where file ends without # END
    if current_section and current_content:
        if current_section == 'learning_objectives':
            objectives = []
            for obj_line in current_content:
                clean_obj = obj_line.strip().lstrip('- •*').strip()
                if clean_obj:
                    objectives.append(clean_obj)
            parsed[current_section] = objectives
        else:
            parsed[current_section] = '\n'.join(current_content).strip()
    
    return parsed

@router.get("/content-format-guide")
async def get_content_format_guide():
    """Get the format guide for uploading module content"""
    
    format_example = """# TITLE: Your Four Worlds
# DESCRIPTION: Communication models, perception, and the four worlds we live in

# SYSTEM_PROMPT:
You are an expert communication theory tutor using Socratic methodology. Your role is to guide students to discover concepts about perception, communication models, and the four worlds concept through strategic questioning.

CORE PRINCIPLES:
- Never give direct answers - help students discover insights themselves
- Ask probing questions that lead to breakthrough moments
- Build on student's prior knowledge and experiences
- Use real-world examples they can relate to
# END

# MODULE_PROMPT:
Help students understand how different perceptual worlds create different communication realities. Focus on:

1. The difference between being a passive receiver vs active participant in communication
2. How we all live in multiple worlds simultaneously 
3. The role of perception in shaping our communication experiences
4. How scripts and mental models influence understanding

Ask them to consider examples from their daily life where they've experienced these different worlds.
# END

# LEARNING_OBJECTIVES:
- Differentiate between communication receiver and participant
- Describe the four worlds in which each of us lives
- Explain communication models and their value
- Explain what perception is and how it affects communication
- Describe how scripts help understand media messages
# END

# RESOURCES:
Additional readings: McLuhan's Understanding Media (selected chapters), Berlo's SMCR Model, Shannon-Weaver Communication Model diagrams
# END
"""

    return {
        "format_guide": {
            "description": "Upload structured text files to update module content",
            "supported_sections": [
                "TITLE: Module title",
                "DESCRIPTION: Brief module description", 
                "SYSTEM_PROMPT: Core AI tutor instructions",
                "MODULE_PROMPT: Module-specific guidance",
                "LEARNING_OBJECTIVES: List of learning goals (one per line with - prefix)",
                "RESOURCES: Additional materials and references"
            ],
            "format_rules": [
                "Each section starts with # SECTION_NAME:",
                "Content sections end with # END",
                "Learning objectives should be bulleted with - prefix",
                "Use plain text format, UTF-8 encoding",
                "Maximum file size: 1MB"
            ],
            "example": format_example
        },
        "upload_endpoint": "/admin/modules/{module_id}/upload-content",
        "export_endpoint": "/admin/modules/{module_id}/export-content"
    }
