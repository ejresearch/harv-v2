"""
UNIVERSAL MODULE ENHANCEMENT
Add this code to your existing backend/app/models/course.py Module class
"""

import json
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime
from typing import Optional, Dict, List

class Module(Base, TimestampMixin):
    """
    Enhanced Module class with UNIVERSAL document intelligence
    Works with ALL 15 modules - backward compatible
    """
    
    # ... ALL YOUR EXISTING FIELDS REMAIN UNCHANGED ...
    
    # NEW: Universal document intelligence fields (all optional)
    source_document_path = Column(String, nullable=True, comment="Path to uploaded document")
    source_document_name = Column(String, nullable=True, comment="Original filename")
    source_document_type = Column(String, nullable=True, comment="pdf, docx, pptx, txt")
    document_processed_at = Column(DateTime, nullable=True, comment="When AI processed document")
    extracted_concepts = Column(Text, nullable=True, comment="AI-extracted concepts (JSON)")
    extracted_examples = Column(Text, nullable=True, comment="Real-world examples (JSON)")
    socratic_questions = Column(Text, nullable=True, comment="Generated questions (JSON)")
    document_summary = Column(Text, nullable=True, comment="AI-generated summary")
    
    def has_document_intelligence(self) -> bool:
        """Check if this module has document intelligence available"""
        return bool(
            self.extracted_concepts and 
            self.extracted_examples and
            self.document_processed_at
        )
    
    def get_document_concepts(self) -> Dict[str, str]:
        """Get extracted concepts as dictionary"""
        if not self.extracted_concepts:
            return {}
        try:
            return json.loads(self.extracted_concepts)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def get_document_examples(self) -> Dict[str, str]:
        """Get extracted examples as dictionary"""
        if not self.extracted_examples:
            return {}
        try:
            return json.loads(self.extracted_examples)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def get_socratic_questions(self) -> Dict[str, List[str]]:
        """Get generated Socratic questions as dictionary"""
        if not self.socratic_questions:
            return {"concept_questions": [], "application_questions": []}
        try:
            return json.loads(self.socratic_questions)
        except (json.JSONDecodeError, TypeError):
            return {"concept_questions": [], "application_questions": []}
    
    def get_document_status(self) -> Dict[str, any]:
        """Get complete document intelligence status"""
        return {
            "has_document": self.has_document_intelligence(),
            "document_name": self.source_document_name,
            "document_type": self.source_document_type,
            "processed_at": self.document_processed_at.isoformat() if self.document_processed_at else None,
            "concepts_count": len(self.get_document_concepts()),
            "examples_count": len(self.get_document_examples()),
            "questions_available": bool(self.socratic_questions)
        }
    
    def clear_document_intelligence(self) -> None:
        """Remove all document intelligence data"""
        self.source_document_path = None
        self.source_document_name = None
        self.source_document_type = None
        self.document_processed_at = None
        self.extracted_concepts = None
        self.extracted_examples = None
        self.socratic_questions = None
        self.document_summary = None

# Copy this enhancement to your existing Module class in course.py
