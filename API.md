# Harv v2.0 API Documentation

## Overview

The Harv v2.0 API is built with FastAPI, providing automatic interactive documentation, request/response validation, and OpenAPI schema generation.

**Base URL**: `http://localhost:8000`  
**API Version**: `v1`  
**Documentation**: `http://localhost:8000/docs`  
**Schema**: `http://localhost:8000/openapi.json`

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Tokens expire after 30 minutes (configurable) and must be refreshed by re-authenticating.

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "data": {},
  "message": "Success message",
  "success": true
}
```

### Error Response
```json
{
  "detail": "Error description",
  "error": "Error type",
  "status_code": 400
}
```

## Endpoints

## Health Monitoring

### GET /health

Basic health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "Harv v2.0 - Intelligent Tutoring System",
  "version": "2.0.0",
  "debug": false
}
```

**Status Codes**:
- `200`: System healthy
- `503`: System unhealthy

---

### GET /health/database

Database connectivity check.

**Response**:
```json
{
  "database": "healthy",
  "connection": "active",
  "query_result": 1
}
```

**Status Codes**:
- `200`: Database healthy
- `503`: Database connection failed

---

### GET /health/detailed

Comprehensive system health check.

**Response**:
```json
{
  "service": "Harv v2.0 - Intelligent Tutoring System",
  "version": "2.0.0",
  "status": "healthy",
  "checks": {
    "database": "healthy",
    "openai_key": "configured",
    "memory_system": "not_implemented_yet"
  }
}
```

## Authentication

### POST /api/v1/register

Register a new user account.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Status Codes**:
- `200`: Registration successful
- `400`: Email already exists or validation error
- `422`: Invalid request data

**Validation Rules**:
- Email must be valid format
- Password minimum 8 characters
- Name is required

---

### POST /api/v1/login

Authenticate user and receive access token.

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Status Codes**:
- `200`: Login successful
- `401`: Invalid credentials
- `400`: Inactive user account
- `422`: Invalid request data

---

### GET /api/v1/me

Get current authenticated user information.

**Headers**:
```
Authorization: Bearer <your-jwt-token>
```

