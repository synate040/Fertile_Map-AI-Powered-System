# Admin Panel Documentation

## Overview
The SoilSense admin panel provides administrators with a centralized interface to manage users and view system statistics.

## Features

### 1. **Dashboard Statistics**
- **Total Users**: Count of all registered users
- **Admin Users**: Count of users with admin role
- **Total Analyses**: Count of all soil analyses performed

### 2. **User Management**
- View all registered users
- Search users by email or name
- Update user roles (Admin ↔ User)
- Delete users and their associated data

### 3. **Admin Endpoints**

#### Get All Users
```
GET /api/admin/users
Authorization: Bearer <admin_token>
Response: { users: [...], total: number }
```

#### Get Admin Statistics
```
GET /api/admin/stats
Authorization: Bearer <admin_token>
Response: { total_users, admin_count, total_analyses }
```

#### Update User Role
```
PUT /api/admin/users/<user_id>/role
Authorization: Bearer <admin_token>
Body: { role: "admin" | "user" }
```

#### Delete User
```
DELETE /api/admin/users/<user_id>
Authorization: Bearer <admin_token>
```

## Accessing Admin Panel

### Prerequisites
- Admin account with `role='admin'` in database
- Login with admin credentials

### Steps
1. Navigate to `/pages/admin.html`
2. Or click the **👑 Admin** button in your dashboard (visible only to admins)

## Admin Credentials

**Default Admin Account:**
- Email: `admin@soilsense.com`
- Password: `admin@12345`

## Creating Additional Admin Users

### Method 1: Command Line Script
```bash
python create_admin.py <email> <password> "<Full Name>" "<Farm Name>"

# Example:
python create_admin.py admin2@example.com secure123 "John Admin" "Main Farm"
```

### Method 2: Direct Database
Update user role in SQLite:
```sql
UPDATE users SET role='admin' WHERE email='user@example.com';
```

## Checking Users

View all users and their roles:
```bash
python check_users.py
```

## Admin Panel Features

### User Search
- Real-time search by email or full name
- Case-insensitive matching

### Role Management
- Click **Edit** on any user row
- Select role: Admin (👑) or User (👤)
- Changes apply immediately

### User Deletion
- Click **Delete** on any user row
- Confirm deletion in modal
- All user data (analyses) will be deleted permanently

## Security Notes

⚠️ **Important:**
- Only users with `role='admin'` can access admin endpoints
- Admin endpoints are protected by `@admin_required` decorator
- Token must be valid and not expired
- Admins cannot delete themselves
- All admin actions are performed on authenticated requests

## Database Schema

**Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    full_name TEXT,
    farm_name TEXT,
    role TEXT CHECK(role IN ('admin', 'user')),  -- NEW
    is_active INTEGER,                            -- NEW
    created_at TIMESTAMP
);
```

## Files

- **Frontend**: `/pages/admin.html` - Admin panel UI
- **CSS**: `/css/admin.css` - Admin panel styling
- **JavaScript**: `/js/admin.js` - Admin panel functionality
- **Backend**: `/app.py` - Admin endpoints with `@admin_required` decorator
- **Scripts**: 
  - `/create_admin.py` - Create admin users
  - `/check_users.py` - View all users

## Troubleshooting

### "Admin access required" Error
- Your user account doesn't have admin role
- Login with a different admin account
- Contact your system administrator

### Can't see Admin Panel Link
- You're not logged in as admin
- Admin link only appears in dashboard for admin users

### User List Won't Load
- Check network connection
- Verify admin token is valid
- Check browser console for errors

## API Response Examples

### Get All Users
```json
{
  "users": [
    {
      "id": 1,
      "email": "admin@soilsense.com",
      "full_name": "SoilSense Admin",
      "farm_name": "Main Farm",
      "role": "admin",
      "created_at": "2026-02-20T10:00:00"
    },
    {
      "id": 2,
      "email": "user@example.com",
      "full_name": "John Doe",
      "farm_name": "Doe Farm",
      "role": "user",
      "created_at": "2026-02-20T11:00:00"
    }
  ],
  "total": 2
}
```

### Get Stats
```json
{
  "total_users": 10,
  "admin_count": 2,
  "total_analyses": 45
}
```
