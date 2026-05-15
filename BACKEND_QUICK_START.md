# Backend Modernization - Quick Start Guide

## What Changed?

Your FERTILE MAP backend has been completely modernized with professional-grade infrastructure:

### ✅ 9 Files Created/Modified
- `requirements.txt` - Added Flask-SQLAlchemy, marshmallow, python-dotenv, email-validator
- `.env.example` - Configuration template
- `config.py` - Modern environment-based configuration
- `models.py` - SQLAlchemy ORM models (User, SoilAnalysis, DatabaseInfo)
- `validation.py` - Marshmallow validation schemas
- `logging_config.py` - Structured logging system
- `error_handlers.py` - Centralized error handling
- `API_DOCUMENTATION.md` - Complete API reference
- `app.py` - Refactored with ORM and error handling

### ✅ Key Features Added

| Feature | Before | After |
|---------|--------|-------|
| **Database Access** | Raw sqlite3 | SQLAlchemy ORM |
| **Error Handling** | Ad-hoc try/except | Centralized APIError system |
| **Logging** | None | Structured with file rotation |
| **Input Validation** | Manual checks | Marshmallow schemas |
| **Configuration** | Hardcoded values | Environment variables |
| **API Documentation** | None | Complete with examples |
| **Security** | Basic | Enhanced with validation |

---

## Setup Instructions

### Step 1: Install New Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### Step 2: Create .env File
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
SQLALCHEMY_DATABASE_URI=sqlite:///database/soil_app.db
```

### Step 3: Run the Application
```bash
python app.py
```

The app will:
1. Initialize SQLAlchemy ORM (creates tables automatically)
2. Setup structured logging (creates `logs/` directory)
3. Register error handlers
4. Start Flask server on http://localhost:5000

---

## Using the New Features

### 1. ORM Models (Instead of Raw SQL)

**Old Way** (Raw SQL):
```python
db = get_db()
user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
db.close()
```

**New Way** (ORM):
```python
user = User.query.filter_by(email=email).first()
user_dict = user.to_dict()  # Easy conversion to dict
```

### 2. Input Validation

**Old Way** (Manual):
```python
if not data.get('email'):
    return jsonify({"error": "Email required"}), 400
```

**New Way** (Marshmallow):
```python
validated_data = validate_request_data(data, user_schema)
# Automatically validates email format, password strength, etc.
```

### 3. Error Handling

**Old Way** (Inconsistent):
```python
if not user:
    return jsonify({"error": "User not found"}), 404
```

**New Way** (Standardized):
```python
if not user:
    raise APIError('User not found', 404)
# Returns: {"success": false, "error": "User not found", "status_code": 404}
```

### 4. Logging

**New Way** (Automatic):
```python
logger.info(f"User {user.email} logged in")
# Logs to: Backend/logs/app.log with timestamp and source location
```

---

## API Endpoints Reference

### Authentication
- **POST** `/api/auth/register` - Register new user
- **POST** `/api/auth/login` - User login
- **GET** `/api/auth/profile` - Get user profile
- **PUT** `/api/auth/profile` - Update profile
- **POST** `/api/auth/change-password` - Change password

### Analysis
- **POST** `/api/analyze` - Submit soil for analysis
- **GET** `/api/history?page=1&limit=10` - Get analysis history
- **DELETE** `/api/history/<id>` - Delete analysis

### Admin
- **GET** `/api/admin/users?page=1&limit=20` - Get all users
- **PUT** `/api/admin/users/<id>/role` - Update user role
- **DELETE** `/api/admin/users/<id>` - Delete user
- **GET** `/api/admin/stats` - Admin dashboard stats
- **GET** `/api/admin/database/info` - Database info
- **GET** `/api/admin/database/tables` - List tables
- **GET** `/api/admin/database/table/<name>?page=1` - Table data

---

## Response Format Examples

### Success Response (200)
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### Error Response (400)
```json
{
  "success": false,
  "error": "Validation failed",
  "status_code": 400,
  "validation_errors": {
    "email": ["Not a valid email address"]
  }
}
```

---

## Database Models

### User Model
```python
User(
    id=1,
    full_name="John Farmer",
    email="john@example.com",
    password="hashed_password",
    farm_name="Green Valley",
    role="user",  # or "admin"
    is_active=True,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
```

### SoilAnalysis Model
```python
SoilAnalysis(
    id=1,
    user_id=1,  # Links to User
    image_url="filename.jpg",
    soil_type="loamy",  # loamy/sandy/clay/silty/peaty/chalky
    confidence=0.92,
    properties={...},
    predictions={...},
    recommendations={...},
    selected_crop="wheat",
    status="analyzed"  # analyzed/pending
)
```

---

## Logging

Logs are stored in `Backend/logs/app.log` with:
- **Automatic rotation** at 10MB per file
- **Keeps 10 backup files** for history
- **Both console and file output**
- **Timestamp, logger, level, source location, message**

Example log entries:
```
2024-01-15 10:30:45,123 - fertile_map - INFO - [app.py:150] - New user registered: john@example.com
2024-01-15 10:31:12,456 - fertile_map - WARNING - [app.py:175] - Login failed for email: invalid@example.com
2024-01-15 10:32:00,789 - fertile_map - ERROR - [app.py:280] - Analysis failed: Model not found
```

---

## Environment Variables

Key variables in `.env`:

```env
# Flask Configuration
FLASK_ENV=development          # development|production|testing
SECRET_KEY=your-secret-key     # Change this in production!
DEBUG=True                     # Set to False in production

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///database/soil_app.db

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret # Change this in production!
JWT_EXPIRATION_HOURS=24

# Logging
LOG_LEVEL=INFO                 # DEBUG|INFO|WARNING|ERROR|CRITICAL
LOG_FILE=logs/app.log

# File Upload
UPLOAD_FOLDER=uploads/
MAX_CONTENT_LENGTH=16777216    # 16MB max file size

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

---

## Testing Endpoints

### Test Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "farm_name": "Test Farm"
  }'
