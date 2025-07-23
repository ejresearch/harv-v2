"""
UNIVERSAL API ENDPOINTS
Add these endpoints to your existing backend/app/api/v1/endpoints/memory.py

These endpoints work with ALL 15 modules for document upload and management
"""

from fastapi import File, UploadFile, HTTPException, Form
from typing import Optional, List
import os
from pathlib import Path
from datetime import datetime

from app.services.document_processor import UniversalDocumentProcessor
from app.core.config import settings

# ADD THESE ENDPOINTS TO YOUR EXISTING MEMORY ROUTER:

@router.post("/modules/{module_id}/upload-document")
async def upload_document_to_module(
    module_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload document to enhance ANY module (1-15) with intelligence
    
    Supported file types: PDF, DOCX, PPTX, TXT
    The document will be processed by AI to extract educational intelligence
    and enhance the module's teaching capabilities.
    """
    
    try:
        # Validate module exists and is in valid range
        if not (1 <= module_id <= 15):
            raise HTTPException(status_code=400, detail="Module ID must be between 1 and 15")
            
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail=f"Module {module_id} not found")
        
        # Validate file type
        processor = UniversalDocumentProcessor(settings.openai_api_key)
        supported_types = processor.get_supported_file_types()
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in supported_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_extension}. Supported: {', '.join(supported_types)}"
            )
        
        # Create upload directory
        upload_dir = f"uploads/modules/module_{module_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save uploaded file with unique name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, safe_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document with AI
        result = await processor.process_document_for_module(
            file_path=file_path,
            module_id=module_id,
            db_session=db,
            original_filename=file.filename
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Document successfully processed for Module {module_id}: {module.title}",
                "module_id": module_id,
                "module_title": module.title,
                "filename": file.filename,
                "file_path": file_path,
                "processing_details": result["processing_details"],
                "enhanced": True,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            # Clean up file if processing failed
            try:
                os.remove(file_path)
            except:
                pass
                
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to process document: {result.get('error', 'Unknown error')}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/modules/{module_id}/document-status")
async def get_module_document_status(
    module_id: int,
    db: Session = Depends(get_db)
):
    """Get document intelligence status for any module (1-15)"""
    
    if not (1 <= module_id <= 15):
        raise HTTPException(status_code=400, detail="Module ID must be between 1 and 15")
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail=f"Module {module_id} not found")
    
    try:
        status = module.get_document_status() if hasattr(module, 'get_document_status') else {
            "has_document": False,
            "message": "Document intelligence not available"
        }
        
        return {
            "module_id": module_id,
            "module_title": module.title,
            **status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.delete("/modules/{module_id}/document")
async def remove_module_document(
    module_id: int,
    db: Session = Depends(get_db)
):
    """Remove document intelligence from a module"""
    
    if not (1 <= module_id <= 15):
        raise HTTPException(status_code=400, detail="Module ID must be between 1 and 15")
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail=f"Module {module_id} not found")
    
    try:
        # Store old file path for cleanup
        old_file_path = module.source_document_path
        
        # Clear document intelligence
        if hasattr(module, 'clear_document_intelligence'):
            module.clear_document_intelligence()
            db.commit()
            
            # Clean up old file
            if old_file_path and os.path.exists(old_file_path):
                try:
                    os.remove(old_file_path)
                except:
                    pass  # Don't fail if file cleanup fails
            
            return {
                "success": True,
                "message": f"Document intelligence removed from Module {module_id}",
                "module_id": module_id,
                "module_title": module.title
            }
        else:
            raise HTTPException(status_code=500, detail="Module does not support document intelligence")
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to remove document: {str(e)}")


@router.post("/modules/bulk-upload")
async def bulk_upload_documents(
    files: List[UploadFile] = File(...),
    module_ids: str = Form(...),  # Comma-separated module IDs
    db: Session = Depends(get_db)
):
    """
    Upload multiple documents to multiple modules
    
    Example: Upload 3 files to modules 1, 5, and 10
    - files: [file1.pdf, file2.docx, file3.pptx]
    - module_ids: "1,5,10"
    """
    
    try:
        # Parse module IDs
        module_id_list = [int(x.strip()) for x in module_ids.split(',')]
        
        if len(files) != len(module_id_list):
            raise HTTPException(
                status_code=400,
                detail=f"Number of files ({len(files)}) must match number of module IDs ({len(module_id_list)})"
            )
        
        # Validate all module IDs
        for mid in module_id_list:
            if not (1 <= mid <= 15):
                raise HTTPException(status_code=400, detail=f"Module ID {mid} must be between 1 and 15")
        
        processor = UniversalDocumentProcessor(settings.openai_api_key)
        results = []
        
        # Process each file-module pair
        for file, module_id in zip(files, module_id_list):
            # Save file
            upload_dir = f"uploads/modules/module_{module_id}"
            os.makedirs(upload_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(upload_dir, safe_filename)
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Process with AI
            result = await processor.process_document_for_module(
                file_path=file_path,
                module_id=module_id,
                db_session=db,
                original_filename=file.filename
            )
            
            results.append({
                "module_id": module_id,
                "filename": file.filename,
                "success": result["success"],
                "error": result.get("error"),
                "processing_details": result.get("processing_details", {})
            })
        
        successful_uploads = sum(1 for r in results if r["success"])
        
        return {
            "total_files": len(files),
            "successful_uploads": successful_uploads,
            "failed_uploads": len(files) - successful_uploads,
            "results": results
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid module_ids format. Use comma-separated integers.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk upload failed: {str(e)}")


@router.get("/modules/document-overview")
async def get_all_modules_document_status(db: Session = Depends(get_db)):
    """Get document intelligence status for all 15 modules"""
    
    modules = db.query(Module).filter(Module.id.between(1, 15)).all()
    
    overview = {
        "total_modules": 15,
        "modules_with_documents": 0,
        "modules_without_documents": 0,
        "module_details": []
    }
    
    for module in modules:
        if hasattr(module, 'get_document_status'):
            status = module.get_document_status()
            has_doc = status.get("has_document", False)
        else:
            has_doc = False
            status = {"has_document": False}
        
        if has_doc:
            overview["modules_with_documents"] += 1
        else:
            overview["modules_without_documents"] += 1
        
        overview["module_details"].append({
            "module_id": module.id,
            "title": module.title,
            "has_document": has_doc,
            **status
        })
    
    return overview

# Usage examples for testing:
# 
# 1. Upload document to Module 5:
# curl -X POST -F "file=@textbook_chapter5.pdf" \
#   http://localhost:8000/api/v1/memory/modules/5/upload-document
# 
# 2. Check Module 3 status:
# curl http://localhost:8000/api/v1/memory/modules/3/document-status
# 
# 3. Get overview of all modules:
# curl http://localhost:8000/api/v1/memory/modules/document-overview
