# 🌱 SoilSense Admin Panel - Complete Setup Guide

## ✅ What's Been Implemented

### 1. **Admin Role System**
- Database updated with `role` column (admin/user)
- `is_active` column for account status
- Admin decorator `@admin_required` for protected endpoints

### 2. **Admin Control Panel**
Complete admin interface with:
- **Dashboard Statistics**: Total users, admin count, total analyses
- **User Management**: View, edit, delete users
- **Role Management**: Change user roles (Admin ↔ User)
- **Search Functionality**: Find users by email or name
- **Responsive Design**: Works on desktop and mobile

### 3. **Admin API Endpoints**

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/admin/users` | GET | List all users | Admin |
| `/api/admin/stats` | GET | System statistics | Admin |
| `/api/admin/users/<id>/role` | PUT | Update user role | Admin |
| `/api/admin/users/<id>` | DELETE | Delete user | Admin |

### 4. **Database Structure**

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT DEFAULT '',
    farm_name TEXT DEFAULT '',
    role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user')),  -- NEW
    is_active INTEGER DEFAULT 1,                                 -- NEW
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. **Frontend Components**

| File | Location | Purpose |
|------|----------|---------|
| admin.html | `/pages/admin.html` | Admin panel interface |
| admin.css | `/css/admin.css` | Admin styling |
| admin.js | `/js/admin.js` | Admin functionality |
| dashboard.html | Updated | Shows admin link |
| charts.js | Updated | Displays admin button |

### 6. **Backend Updates**

| File | Changes |
|------|---------|
| app.py | Added admin endpoints, admin_required decorator |
| db.py | Database schema updated |
| login endpoint | Returns user role |
| profile endpoint | Returns user role |

## 🚀 Getting Started

### Default Admin Account
```
Email: admin@soilsense.com
Password: admin@12345
```

### Access Admin Panel
1. Go to: `http://localhost:5000/pages/login.html`
2. Login with admin credentials
3. Click **👑 Admin** button in dashboard
4. Or directly visit: `http://localhost:5000/pages/admin.html`

### Admin Dashboard Features

#### View Statistics
- Real-time user count
- Admin count
- Total soil analyses performed

#### Manage Users
- **Search**: Find users by email or name
- **Edit Role**: Change user role with one click
- **Delete**: Remove users (with confirmation)

#### User Actions
```
[Edit Button] → Opens role selector → Save changes
[Delete Button] → Confirmation modal → Permanent deletion
```

## 📝 Create Additional Admins

### Method 1: Command Line (Recommended)
```bash
python create_admin.py admin2@example.com password123 "Admin Name" "Farm Name"
```

### Method 2: Direct SQL
```sql
UPDATE users SET role='admin' WHERE id=2;
```

## 🔍 Verify Installation

Run verification script:
```bash
python verify_admin_panel.py
```

Expected output:
```
✓ Database Status
✓ Admin Accounts
✓ Admin API Endpoints
✓ Frontend Files
ADMIN PANEL READY TO USE
```

## 📊 Admin Panel Capabilities

### Statistics Dashboard
Shows real-time metrics:
- Total registered users
- Number of admin users
- Total soil analyses in system

### User Management Table
Display all users with:
- User ID
- Email address
- Full name
- Farm name
- User role (Admin/User)
- Account creation date
- Action buttons (Edit/Delete)

### Role Management
- Toggle between Admin and User roles
- Modal confirmation
- Immediate effect

### User Deletion
- Soft delete option available
- Delete user and associated data
- Confirmation required
- Cannot delete self

## 🔐 Security Features

✅ **Protected Endpoints**
- Admin endpoints require `@admin_required` decorator
- Token validation on all requests
- Role verification

✅ **Data Validation**
- Input validation on all forms
- Role constraint in database
- Email uniqueness

✅ **Safety Features**
- Cannot delete own account
- Confirmation modals for critical actions
- Transaction safety

## 📋 Helper Scripts

### check_users.py
View all users and their roles:
```bash
python check_users.py
```

### create_admin.py
Create new admin users:
```bash
python create_admin.py <email> <password> [full_name] [farm_name]
```

### migrate_db.py
Backup and reinitialize database:
```bash
python migrate_db.py
```

### verify_admin_panel.py
Verify admin panel setup:
```bash
python verify_admin_panel.py
```

## 🎯 User Flow

```
Admin Login
    ↓
Dashboard (with Admin button visible)
    ↓
Click "👑 Admin" Button
    ↓
Admin Panel
    ├─ View Statistics
    ├─ Search Users
    ├─ Edit User Roles
    └─ Delete Users
```

## 📱 Responsive Design

Admin panel works on:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px+)
- ✅ Mobile (responsive tables)

## 🐛 Troubleshooting

### Issue: "Admin access required" Error
**Solution**: Login with an admin account

### Issue: Can't see Admin button
**Solution**: User must be logged in as admin

### Issue: Database errors
**Solution**: Run `python migrate_db.py` to reinitialize

## 📚 Files Created/Modified

### Created Files
- ✅ `/pages/admin.html` - Admin dashboard
- ✅ `/css/admin.css` - Admin styles
- ✅ `/js/admin.js` - Admin logic
- ✅ `create_admin.py` - Admin creation script
- ✅ `verify_admin_panel.py` - Verification script
- ✅ `ADMIN_PANEL_README.md` - Full documentation

### Modified Files
- ✅ `app.py` - Added admin endpoints
- ✅ `db.py` - Updated schema
- ✅ `charts.js` - Show admin link
- ✅ `dashboard.html` - Admin link added
- ✅ Login endpoint - Include role
- ✅ Profile endpoint - Include role

## 🎓 Next Steps

1. **Test the Admin Panel**
   ```bash
   # Start Flask server
   python app.py
   ```

2. **Login with Admin**
   - Email: `admin@soilsense.com`
   - Password: `admin@12345`

3. **Create More Admins**
   ```bash
   python create_admin.py newemail@example.com password123
   ```

4. **Test User Management**
   - Create a regular user account
   - Go to admin panel
   - Change user role to admin
   - Delete test user

## 💡 Tips

- Admin button only appears for admin users
- Search updates in real-time
- All changes take effect immediately
- Role changes don't require re-login
- Deleted users cannot be recovered

---

**Status**: ✅ ADMIN PANEL FULLY FUNCTIONAL

**Last Updated**: February 20, 2026
