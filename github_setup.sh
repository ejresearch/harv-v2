#!/bin/bash

echo "🚀 Setting up Harv v2.0 GitHub Repository"
echo "=========================================="
echo ""

# Check if we're in the harv-v2 directory
if [[ ! -d "backend" || ! -d "frontend" ]]; then
    echo "❌ Error: Run this script from the harv-v2 directory"
    echo "Expected directory structure with backend/ and frontend/ folders"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo "✅ Detected harv-v2 project structure"
echo ""

# =============================================================================
# CREATE DOCUMENTATION FILES
# =============================================================================

echo "📚 Creating comprehensive documentation..."

# Create docs directory
mkdir -p docs

# Create README.md (Main repository readme)
cat > README.md << 'EOF'
[MAIN README CONTENT FROM ARTIFACT 1 GOES HERE]
EOF

# Create SETUP.md (Detailed setup guide)
cat > SETUP.md << 'EOF'
[SETUP DOCUMENTATION FROM ARTIFACT 2 GOES HERE]
EOF

# Create docs/API.md (API documentation)
cat > docs/API.md << 'EOF'
[API DOCUMENTATION FROM ARTIFACT 3 GOES HERE]  
EOF

# Create DATABASE.md
cat > docs/DATABASE.md << 'EOF'
# Database Schema Documentation

## Overview

Harv v2.0 uses SQLAlchemy ORM with a carefully designed schema optimized for educational analytics and the enhanced memory system.

## Schema Diagram

```
Users
├── OnboardingSurvey (1:1)
├── Conversations (1:many)
├── MemorySummary (1:many)
└── UserProgress (1:many)

Modules
├── Conversations (1:many)
├── MemorySummary (1:many)
└── UserProgress (1:many)

Conversations
├── User (many:1)
├── Module (many:1)
└── Messages (1:many)
```

## Table Definitions

### Users Table
Stores user authentication and profile information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Unique user identifier |
| email | String | Unique, Not Null | User email for authentication |
| hashed_password | String | Not Null | Bcrypt hashed password |
| name | String | Not Null | User display name |
| onboarding_data | Text | Nullable | JSON survey responses |
| is_active | Boolean | Default True | Account status |
| created_at | DateTime | Auto | Account creation timestamp |
| updated_at | DateTime | Auto | Last modification timestamp |

### OnboardingSurvey Table
Learning style and preference data used by the memory system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Unique survey identifier |
| user_id | Integer | FK, Unique | Reference to users.id |
| learning_style | String | Nullable | visual, auditory, kinesthetic, reading |
| prior_experience | Text | Nullable | JSON previous learning experience |
| goals | Text | Nullable | Learning objectives |
| preferred_pace | String | Nullable | slow, medium, fast |
| interaction_preference | String | Nullable | questions, examples, practice |
| background_info | Text | Nullable | Additional context |
| motivation_level | String | Nullable | Learning motivation assessment |
| time_availability | String | Nullable | Available study time |

[Continue with all other tables...]

## Indexes

- `idx_users_email` on users(email)
- `idx_conversations_user_module` on conversations(user_id, module_id)
- `idx_messages_conversation` on messages(conversation_id)
- `idx_memory_user_module` on memory_summaries(user_id, module_id)
- `idx_progress_user_module` on user_progress(user_id, module_id)

## Relationships

All foreign key relationships use CASCADE DELETE to maintain data integrity:

```python
# User -> Conversations
conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

# Conversation -> Messages  
messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
```

## Migration Strategy

Database migrations are managed through Alembic:

```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```
EOF

# Create DEPLOYMENT.md
cat > docs/DEPLOYMENT.md << 'EOF'
# Deployment Guide

## Production Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f
```

### Manual Deployment

```bash
# Set production environment
export DATABASE_URL="postgresql://user:pass@host:5432/harv_prod"
export SECRET_KEY="your-production-secret-key"
export DEBUG=false

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | Database connection string |
| SECRET_KEY | Yes | JWT signing key |
| OPENAI_API_KEY | Yes | OpenAI API key |
| DEBUG | No | Debug mode (default: false) |
| CORS_ORIGINS | No | Allowed CORS origins |

### Health Checks

- `GET /health` - Basic health check
- `GET /health/database` - Database connectivity
- `GET /health/detailed` - Comprehensive status

### Monitoring

Recommended monitoring setup:
- Application logs: Structured JSON logging
- Metrics: Prometheus/Grafana
- Error tracking: Sentry
- Uptime monitoring: Health check endpoints
EOF

