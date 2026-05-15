# Database Manager Documentation

## Overview
The Database Manager allows admin users to directly access and browse the SQLite database without going through the user management interface. This provides complete visibility into all database tables and their contents.

## Features

### 1. Database Information
- **Database Path**: Shows the full path to the SQLite database file
- **File Size**: Displays database file size in MB
- **Total Tables**: Shows number of tables in the database
- **Table Overview Cards**: Each table displays record count with quick-view button

### 2. Table Browsing
- **Table Selection**: Dropdown to select which table to view
- **Table Schema**: View column names, data types, primary keys, and constraints
- **Record Viewing**: Display all records from selected table (up to 100 records)
- **Search Functionality**: Search across all visible records in real-time

### 3. Data Security
- **Password Fields Hidden**: Automatically hides password and hash fields with `***hidden***`
- **Null Value Display**: Shows NULL values clearly with special formatting
- **Boolean Formatting**: Displays true/false values with color coding
- **Long Value Truncation**: Truncates values over 100 characters for readability

### 4. Data Export
- **Full Database Export**: Download entire database as JSON file
- **Timestamp Included**: Export file includes export timestamp
- **All Tables Included**: Export contains all database tables and records
- **Secure Download**: Export respects security settings (passwords still hidden)

## Access

### URL
```
/pages/database.html
```

### Requirements
- Must be logged in as admin user
- Admin role is required for all database endpoints

### Navigation
1. From Dashboard → Click "Admin Panel" → Click "🗄️ Database"
2. Or directly navigate to `/pages/database.html`

## Database Endpoints

### Get Database Info
```
GET /api/admin/database/info
```
Returns: Database path, file size, table list with row counts

### Get All Tables
```
GET /api/admin/database/tables
```
Returns: Array of table names

### Get Table Data
```
GET /api/admin/database/table/<table_name>
```
Returns: Columns, rows, and record count from specified table

### Get Table Schema
```
GET /api/admin/database/table/<table_name>/schema
```
Returns: Column details including type, primary key status, and constraints

## Examples

### Example 1: View Users Table
1. Navigate to Database Manager
2. Click "users" table card or select from dropdown
3. View all users with columns: id, email, password_hash, full_name, farm_name, role, is_active, created_at
4. Search for specific users using the search box

### Example 2: View Analyses Records
1. Select "analyses" from the table dropdown
2. View soil analysis records with columns: id, user_id, image_path, soil_type, confidence, properties, recommendations, crop_type, notes, created_at
3. Check record count and export if needed

### Example 3: Export Database
1. Click "💾 Export All" button
2. JSON file downloads: `soil_app_export_YYYY-MM-DD.json`
3. File contains all tables and their records

## Data Display Format

### Special Values
| Type | Display | Example |
|------|---------|---------|
| NULL | `NULL` (gray italic) | `NULL` |
| Boolean True | `True` (green) | `True` |
| Boolean False | `False` (red) | `False` |
| Password | `***hidden***` (red) | `***hidden***` |
| Long Text | Truncated at 100 chars | `Lorem ipsum dolor sit...` |

## Security Features

- ✅ **Admin-Only Access**: All endpoints protected by @admin_required decorator
- ✅ **Password Hiding**: Sensitive fields automatically hidden
- ✅ **Token Authentication**: JWT token required for all requests
- ✅ **SQL Injection Prevention**: Table names validated before queries
- ✅ **Input Validation**: All user inputs sanitized

## Files Involved

### Backend
- `Backend/app.py`: Contains 5 new admin database endpoints
- `Backend/db.py`: Database connection management

### Frontend
- `Frontend/pages/database.html`: Database manager interface (HTML)
- `Frontend/js/database.js`: Database browser functionality (JavaScript)
- `Frontend/css/database.css`: Database manager styling (CSS)

### Updated Files
- `Frontend/pages/admin.html`: Added database link to navigation

## Table Structure

### Users Table
```
id (INTEGER, PRIMARY KEY)
email (TEXT, UNIQUE)
password_hash (TEXT)
full_name (TEXT)
farm_name (TEXT)
role (TEXT) - 'user' or 'admin'
is_active (INTEGER) - 1 or 0
created_at (TIMESTAMP)
```

### Analyses Table
```
id (INTEGER, PRIMARY KEY)
user_id (INTEGER, FOREIGN KEY)
image_path (TEXT)
soil_type (TEXT)
confidence (REAL)
properties (TEXT)
recommendations (TEXT)
crop_type (TEXT)
notes (TEXT)
created_at (TIMESTAMP)
```

## Troubleshooting

### Cannot Access Database Manager
- **Issue**: 404 error or redirect to login
- **Solution**: 
  - Verify you're logged in as admin user
  - Check token in browser's localStorage
  - Try clearing cache and logging in again

### No Tables Showing
- **Issue**: Database info loads but no tables visible
- **Solution**:
  - Verify database file exists at `Backend/database/soil_app.db`
  - Run `python Backend/migrate_db.py` to reinitialize database
  - Check file permissions

### Export Not Working
- **Issue**: Export button doesn't download file
- **Solution**:
  - Check browser's download settings
  - Verify sufficient disk space
  - Try different browser if issue persists

### Search Not Finding Records
- **Issue**: Search returns no results even for existing values
- **Solution**:
  - Search is case-insensitive, try different terms
  - Search only works on currently loaded records (max 100)
  - Try reloading the page

## Performance Notes

- ⚡ **Record Limit**: Tables limited to 100 most recent records for performance
- ⚡ **Search**: Real-time search filters loaded records only
- ⚡ **Large Tables**: Export of very large databases may take time
- ⚡ **Long Values**: Values over 100 characters truncated in display

## Future Enhancements

Potential features for future versions:
- [ ] Edit/Update records directly
- [ ] Add new records to tables
- [ ] Delete individual records with confirmation
- [ ] SQL query editor
- [ ] Table statistics and analytics
- [ ] Column filtering and sorting
- [ ] Pagination for large tables
- [ ] CSV export option

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Flask debug output in terminal
3. Check browser console for JavaScript errors (F12)
4. Verify database file integrity with `sqlite3 soil_app.db ".tables"`
