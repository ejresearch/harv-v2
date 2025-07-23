# Universal Document Diffusion Testing Guide

## 🎯 Overview
This guide helps you test the universal document diffusion integration with all 15 modules.

## 🚀 Quick Start Testing

### 1. Start Your Server
```bash
cd backend
uvicorn app.main:app --reload
```

### 2. Check Integration Status
```bash
# Check all modules status
curl http://localhost:8000/api/v1/memory/modules/document-overview
```

### 3. Upload Test Documents

#### Upload to Module 1 (Your Four Worlds)
```bash
curl -X POST \
  -F "file=@your_textbook_chapter1.pdf" \
  http://localhost:8000/api/v1/memory/modules/1/upload-document
```

#### Upload to Module 5 (Digital Revolution)
```bash
curl -X POST \
  -F "file=@digital_media_chapter.docx" \
  http://localhost:8000/api/v1/memory/modules/5/upload-document
```

#### Upload to Any Module (1-15)
```bash
curl -X POST \
  -F "file=@communication_theory.pptx" \
  http://localhost:8000/api/v1/memory/modules/3/upload-document
```

### 4. Test Enhanced Memory Responses

#### Before Document Upload
```bash
curl "http://localhost:8000/api/v1/memory/enhanced/1?current_message=What%20is%20communication"
```
**Expected**: Generic response about communication

#### After Document Upload
```bash
curl "http://localhost:8000/api/v1/memory/enhanced/1?current_message=What%20is%20communication"
```
**Expected**: Response using specific examples from your uploaded document

## 🧪 Comprehensive Testing Scenarios

### Scenario 1: Single Module Enhancement
1. Choose one module (e.g., Module 3)
2. Upload relevant course document
3. Test before/after responses
4. Verify document-specific content in AI responses

### Scenario 2: Multiple Module Enhancement
1. Upload documents to Modules 1, 5, and 10
2. Test each module's enhanced responses
3. Verify cross-module learning still works
4. Check that non-enhanced modules still function normally

### Scenario 3: Bulk Upload Testing
```bash
# Upload 3 files to modules 1, 2, 3
curl -X POST \
  -F "files=@chapter1.pdf" \
  -F "files=@chapter2.docx" \
  -F "files=@chapter3.pptx" \
  -F "module_ids=1,2,3" \
  http://localhost:8000/api/v1/memory/modules/bulk-upload
```

### Scenario 4: Document Removal
```bash
# Remove document intelligence from Module 1
curl -X DELETE http://localhost:8000/api/v1/memory/modules/1/document
```

## 📊 Expected Results

### Enhanced Module Response Example
```json
{
  "memory_layers": {
    "module_data": {
      "teaching_configuration": {
        "document_intelligence": {
          "source_document": "communication_theory.pdf",
          "extracted_concepts": {
            "shannon_weaver": "Mathematical communication model...",
            "feedback_loops": "Two-way communication process..."
          },
          "real_world_examples": {
            "social_media": "Facebook interaction patterns...",
            "broadcast_tv": "One-way mass communication..."
          },
          "enhanced": true
        }
      }
    }
  }
}
```

### AI Response Enhancement
- **Before**: "Communication is the process of sending messages..."
- **After**: "Consider the Shannon-Weaver model we discussed - how does feedback change the communication process in social media compared to broadcast television?"

## 🔍 Troubleshooting

### Document Upload Fails
```bash
# Check supported file types
curl http://localhost:8000/api/v1/memory/modules/1/document-status
```

### AI Analysis Fails
- Check OpenAI API key in settings
- Verify document content is readable
- Check file size (should be < 50MB)

### Memory Enhancement Not Working
- Verify module model has document intelligence methods
- Check memory service integration
- Confirm database migration completed

## 📈 Performance Testing

### Load Testing
```bash
# Test multiple simultaneous uploads
for i in {1..5}; do
  curl -X POST -F "file=@test_doc.pdf" \
    http://localhost:8000/api/v1/memory/modules/$i/upload-document &
done
```

### Memory Performance
```bash
# Test enhanced memory assembly speed
time curl "http://localhost:8000/api/v1/memory/enhanced/1?current_message=test"
```

## ✅ Success Criteria

### Integration Success
- [ ] All 15 modules show in document overview
- [ ] Documents upload successfully to any module
- [ ] AI extracts concepts and examples
- [ ] Memory system uses document intelligence
- [ ] Non-enhanced modules still work normally

### Response Quality
- [ ] AI references specific document content
- [ ] Socratic questions use document examples
- [ ] Cross-module learning preserved
- [ ] Teaching strategy enhanced with document knowledge

### System Stability
- [ ] No breaking changes to existing functionality
- [ ] Graceful fallback when documents unavailable
- [ ] Proper error handling for invalid uploads
- [ ] Memory system performance maintained

## 🎯 Module-Specific Testing

Test each of your 15 modules with relevant content:

1. **Your Four Worlds**: Upload communication theory textbook
2. **Writing: Persistence of Words**: Upload writing/literacy document
3. **Books: Birth of Mass Communication**: Upload media history content
4. **Mass Communication Theory**: Upload theoretical frameworks
5. **Digital Revolution**: Upload digital media analysis
6. **Module 6-15**: Upload any relevant communication course materials

The system should adapt the AI responses to each module's specific content while maintaining your existing pedagogical approach.