```

### Test Login (Get Token)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Protected Endpoint
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Troubleshooting

### Problem: "Module not found" errors
**Solution**: Run `pip install -r requirements.txt`

### Problem: Database locked
**Solution**: 
1. Close all connections
2. Delete `Backend/database/soil_app.db`
3. Restart the app (creates fresh database)

### Problem: Logs not appearing
**Solution**: Check that `Backend/logs/` directory exists and is writable

### Problem: CORS errors in frontend
**Solution**: Update `CORS_ORIGINS` in `.env` to include your frontend URL

### Problem: Token expiration errors
**Solution**: Frontend needs to handle 401 errors and request new login

---

## Validation Rules

### User Registration
- **full_name**: Required, 2-255 characters
- **email**: Required, valid email format, must be unique
- **password**: Required, minimum 6 characters
- **farm_name**: Optional, any length
- **role**: Optional, must be 'user' or 'admin' (default: 'user')

### User Login
- **email**: Required, must be valid email format
- **password**: Required, minimum 6 characters

### Soil Analysis
- **soil_type**: Must be one of: loamy, sandy, clay, silty, peaty, chalky
- **confidence**: Must be between 0-100
- **crop_type**: Optional, any string

### Profile Update
- **full_name**: Optional, 2-255 characters if provided
- **farm_name**: Optional, any length

---

## Admin Operations

### Get All Users
```bash
curl -X GET "http://localhost:5000/api/admin/users?page=1&limit=20" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### Change User Role
```bash
curl -X PUT http://localhost:5000/api/admin/users/2/role \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}'
```

### Delete User
```bash
curl -X DELETE http://localhost:5000/api/admin/users/2 \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### Get Database Stats
```bash
curl -X GET http://localhost:5000/api/admin/stats \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## Production Deployment

Before deploying to production:

1. **Update .env file**:
   - Change `FLASK_ENV=production`
   - Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
   - Use PostgreSQL instead of SQLite
   - Update `CORS_ORIGINS`

2. **Security checks**:
   - Set `DEBUG=False`
   - Enable HTTPS
   - Use environment variables for all secrets
   - Implement rate limiting
   - Setup Web Application Firewall

3. **Monitoring**:
   - Setup log aggregation
   - Configure alerting
   - Monitor database performance
   - Track API response times

4. **Backup**:
   - Daily database backups
   - Backup configuration files
   - Test restore procedures

---

## Next Steps

1. ✅ Run `pip install -r requirements.txt`
2. ✅ Create `.env` file with your settings
3. ✅ Start the application: `python app.py`
4. ✅ Test endpoints using provided curl examples
5. ✅ Monitor logs in `Backend/logs/app.log`
6. ✅ Deploy to staging for user testing
7. ✅ Deploy to production

---

## Documentation Files

- **API_DOCUMENTATION.md** - Complete API reference with all endpoints
- **BACKEND_MODERNIZATION_COMPLETE.md** - Detailed technical documentation
- **Backend/API_DOCUMENTATION.md** - Markdown API reference

---

## Support

For issues or questions:
1. Check the logs in `Backend/logs/app.log`
2. Review the API documentation
3. Verify .env configuration
4. Ensure all dependencies are installed

---

**Version**: 1.0.0  
**Last Updated**: January 15, 2024
