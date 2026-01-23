# API Documentation

This document provides comprehensive documentation for the EchoStor Security Posture Assessment Tool API endpoints.

## 📋 Table of Contents

- [Base URL and Authentication](#base-url-and-authentication)
- [Authentication Endpoints](#authentication-endpoints)
- [Assessment Endpoints](#assessment-endpoints)
- [Report Endpoints](#report-endpoints)
- [Admin Endpoints](#admin-endpoints)
- [Health Check Endpoints](#health-check-endpoints)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## 🔗 Base URL and Authentication

### Base URLs
- **Production**: `https://echostor-security-posture-tool.fly.dev`
- **Local Development**: `http://localhost:8000`

### Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Interactive API Documentation
The API provides auto-generated interactive documentation:
- **Swagger UI**: `/docs` - Interactive API explorer
- **ReDoc**: `/redoc` - Clean documentation interface

## 🔐 Authentication Endpoints

### POST /api/auth/register
Register a new user account.

**Rate Limit**: 5 requests per minute

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "company_name": "Example Corp"
}
```

**Response (201):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "company_name": "Example Corp",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Errors:**
- `400 Bad Request`: Email already registered
- `422 Unprocessable Entity`: Invalid request data

---

### POST /api/auth/login
Authenticate user and get access token.

**Rate Limit**: 10 requests per minute

**Request Body:**
```json
{
  "email": "user@example.com", 
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "company_name": "Example Corp"
  }
}
```

**Errors:**
- `401 Unauthorized`: Invalid credentials
- `422 Unprocessable Entity`: Invalid request data

---

### GET /api/auth/me
Get current authenticated user information.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe", 
  "company_name": "Example Corp",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

## 📊 Assessment Endpoints

### GET /api/assessment/structure
Get the complete assessment structure with all sections and questions.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "sections": [
    {
      "id": "governance",
      "title": "Governance and Risk Management",
      "description": "Questions about organizational security governance",
      "questions": [
        {
          "id": "gov_001",
          "text": "Does your organization have a formal information security policy?",
          "type": "single_choice",
          "options": [
            {"value": "yes", "label": "Yes, comprehensive policy"},
            {"value": "partial", "label": "Partial policy exists"},
            {"value": "no", "label": "No formal policy"}
          ],
          "required": true
        }
      ]
    }
  ]
}
```

---

### POST /api/assessment/start
Start a new assessment for the current user.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (201):**
```json
{
  "id": "assessment-uuid",
  "user_id": "user-uuid",
  "status": "in_progress",
  "started_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-30T10:30:00Z",
  "progress_percentage": 0.0
}
```

**Errors:**
- `400 Bad Request`: User already has an active assessment

---

### GET /api/assessment/current
Get the current user's active assessment.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": "assessment-uuid",
  "status": "in_progress",
  "started_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-30T10:30:00Z",
  "last_saved_at": "2024-01-15T14:30:00Z",
  "progress_percentage": 25.5,
  "consultation_interest": false
}
```

**Errors:**
- `404 Not Found`: No active assessment found

---

### GET /api/assessment/responses
Get all responses for the current assessment.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "responses": [
    {
      "section_id": "governance",
      "question_id": "gov_001", 
      "answer_value": "yes",
      "comment": "We have a comprehensive security policy updated annually",
      "created_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

---

### POST /api/assessment/responses
Save or update assessment responses.

**Headers:**
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "responses": [
    {
      "section_id": "governance",
      "question_id": "gov_001",
      "answer_value": "yes",
      "comment": "Optional comment about the answer"
    }
  ]
}
```

**Response (200):**
```json
{
  "message": "Responses saved successfully",
  "saved_count": 1,
  "assessment": {
    "id": "assessment-uuid",
    "progress_percentage": 26.8,
    "last_saved_at": "2024-01-15T14:35:00Z"
  }
}
```

---

### POST /api/assessment/save-progress
Manual save of current progress (also auto-saves every 10 minutes).

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "message": "Progress saved successfully",
  "last_saved_at": "2024-01-15T14:35:00Z",
  "progress_percentage": 26.8
}
```

---

### POST /api/assessment/complete
Mark assessment as completed.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "message": "Assessment completed successfully",
  "assessment": {
    "id": "assessment-uuid",
    "status": "completed",
    "completed_at": "2024-01-15T16:00:00Z",
    "progress_percentage": 100.0
  }
}
```

**Errors:**
- `400 Bad Request`: Assessment not ready for completion
- `404 Not Found`: No active assessment found

---

### POST /api/assessment/consultation
Save consultation interest and details.

**Headers:**
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "interested": true,
  "details": "We're interested in cybersecurity consulting for our cloud infrastructure"
}
```

**Response (200):**
```json
{
  "message": "Consultation interest saved successfully"
}
```

## 📄 Report Endpoints

### POST /api/reports/{assessment_id}/generate
Generate a standard PDF report for a completed assessment.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": "report-uuid",
  "assessment_id": "assessment-uuid", 
  "report_type": "standard",
  "status": "generating",
  "requested_at": "2024-01-15T16:05:00Z"
}
```

**Errors:**
- `404 Not Found`: Assessment not found or not completed

---

### POST /api/reports/{assessment_id}/request-ai-report
Request an AI-enhanced report (requires admin approval).

**Headers:**
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "additional_context": "Please focus on cloud security recommendations"
}
```

**Response (200):**
```json
{
  "message": "AI report requested successfully",
  "status": "pending",
  "estimated_delivery": "3-5 business days"
}
```

---

### GET /api/reports/{report_id}/status
Get the status of a specific report.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": "report-uuid",
  "report_type": "standard",
  "status": "completed",
  "requested_at": "2024-01-15T16:05:00Z",
  "completed_at": "2024-01-15T16:10:00Z"
}
```

