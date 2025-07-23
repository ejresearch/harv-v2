"""Add document intelligence fields to modules

Revision ID: doc_intelligence_universal
Revises: head
Create Date: $(date +%Y-%m-%d %H:%M:%S)

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = 'doc_intelligence_universal'
down_revision = 'head'
branch_labels = None
depends_on = None

def upgrade():
    """Add document intelligence columns to existing modules table"""
    print("🔄 Adding document intelligence fields to modules table...")
    
    # Add document intelligence columns (all nullable for backward compatibility)
    op.add_column('modules', sa.Column('source_document_path', sa.String(), nullable=True, 
                                     comment="Path to uploaded document"))
    op.add_column('modules', sa.Column('source_document_name', sa.String(), nullable=True,
                                     comment="Original filename of uploaded document"))
    op.add_column('modules', sa.Column('source_document_type', sa.String(), nullable=True,
                                     comment="Document type: pdf, docx, pptx, txt"))
    op.add_column('modules', sa.Column('document_processed_at', sa.DateTime(), nullable=True,
                                     comment="When AI processed the document"))
    op.add_column('modules', sa.Column('extracted_concepts', sa.Text(), nullable=True,
                                     comment="AI-extracted key concepts (JSON)"))
    op.add_column('modules', sa.Column('extracted_examples', sa.Text(), nullable=True,
                                     comment="Real-world examples from document (JSON)"))
    op.add_column('modules', sa.Column('socratic_questions', sa.Text(), nullable=True,
                                     comment="Generated question bank (JSON)"))
    op.add_column('modules', sa.Column('document_summary', sa.Text(), nullable=True,
                                     comment="AI-generated summary of document content"))
    
    print("✅ Document intelligence fields added successfully")

def downgrade():
    """Remove document intelligence columns if needed"""
    print("🔄 Removing document intelligence fields...")
    
    op.drop_column('modules', 'document_summary')
    op.drop_column('modules', 'socratic_questions')
    op.drop_column('modules', 'extracted_examples')
    op.drop_column('modules', 'extracted_concepts')
    op.drop_column('modules', 'document_processed_at')
    op.drop_column('modules', 'source_document_type')
    op.drop_column('modules', 'source_document_name')
    op.drop_column('modules', 'source_document_path')
    
    print("✅ Document intelligence fields removed")