**Response**:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true
}
```

**Status Codes**:
- `200`: User information retrieved
- `401`: Invalid or expired token
- `404`: User not found

## Memory System (Phase 2)

*Coming in Phase 2 - Enhanced Memory System Implementation*

### GET /api/v1/memory/enhanced/{module_id}

Retrieve enhanced memory context for a specific module.

**Parameters**:
- `module_id` (integer): ID of the learning module

**Headers**:
```
Authorization: Bearer <your-jwt-token>
```

**Response**:
```json
{
  "assembled_prompt": "Complete context for AI with 4-layer memory...",
  "context_metrics": {
    "total_chars": 1543,
    "layer_breakdown": {
      "system_data": 234,
      "module_data": 456,
      "conversation_data": 567,
      "prior_knowledge": 286
    }
  },
  "memory_layers": {
    "system_data": {
      "learning_style": "visual",
      "preferred_pace": "medium",
      "goals": ["improve communication skills"]
    },
    "module_data": {
      "title": "Communication Theory",
      "objectives": "Understand fundamental concepts...",
      "progress": 0.3
    },
    "conversation_data": {
      "recent_messages": [],
      "current_topic": "introduction"
    },
    "prior_knowledge": {
      "related_modules": [],
      "connections": []
    }
  },
  "database_status": {
    "user_found": true,
    "module_found": true,
    "memories_loaded": 0
  }
}
```

## Chat System (Phase 2)

### POST /api/v1/chat/enhanced

Send message with enhanced memory integration.

**Request Body**:
```json
{
  "module_id": 1,
  "message": "What is mass communication?",
  "conversation_id": "optional-uuid"
}
```

**Headers**:
```
Authorization: Bearer <your-jwt-token>
```

**Response**:
```json
{
  "reply": "That's an interesting question! What makes you think about mass communication specifically? Can you think of examples from your daily life where you encounter mass communication?",
  "conversation_id": "uuid-string",
  "module_id": 1,
  "memory_metrics": {
    "context_used": 1543,
    "layers_active": 4,
    "connections_found": 2
  },
  "socratic_analysis": {
    "question_type": "exploratory",
    "engagement_level": "high",
    "learning_objective": "conceptual_understanding"
  },
  "enhanced": true
}
```

## Learning Modules (Phase 2)

### GET /api/v1/modules

Retrieve all available learning modules.

**Headers**:
```
Authorization: Bearer <your-jwt-token>
```

**Response**:
```json
[
  {
    "id": 1,
    "title": "Your Four Worlds",
    "description": "Communication models, perception, and the four worlds we live in",
    "difficulty_level": "beginner",
    "estimated_duration": 45,
    "is_active": true,
    "user_progress": {
      "completion_percentage": 0.0,
      "mastery_level": "beginner",
      "last_accessed": null
    }
  },
  {
    "id": 2,
    "title": "Writing: The Persistence of Words",
    "description": "How writing changed human communication and knowledge preservation",
    "difficulty_level": "intermediate",
    "estimated_duration": 60,
    "is_active": true,
    "user_progress": {
      "completion_percentage": 0.3,
      "mastery_level": "beginner", 
      "last_accessed": "2024-01-15T10:30:00Z"
    }
  }
]
```

### GET /api/v1/modules/{module_id}

Get detailed information about a specific module.

**Parameters**:
- `module_id` (integer): ID of the learning module

**Headers**:
```
Authorization: Bearer <your-jwt-token>
```

**Response**:
```json
{
  "id": 1,
  "title": "Your Four Worlds",
  "description": "Communication models, perception, and the four worlds we live in",
  "learning_objectives": "Students will discover how perception shapes communication...",
  "resources": "Additional reading materials and examples",
  "difficulty_level": "beginner",
  "estimated_duration": 45,
  "prerequisites": [],
  "user_progress": {
    "completion_percentage": 0.0,
    "mastery_level": "beginner",
    "total_conversations": 0,
    "total_messages": 0,
    "time_spent": 0,
    "insights_gained": 0,
    "connections_made": 0
  }
}
```

## User Progress (Phase 2)

### GET /api/v1/progress

Get user's progress across all modules.

**Headers**:
```
Authorization: Bearer <your-jwt-token>
```

**Response**:
```json
[
  {
    "module_id": 1,
    "module_title": "Your Four Worlds",
    "completion_percentage": 75.0,
    "mastery_level": "intermediate",
    "total_conversations": 3,
    "total_messages": 47,
    "time_spent": 120,
    "last_accessed": "2024-01-15T10:30:00Z",
    "is_completed": false
  }
]
```

### GET /api/v1/progress/{module_id}

Get detailed progress for a specific module.

**Parameters**:
- `module_id` (integer): ID of the learning module

**Headers**:
```
Authorization: Bearer <your-jwt-token>
```

**Response**:
```json
{
  "module_id": 1,
  "module_title": "Your Four Worlds",
  "completion_percentage": 75.0,
  "mastery_level": "intermediate",
  "total_conversations": 3,
  "total_messages": 47,
  "time_spent": 120,
  "questions_asked": 23,
  "insights_gained": 8,
  "connections_made": 5,
  "current_focus": "Exploring perception differences in communication",
  "learning_path": [
    {
      "concept": "Communication Models",
      "status": "mastered",
      "insights": ["Understanding sender-receiver model"]
    },
    {
      "concept": "Perceptual Worlds", 
      "status": "learning",
      "insights": ["Different perspectives create different realities"]
    }
  ],
  "is_completed": false
}
```

## Error Handling

### Common Error Responses

**400 Bad Request**:
```json
{
  "detail": "Email already registered",
  "error": "validation_error",
  "status_code": 400
}
```

**401 Unauthorized**:
```json
{
  "detail": "Could not validate credentials",
  "error": "authentication_error",
  "status_code": 401
}
```

**404 Not Found**:
```json
{
  "detail": "User not found",
  "error": "not_found_error",
  "status_code": 404
}
```

**422 Validation Error**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ],
  "error": "validation_error",
  "status_code": 422
}
```

**500 Internal Server Error**:
```json
{
  "detail": "An unexpected error occurred",
  "error": "internal_server_error",
  "status_code": 500
}
```

## Rate Limiting

*To be implemented in production*

- **Authentication endpoints**: 5 requests per minute per IP
- **Chat endpoints**: 60 requests per minute per user
- **General API**: 100 requests per minute per user

Rate limit headers included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Development & Testing

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation where you can:
- Explore all endpoints
- Test API calls directly
- View request/response schemas
- Understand authentication requirements

### Example Integration

```python
import httpx

class HarvClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
    
    async def login(self, email: str, password: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/login",
                json={"email": email, "password": password}
            )
            data = response.json()
            self.token = data["access_token"]
            return data
    
    async def get_modules(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/modules",
                headers=headers
            )
            return response.json()

# Usage
client = HarvClient()
await client.login("user@example.com", "password")
modules = await client.get_modules()
```

## Versioning

The API uses URL versioning (`/api/v1/`). Breaking changes will result in a new version (`/api/v2/`).

**Current Version**: `v1`  
**Deprecation Policy**: Previous versions supported for 6 months after new version release

---

*This API documentation is automatically generated and kept in sync with the actual implementation through FastAPI's OpenAPI integration.*