---

### GET /api/reports/{report_id}/download
Download a completed report PDF.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response (200):**
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="security_assessment_report_standard_{report_id}.pdf"`

**Errors:**
- `403 Forbidden`: Not authorized to download this report
- `404 Not Found`: Report not found or not ready

---

### GET /api/reports/user/reports
Get all reports for the current user.

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `skip` (int, default=0): Number of items to skip for pagination
- `limit` (int, default=100): Maximum items to return

**Response (200):**
```json
{
  "items": [
    {
      "id": "report-uuid",
      "report_type": "standard",
      "status": "completed", 
      "requested_at": "2024-01-15T16:05:00Z",
      "completed_at": "2024-01-15T16:10:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

## 👨‍💼 Admin Endpoints

All admin endpoints require admin authentication.

### GET /api/admin/users
Get all users with pagination and search.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Query Parameters:**
- `skip` (int, default=0): Items to skip
- `limit` (int, default=100): Maximum items to return  
- `search` (str, optional): Search by email, name, or company

**Response (200):**
```json
{
  "items": [
    {
      "id": "user-uuid",
      "email": "user@example.com",
      "full_name": "John Doe",
      "company_name": "Example Corp",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 150,
  "skip": 0,
  "limit": 100
}
```

---

### GET /api/admin/users/{user_id}
Get specific user details.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
{
  "id": "user-uuid",
  "email": "user@example.com", 
  "full_name": "John Doe",
  "company_name": "Example Corp",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/admin/users/{user_id}/assessments
Get all assessments for a specific user.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
[
  {
    "id": "assessment-uuid",
    "status": "completed",
    "started_at": "2024-01-15T10:30:00Z",
    "completed_at": "2024-01-15T16:00:00Z",
    "progress_percentage": 100.0,
    "consultation_interest": true
  }
]
```

---

### GET /api/admin/assessments
Get all assessments with filtering.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Query Parameters:**
- `skip` (int, default=0): Items to skip
- `limit` (int, default=100): Maximum items 
- `status` (str, optional): Filter by status (in_progress, completed, expired)

**Response (200):**
```json
{
  "items": [
    {
      "id": "assessment-uuid",
      "user": {
        "email": "user@example.com",
        "full_name": "John Doe",
        "company_name": "Example Corp"
      },
      "status": "completed",
      "started_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T16:00:00Z",
      "progress_percentage": 100.0
    }
  ],
  "total": 50,
  "skip": 0,
  "limit": 100
}
```

---

### GET /api/admin/dashboard/stats
Get dashboard statistics.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
{
  "total_users": 150,
  "active_assessments": 25,
  "completed_assessments": 100,
  "expired_assessments": 15,
  "new_users_this_week": 8,
  "stuck_assessments": 3,
  "average_completion_hours": 4.5
}
```

---

### GET /api/admin/users-progress-summary
Get detailed progress summary for all users.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
[
  {
    "user_id": "user-uuid",
    "full_name": "John Doe",
    "email": "user@example.com", 
    "company_name": "Example Corp",
    "assessment_status": "completed",
    "progress_percentage": 100.0,
    "started_at": "2024-01-15T10:30:00Z",
    "last_activity": "2024-01-15T16:00:00Z"
  }
]
```

---

### POST /api/admin/reports/{report_id}/generate-ai
Admin endpoint to generate AI-enhanced reports.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
{
  "id": "report-uuid",
  "status": "generating",
  "message": "AI report generation started"
}
```

---

### POST /api/admin/reports/{report_id}/release
Release AI-enhanced report to user.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
{
  "message": "AI report released to user",
  "report_id": "report-uuid"
}
```

---

### GET /api/admin/consultation-requests
Get all consultation requests.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
[
  {
    "user": {
      "email": "user@example.com",
      "full_name": "John Doe", 
      "company_name": "Example Corp"
    },
    "assessment_id": "assessment-uuid",
    "consultation_details": "Need help with cloud security",
    "requested_at": "2024-01-15T16:00:00Z"
  }
]
```

---

### DELETE /api/admin/users/{user_id}
Delete a user account.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
{
  "message": "User deleted successfully"
}
```

---

### POST /api/admin/users/{user_id}/reset-password
Reset user password.

**Headers:**
```http
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "new_password": "newsecurepassword123"
}
```

**Response (200):**
```json
{
  "message": "Password reset successfully"
}
```

## 🏥 Health Check Endpoints

### GET /health
Comprehensive health check with service status.

**Response (200):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 3600.25,
  "timestamp": "2024-01-15T16:00:00Z",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    },
    "redis": {
      "status": "healthy", 
      "message": "Redis connection successful"
    }
  }
}
```

**Response (503) - Unhealthy:**
```json
{
  "status": "unhealthy",
  "version": "1.0.0",
  "uptime_seconds": 3600.25,
  "timestamp": "2024-01-15T16:00:00Z",
  "checks": {
    "database": {
      "status": "unhealthy",
      "message": "Database connection failed: Connection timeout"
    }
  }
}
```

---

### GET /health/live
Liveness probe (always returns 200 if application is running).

**Response (200):**
```json
{
  "status": "alive",
  "version": "1.0.0", 
  "uptime_seconds": 3600.25,
  "timestamp": "2024-01-15T16:00:00Z"
}
```

---

### GET /health/ready
Readiness probe (returns 200 only if database is accessible).

**Response (200):**
```json
{
  "status": "ready",
  "version": "1.0.0",
  "uptime_seconds": 3600.25, 
  "timestamp": "2024-01-15T16:00:00Z",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    }
  }
}
```

**Response (503):**
```json
{
  "status": "not_ready",
  "version": "1.0.0",
  "uptime_seconds": 3600.25,
  "timestamp": "2024-01-15T16:00:00Z",
  "checks": {
    "database": {
      "status": "unhealthy",
      "message": "Database connection failed"
    }
  }
}
```

## ⚠️ Error Handling

### Standard Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- **200 OK**: Successful request
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data or business logic error
- **401 Unauthorized**: Invalid or missing authentication
- **403 Forbidden**: Valid authentication but insufficient permissions
- **404 Not Found**: Requested resource not found
- **422 Unprocessable Entity**: Invalid request body schema
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Unexpected server error
- **503 Service Unavailable**: Service temporarily unavailable

### Common Error Scenarios

#### Authentication Errors
```json
// 401 Unauthorized - Invalid token
{
  "detail": "Could not validate credentials"
}

// 401 Unauthorized - Token expired  
{
  "detail": "Token has expired"
}
```

#### Validation Errors
```json
// 422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Rate Limit Errors
```json
// 429 Too Many Requests
{
  "detail": "Rate limit exceeded. Try again later."
}
```

## 🚦 Rate Limiting

The API implements rate limiting on sensitive endpoints:

- **Registration**: 5 requests per minute per IP
- **Login**: 10 requests per minute per IP
- **Admin endpoints**: 100 requests per minute per authenticated admin

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 8
X-RateLimit-Reset: 1642262400
```

## 📚 Additional Resources

- **Interactive API Docs**: Available at `/docs` when running the backend
- **OpenAPI Specification**: Available at `/openapi.json`
- **Architecture Documentation**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- **Troubleshooting Guide**: [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Last Updated**: January 2024  
**API Version**: 1.0.0
