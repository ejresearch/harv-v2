#!/bin/bash
# Complete Implementation with Your Real Module 1 Content

echo "🚀 IMPLEMENTING DOCUMENT DIFFUSION WITH REAL MODULE 1 CONTENT"
echo "============================================================="
echo ""

# Step 1: Copy your real content into the project
echo "📄 Step 1: Setting up your real Module 1 content"
echo "------------------------------------------------"

# Copy the file from desktop to project
cp ~/Desktop/1_Your4Worlds.txt ./module1_content.txt

if [[ -f "./module1_content.txt" ]]; then
    echo "✅ Module 1 content copied successfully"
    echo "📊 Content preview:"
    head -5 ./module1_content.txt
    echo "..."
else
    echo "❌ Could not find 1_Your4Worlds.txt on desktop"
    echo "💡 Tip: Make sure the file is exactly at ~/Desktop/1_Your4Worlds.txt"
    echo "    Or manually copy it to your harv-v2 directory as module1_content.txt"
    exit 1
fi

echo ""

# Step 2: Enhanced implementation test script
echo "🧪 Step 2: Creating test script for real content"
echo "-----------------------------------------------"

cat > backend/test_real_module1.py << 'EOF'
#!/usr/bin/env python3
"""
Test Document Upload with Real Module 1 Content
Uses your actual 1_Your4Worlds.txt content
"""

import asyncio
import sys
import os
sys.path.append('.')

from app.core.database import SessionLocal
from app.services.document_processor import UniversalDocumentProcessor
from app.models.course import Module

