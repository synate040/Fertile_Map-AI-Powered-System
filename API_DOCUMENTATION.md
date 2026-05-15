# FERTILE MAP API Documentation

## Overview
FERTILE MAP is an AI-powered soil analysis system that provides real-time soil type identification and fertilizer recommendations using machine learning.

**API Version**: 1.0.0  
**Base URL**: `http://localhost:5000/api`  
**Authentication**: JWT Bearer Token

---

## Table of Contents
1. [Authentication](#authentication)
2. [Users](#users)
3. [Soil Analysis](#soil-analysis)
4. [Database Manager](#database-manager)
5. [Error Handling](#error-handling)
6. [Response Format](#response-format)

---

## Authentication

### Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "full_name": "John Farmer",
  "email": "john@example.com",
  "password": "securepassword123",
  "farm_name": "Green Valley Farm"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "full_name": "John Farmer",
    "email": "john@example.com",
    "farm_name": "Green Valley Farm"
  }
}
```

**Validation Errors (400):**
```json
{
  "success": false,
  "error": "Validation failed",
  "validation_errors": {
    "email": ["Not a valid email address"],
    "password": ["Length must be >= 6"]
  }
}
```

---

### Login
**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "full_name": "John Farmer",
      "email": "john@example.com",
      "role": "user"
    }
  }
}
```

**Error (401):**
```json
{
  "success": false,
  "error": "Invalid email or password",
  "status_code": 401
}
```

---

## Users

### Get User Profile
**GET** `/users/profile`

Retrieve current user profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "full_name": "John Farmer",
    "email": "john@example.com",
    "farm_name": "Green Valley Farm",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

### Update User Profile
**PUT** `/users/profile`

Update user profile information.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "John Farmer Updated",
  "farm_name": "Green Valley Farm 2.0"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "full_name": "John Farmer Updated",
    "farm_name": "Green Valley Farm 2.0"
  }
}
```

---

### Change Password
**POST** `/users/change-password`

Change user password.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword456",
  "confirm_password": "newpassword456"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

## Soil Analysis

### Analyze Soil
**POST** `/analysis/analyze`

Submit soil image for analysis.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Form Data:**
- `image`: Image file (PNG, JPG, JPEG, WEBP)
- `crop_type`: (optional) Target crop type

**Response (200):**
```json
{
  "success": true,
  "message": "Analysis completed",
  "data": {
    "soil_type": "loamy",
    "confidence": 0.92,
    "confidence_percent": "92.00",
    "properties": {
      "texture": "Loamy",
      "color": "Dark Brown",
      "drainage": "Well-drained"
    },
    "recommendations": {
      "status": "Optimal",
      "general_fertilizers": [
        {
          "name": "NPK 10-10-10",
          "purpose": "Balanced nutrition",
          "application": "Top dressing",
          "frequency": "Monthly"
        }
      ],
      "organic_alternatives": ["Compost", "Aged manure"]
    }
  }
}
```

---

### Get Analysis History
**GET** `/analysis/history?page=1&limit=10`

Retrieve user's analysis history.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Results per page (default: 10)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "analyses": [
      {
        "id": 1,
        "soil_type": "loamy",
        "confidence": 0.92,
        "created_at": "2024-01-15T10:30:00",
        "status": "analyzed"
      }
    ],
    "total": 15,
    "page": 1,
    "pages": 2
  }
}
```

---

### Get Single Analysis
**GET** `/analysis/<id>`

Retrieve specific soil analysis.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "soil_type": "loamy",
    "confidence": 0.92,
    "properties": {...},
    "recommendations": {...},
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

## Database Manager

### Get Database Info
**GET** `/database/info`

Retrieve database statistics and metadata.

**Headers:**
```
Authorization: Bearer <token>
X-Require-Admin: true
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "database_name": "soil_app.db",
    "tables_count": 3,
    "total_users": 42,
    "total_analyses": 156,
    "last_backup": "2024-01-15T20:00:00"
  }
}
```

---

### Get Table Data
**GET** `/database/table/<table_name>?page=1&limit=20`

Retrieve table data with pagination.

**Headers:**
```
Authorization: Bearer <token>
X-Require-Admin: true
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "table": "users",
    "columns": ["id", "full_name", "email", "role"],
    "rows": [...],
    "total": 42,
    "page": 1,
    "pages": 3
  }
}
```

---

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Error message",
  "status_code": 400,
  "validation_errors": {} // Optional
}
```

### Common Status Codes
| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication failed |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 500 | Server Error - Internal error |

---

## Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "status_code": 200,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description",
  "status_code": 400
}
```

---

## Authentication

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer <your_token_here>
```

Token expires after 24 hours. Request a new token by logging in again.

---

## Rate Limiting

Currently no rate limiting is implemented. This should be added in production.

---

## CORS

CORS is enabled for all origins. Configure in `.env`:
```
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## Best Practices

1. **Always use HTTPS** in production
2. **Store token securely** in localStorage or sessionStorage
3. **Refresh token** before expiration
4. **Handle errors** properly in frontend
5. **Validate input** before sending requests
6. **Log important events** for debugging

---

## Support

For API issues or questions, please check the logs in `Backend/logs/app.log`

**Version**: 1.0.0  
**Last Updated**: 2024-01-15
