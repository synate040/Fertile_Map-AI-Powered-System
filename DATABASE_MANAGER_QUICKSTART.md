# Database Manager - Quick Start Guide

## 🚀 Launch the App

```bash
cd Backend
python app.py
```

Then open: `http://localhost:5000/pages/login.html`

## 🔐 Login as Admin

**Email**: `admin@soilsense.com`  
**Password**: `admin@12345`

## 📊 Access Database Manager

From Dashboard:
1. Click **"Admin Panel"** (top navigation)
2. Click **"🗄️ Database"** (in navbar or new tab)
3. Or go directly to: `http://localhost:5000/pages/database.html`

## ✨ Features

### Database Overview
- File size and location
- Total tables and record counts
- Quick-access table cards

### Browse Tables
- Select any table from dropdown
- View table schema (columns, types)
- See all records (up to 100)
- Real-time search across records

### Export Database
- Click **"💾 Export All"** button
- Saves as JSON with timestamp
- Contains all tables and records

## 🛡️ Security

✅ Only admins can access  
✅ JWT token authentication  
✅ Passwords automatically hidden  
✅ SQL injection prevention  

## 📋 Tables Available

### Users Table
- id, email, password_hash, full_name, farm_name, role, is_active, created_at

### Analyses Table  
- id, user_id, image_path, soil_type, confidence, properties, recommendations, crop_type, notes, created_at

## 🔗 API Endpoints

```
GET  /api/admin/database/info              - Database information
GET  /api/admin/database/tables             - List all tables
GET  /api/admin/database/table/<name>      - Get table records
GET  /api/admin/database/table/<name>/schema - Get table schema
```

All require admin authentication.

## 🎯 Common Tasks

### View All Users
1. Select "users" table
2. See full list with roles

### Check Analysis History  
1. Select "analyses" table
2. Browse all soil analyses

### Search Records
1. Select table
2. Type in search box
3. Results filter in real-time

### Backup Database
1. Click "Export All"
2. JSON file downloads automatically
3. Save to safe location

## 📚 Documentation

- **DATABASE_MANAGER_README.md** - Complete guide
- **IMPLEMENT_DATABASE_MANAGER.md** - Technical details
- **Backend/verify_database_manager.py** - Run to verify setup

## ❓ Troubleshooting

**Can't access Database Manager?**
- Log in as admin (not regular user)
- Check browser console (F12) for errors

**No tables showing?**
- Database must exist at `Backend/database/soil_app.db`
- Run `python migrate_db.py` to create/reset

**Export not working?**
- Check browser's download permissions
- Try different browser if persists

## 🎓 Example Workflow

1. **Login** as admin@soilsense.com
2. **Go to** Dashboard
3. **Click** Admin Panel → Database
4. **Select** "users" table
5. **View** all users and their roles
6. **Search** for specific users
7. **Check** "analyses" table for soil data
8. **Export** database as backup

---

**Database Manager is ready to use!** 🎉

For more details, see DATABASE_MANAGER_README.md