async def test_real_module1_upload():
    """Test with your actual Module 1 content"""
    
    print("🧪 Testing with REAL Module 1 Content: 1_Your4Worlds.txt")
    print("=" * 60)
    
    # Path to your real content
    content_file = "../module1_content.txt"
    
    if not os.path.exists(content_file):
        print("❌ Module 1 content file not found!")
        print(f"Expected: {os.path.abspath(content_file)}")
        print("💡 Make sure you copied 1_Your4Worlds.txt to the project root")
        return False
    
    # Show content preview
    with open(content_file, 'r') as f:
        content_preview = f.read()[:500]
    print(f"📄 Content Preview (first 500 chars):")
    print(f"{content_preview}...")
    print()
    
    try:
        # Initialize processor with your OpenAI key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OPENAI_API_KEY not set!")
            print("Run: export OPENAI_API_KEY='your-key-here'")
            return False
        
        processor = UniversalDocumentProcessor(api_key)
        print("✅ Document processor initialized")
        
        # Create database session
        db = SessionLocal()
        print("✅ Database connection established")
        
        # Process your real Module 1 content
        print("🤖 Processing your Module 1 content with AI...")
        print("   This may take 10-30 seconds...")
        
        result = await processor.process_document_for_module(
            file_path=content_file,
            module_id=1,  # Module 1: Your Four Worlds
            db_session=db,
            original_filename="1_Your4Worlds.txt"
        )
        
        print(f"\n📊 Processing Results:")
        print(f"Success: {result['success']}")
        
        if result['success']:
            print(f"🎉 YOUR MODULE 1 IS NOW DOCUMENT-INTELLIGENT!")
            
            # Show detailed results
            details = result.get('processing_details', {})
            ai_details = details.get('ai_analysis', {})
            
            print(f"\n📈 Processing Statistics:")
            print(f"Content Length: {details.get('content_length', 0):,} characters")
            print(f"Concepts Extracted: {ai_details.get('concepts_extracted', 0)}")
            print(f"Examples Found: {ai_details.get('examples_found', 0)}")
            print(f"Questions Generated: {ai_details.get('questions_generated', 0)}")
            
            # Test the enhanced module
            module = db.query(Module).filter(Module.id == 1).first()
            if module and module.has_document_intelligence():
                print(f"\n🧠 Module 1 Intelligence Summary:")
                
                concepts = module.get_document_concepts()
                examples = module.get_document_examples() 
                questions = module.get_socratic_questions()
                
                print(f"📚 Key Concepts Extracted:")
                for i, (concept, definition) in enumerate(concepts.items(), 1):
                    print(f"  {i}. {concept}: {definition[:100]}...")
                
                print(f"\n📝 Real-World Examples Found:")
                for i, (example, description) in enumerate(examples.items(), 1):
                    print(f"  {i}. {example}: {description[:100]}...")
                
                print(f"\n❓ Socratic Questions Generated:")
                concept_questions = questions.get('concept_questions', [])
                for i, question in enumerate(concept_questions[:3], 1):
                    print(f"  {i}. {question}")
                
                print(f"\n✅ Module 1 is now ready for intelligent tutoring!")
                return True
        else:
            print(f"❌ Processing failed: {result.get('error')}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

async def test_memory_integration():
    """Test that your memory system can use the document intelligence"""
    
    print(f"\n🧠 Testing Memory System Integration")
    print("=" * 40)
    
    try:
        db = SessionLocal()
        module = db.query(Module).filter(Module.id == 1).first()
        
        if module and module.has_document_intelligence():
            print("✅ Memory system can access document intelligence")
            
            # Simulate what your memory service will do
            concepts = module.get_document_concepts()
            examples = module.get_document_examples()
            
            print(f"\n🎯 Your AI tutor now knows:")
            print(f"- {len(concepts)} specific concepts from your textbook")
            print(f"- {len(examples)} real-world examples to reference")
            print(f"- Generated Socratic questions for discovery-based learning")
            
            print(f"\n💡 Before: Generic responses about communication")
            print(f"💡 After: Specific references to YOUR textbook content")
            
            return True
        else:
            print("❌ Module 1 doesn't have document intelligence yet")
            return False
            
    except Exception as e:
        print(f"❌ Memory integration test failed: {e}")
        return False
    finally:
        db.close()

async def main():
    """Run complete test with real content"""
    
    print("🚀 TESTING DOCUMENT DIFFUSION WITH YOUR REAL MODULE 1 CONTENT")
    print("=" * 70)
    
    # Test document processing
    success = await test_real_module1_upload()
    
    if success:
        # Test memory integration
        memory_success = await test_memory_integration()
        
        if memory_success:
            print(f"\n🎉 COMPLETE SUCCESS!")
            print("=" * 50)
            print("✅ Your real Module 1 content processed successfully")
            print("✅ Document intelligence extracted and stored")
            print("✅ Memory system integration working")
            print("✅ Module 1 is now textbook-intelligent!")
            print("")
            print("🎯 Next Steps:")
            print("- Test with students asking questions about Module 1")
            print("- AI will now reference YOUR specific textbook content")
            print("- Expand to other modules when ready")
        else:
            print(f"\n⚠️ Partial Success - document processed but memory needs work")
    else:
        print(f"\n❌ Failed - check error messages above")

if __name__ == "__main__":
    asyncio.run(main())
EOF

echo "✅ Test script created for your real Module 1 content"

echo ""
echo "🎯 READY TO IMPLEMENT!"
echo "====================="
echo ""
echo "Your implementation steps:"
echo "1. First, make sure you've enhanced your Module model (Step 1 from earlier)"
echo "2. Run the database migration (Step 2 from earlier)" 
echo "3. Create the document processor service (Step 3 from earlier)"
echo "4. Then run this test:"
echo ""
echo "   cd backend"
echo "   python test_real_module1.py"
echo ""
echo "This will:"
echo "✅ Use your actual 1_Your4Worlds.txt content"
echo "✅ Process it with AI to extract concepts and examples"
echo "✅ Store the intelligence in Module 1"
echo "✅ Test that your memory system can access it"
echo ""
echo "🎉 Result: Your AI tutor will know YOUR specific textbook content!"
echo "   Instead of generic responses, it will reference your actual material"
