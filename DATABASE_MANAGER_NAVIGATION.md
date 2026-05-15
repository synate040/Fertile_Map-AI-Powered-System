# 🗄️ Database Manager - Step-by-Step Navigation

## Quick Access Path

```
Login Page (http://localhost:5000/pages/login.html)
    ↓
    Login as: admin@soilsense.com / admin@12345
    ↓
Dashboard (http://localhost:5000/pages/dashboard.html)
    ↓
    Click "👑 Admin Panel" button
    ↓
Admin Panel (http://localhost:5000/pages/admin.html)
    ↓
    Click "🗄️ Database" link in navbar
    ↓
Database Manager (http://localhost:5000/pages/database.html)
    ↓
    ✓ Browse Tables
    ✓ View Records
    ✓ Search Data
    ✓ Export Database
```

## Direct URL Access

If you're already logged in as admin, go directly to:

```
http://localhost:5000/pages/database.html
```

## Navigation Elements in Admin Panel

The Database Manager is linked from the admin panel navbar:

```
┌─────────────────────────────────────┐
│ Dashboard  │ Admin Panel  │ 🗄️ DB   │
└─────────────────────────────────────┘
                           ↑
                    Database Link
                  (You are here when
                   Database Manager
                   is active)
```

## Features on Database Manager Page

### 1. Database Information Card
```
┌─ Database Information ──────────────┐
│ Database Path: C:\...\soil_app.db  │
│ File Size: 0.03 MB                 │
│ Total Tables: 2                    │
└─────────────────────────────────────┘
```

### 2. Tables Overview Section
```
┌──────────────┬──────────────┐
│   users      │  analyses    │
├──────────────┼──────────────┤
│ 5 records    │ 12 records   │
│ [View Btn]   │ [View Btn]   │
└──────────────┴──────────────┘
```

### 3. Table Browser Section
```
┌─ Table Data ────────────────────┐
│ Select table: [users ▼]         │
│ Search: [           ]           │
├─────────────────────────────────┤
│ Table Schema                    │
│ ┌────────────────────────────┐  │
│ │ Column | Type | PK | NotNl │  │
│ ├────────────────────────────┤  │
│ │ id     | INT  | ✓  | ✓    │  │
│ │ email  | TEXT |    | ✓    │  │
│ └────────────────────────────┘  │
├─────────────────────────────────┤
│ Table Records (5 records)       │
│ ┌────────────────────────────┐  │
│ │ ID │ Email  │ Full Name   │  │
│ ├────────────────────────────┤  │
│ │ 1  │ admin@ │ Admin User  │  │
│ │ 2  │ user@  │ Regular User│  │
│ └────────────────────────────┘  │
└─────────────────────────────────┘
```

## Action Buttons

### Top Right Buttons
- **🔄 Refresh** - Reload database information
- **💾 Export All** - Download entire database as JSON

### Table Card Actions
- **[View]** - Click to load that table's data

### Table Selection
- **Dropdown** - Select which table to browse
- **Search Box** - Filter records in real-time

## What You Can Do

✅ **View Database Info**
   1. See file location and size
   2. Check total number of tables
   3. See record count for each table

✅ **Browse Table Data**
   1. Select a table from dropdown
   2. View table schema (columns, data types)
   3. See all records in table
   4. Check primary keys and constraints

✅ **Search Records**
   1. Select a table
   2. Type in search box
   3. Results filter in real-time
   4. Case-insensitive search

✅ **View Table Schema**
   1. Select a table
   2. "Table Schema" section shows:
      - Column names
      - Data types (INTEGER, TEXT, etc.)
      - Primary key indicator
      - Not-null constraint indicator

✅ **Export Database**
   1. Click "💾 Export All" button
   2. JSON file downloads automatically
   3. File named: `soil_app_export_YYYY-MM-DD.json`
   4. Contains all tables and records

## Special Data Display

The database manager automatically formats special values:

| Value Type | Display | Example |
|-----------|---------|---------|
| NULL | `NULL` (gray) | `NULL` |
| Password field | `***hidden***` (red) | `***hidden***` |
| Boolean True | `True` (green) | `True` |
| Boolean False | `False` (red) | `False` |
| Long text | Truncated + ... | `Lorem ipsum do...` |

## Keyboard Shortcuts

- **Tab** - Navigate between elements
- **Enter** - Select dropdown options
- **Ctrl+F** - Browser find (NOT same as search box)
- **Ctrl+S** - Save exported file (after download)

## Mobile/Tablet Usage

Database manager is responsive and works on:
- ✓ Desktop (full features)
- ✓ Tablet (touch-friendly buttons)
- ✓ Mobile (optimized layout)

**Note**: On mobile, the table may scroll horizontally if many columns

## Session Management

- Must be logged in as admin user
- Your session lasts for 24 hours
- Click "Logout" to end session
- Leaving page doesn't log you out automatically

## Common Workflows

### View All Users
1. Select "users" from table dropdown
2. View full list with email, role, etc.
3. Search by email or name

### Check Soil Analyses
1. Select "analyses" from dropdown
2. View all soil analysis records
3. Check timestamps and user associations

### Search for Specific User
1. Select "users" table
2. Type email/name in search box
3. Results update instantly

### Export for Backup
1. Click "💾 Export All"
2. JSON file downloads
3. Save to safe location
4. Can be used for backup or analysis

### Check Database Size
1. Look at "Database Information" card
2. See file size in MB
3. Helps monitor database growth

## Troubleshooting Navigation

**Can't find Database link?**
- Make sure you're logged in as admin
- Check that you're on Admin Panel page
- Refresh the page (F5)

**Database Manager page won't load?**
- Verify you're still logged in
- Check browser console (F12) for errors
- Try direct URL: http://localhost:5000/pages/database.html

**Tables not showing?**
- Database file may not exist
- Run `python Backend/migrate_db.py` to create it
- Refresh the page

**Search not working?**
- Make sure a table is selected
- Search is case-insensitive
- Try shorter search terms

## Related Pages

- **Dashboard** - Main user interface
- **Admin Panel** - User management
- **Profile** - User profile settings
- **Capture** - Soil analysis capture
- **History** - Analysis history

---

**You now have full database access as an admin user!** 🎉

For more details, see DATABASE_MANAGER_README.md