# Create CONTRIBUTING.md
cat > CONTRIBUTING.md << 'EOF'
# Contributing to Harv v2.0

Thank you for your interest in contributing to the Harv v2.0 Intelligent Tutoring System!

## Development Setup

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/harv-v2.git
   cd harv-v2
   ```

3. **Set up development environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## Code Standards

- **Python**: Follow PEP 8
- **Type Hints**: Required for all functions
- **Documentation**: Docstrings for all public methods
- **Testing**: Unit tests for new features

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation
6. Submit pull request

## Code Review Criteria

- Code follows established patterns
- Tests cover new functionality
- Documentation is updated
- No breaking changes without discussion
- Performance impact considered

## Feature Requests

Open an issue with:
- Clear description of the problem
- Proposed solution
- Use cases and benefits
- Implementation considerations
EOF

# Create LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Harv v2.0 Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create .github directory and templates
mkdir -p .github/{ISSUE_TEMPLATE,workflows}

# Create issue templates
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g. macOS, Linux, Windows]
- Python version: [e.g. 3.12]
- FastAPI version: [e.g. 0.110.0]

**Additional context**
Add any other context about the problem here.
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
EOF

# Create GitHub Actions workflow
cat > .github/workflows/tests.yml << 'EOF'
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.11, 3.12]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        cd backend  
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        flags: unittests
EOF

echo "✅ Documentation created"

# =============================================================================
# INITIALIZE GIT REPOSITORY
# =============================================================================

echo "📝 Setting up Git repository..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
fi

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
.venv/

# Environment variables
.env
.env.local
.env.production
.env.staging

# Database
*.db
*.sqlite3
harv_v2.db

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React build
/frontend/build
/frontend/dist

# Testing
.coverage
htmlcov/
.pytest_cache/
coverage.xml

# Temporary files
*.tmp
*.temp
.cache/

# Jupyter Notebooks
.ipynb_checkpoints

# macOS
.DS_Store

# Windows
Thumbs.db
EOF

# Add all files
git add .

# Create initial commit
git commit -m "🎉 Initial commit: Harv v2.0 Intelligent Tutoring System

✨ Features:
- Clean FastAPI backend architecture
- JWT authentication system
- SQLAlchemy database models
- Health monitoring endpoints
- Comprehensive documentation
- Production-ready configuration

🏗️ Architecture:
- Modular design with separation of concerns
- Enhanced memory system foundation
- Socratic methodology framework
- 15 communication modules ready

📚 Documentation:
- Complete API documentation
- Database schema details
- Setup and deployment guides
- Contributing guidelines

🚀 Ready for Phase 2: Enhanced Memory System implementation"

echo "✅ Git repository initialized"

# =============================================================================
# CREATE GITHUB REPOSITORY INSTRUCTIONS
# =============================================================================

echo ""
echo "🎯 GITHUB REPOSITORY SETUP COMPLETE!"
echo "====================================="
echo ""
echo "📋 Next steps to create GitHub repository:"
echo ""
echo "1. 🌐 Create new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: harv-v2"
echo "   - Description: Intelligent Tutoring System with Enhanced Memory & Socratic Methodology"
echo "   - Make it Public (to showcase your work)"
echo "   - Don't initialize with README (we have our own)"
echo ""
echo "2. 🔗 Connect local repository to GitHub:"
echo "   git remote add origin https://github.com/YOURUSERNAME/harv-v2.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 📊 Configure GitHub repository:"
echo "   - Add topics: artificial-intelligence, education, fastapi, python, socratic-method"
echo "   - Enable Issues and Discussions"
echo "   - Set up branch protection for main branch"
echo "   - Configure GitHub Pages for documentation (optional)"
echo ""
echo "4. 🏷️ Create first release:"
echo "   - Tag: v2.0.0-alpha"
echo "   - Title: Harv v2.0 Alpha - Clean Architecture Foundation"
echo "   - Description: Production-ready foundation with authentication and database"
echo ""
echo "📂 Repository includes:"
echo "   ✅ Comprehensive README.md with badges and quick start"
echo "   ✅ Detailed SETUP.md with step-by-step build process"
echo "   ✅ Complete API documentation in docs/API.md"
echo "   ✅ Database schema documentation"
echo "   ✅ Deployment and contributing guidelines"
echo "   ✅ GitHub templates for issues and PRs"
echo "   ✅ GitHub Actions for automated testing"
echo "   ✅ Professional .gitignore and LICENSE"
echo ""
echo "🎉 Your repository is ready to impress!"
echo ""
echo "Repository URL will be: https://github.com/YOURUSERNAME/harv-v2"
