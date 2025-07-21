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
