// Database Manager Functionality
let currentTableName = null;
let allTableData = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadDatabaseInfo();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('logoutBtn').addEventListener('click', logout);
    document.getElementById('refreshBtn').addEventListener('click', loadDatabaseInfo);
    document.getElementById('exportBtn').addEventListener('click', exportDatabase);
    document.getElementById('tableSelect').addEventListener('change', handleTableSelect);
    document.getElementById('searchInput').addEventListener('input', filterTableData);
}

// Check authentication and show admin links
async function checkAuth() {
    const token = localStorage.getItem('token');
    const userEmail = localStorage.getItem('userEmail');
    const userRole = localStorage.getItem('userRole');

    if (!token) {
        window.location.href = '/pages/login.html';
        return;
    }

    // Show user role
    document.getElementById('userRole').textContent = userRole ? userRole.toUpperCase() : 'USER';

    // Show admin links for admin users
    if (userRole === 'admin') {
        const adminLinksContainer = document.getElementById('adminLinksContainer');
        adminLinksContainer.innerHTML = `
            <a href="admin.html" class="nav-link admin-link">
                <span class="icon">⚙️</span>
                <span>User Management</span>
            </a>
            <a href="database.html" class="nav-link admin-link active">
                <span class="icon">🗄️</span>
                <span>Database Manager</span>
            </a>
        `;
    }
}

// Load database information
async function loadDatabaseInfo() {
    try {
        const response = await fetch('/api/admin/database/info', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load database info');
        }

        const data = await response.json();

        // Update database info
        document.getElementById('dbPath').textContent = data.database_path;
        document.getElementById('dbSize').textContent = `${data.file_size_mb} MB`;
        document.getElementById('totalTables').textContent = data.total_tables;

        // Load tables overview
        loadTablesOverview(data.tables);

        // Populate table select dropdown
        loadTableSelect(data.tables);

    } catch (error) {
        console.error('Error loading database info:', error);
        alert('Error loading database information: ' + error.message);
    }
}

// Load tables overview cards
async function loadTablesOverview(tables) {
    const container = document.getElementById('tablesOverview');
    container.innerHTML = '';

    for (const table of tables) {
        const card = document.createElement('div');
        card.className = 'table-card';
        card.innerHTML = `
            <h3>${table.name}</h3>
            <p>${table.row_count} <span>record${table.row_count !== 1 ? 's' : ''}</span></p>
            <button class="btn btn-small" onclick="handleTableCardClick('${table.name}')">
                View
            </button>
        `;
        container.appendChild(card);
    }
}

// Load table select dropdown
async function loadTableSelect(tables) {
    const select = document.getElementById('tableSelect');
    const currentValue = select.value;

    // Keep the default option
    select.innerHTML = '<option value="">Select a table to view...</option>';

    for (const table of tables) {
        const option = document.createElement('option');
        option.value = table.name;
        option.textContent = `${table.name} (${table.row_count} records)`;
        select.appendChild(option);
    }

    // Restore previous selection if it still exists
    if (currentValue && Array.from(select.options).some(opt => opt.value === currentValue)) {
        select.value = currentValue;
    }
}

// Handle table card click
function handleTableCardClick(tableName) {
    document.getElementById('tableSelect').value = tableName;
    handleTableSelect();
}

// Handle table selection
async function handleTableSelect() {
    const tableName = document.getElementById('tableSelect').value;

    if (!tableName) {
        document.getElementById('tableDataContainer').style.display = 'none';
        document.getElementById('schemaInfo').style.display = 'none';
        document.getElementById('noTableSelected').style.display = 'block';
        document.getElementById('searchInput').value = '';
        currentTableName = null;
        return;
    }

    currentTableName = tableName;

    try {
        // Load schema
        await loadTableSchema(tableName);

        // Load table data
        await loadTableData(tableName);

        document.getElementById('noTableSelected').style.display = 'none';
        document.getElementById('tableDataContainer').style.display = 'block';

    } catch (error) {
        console.error('Error loading table:', error);
        alert('Error loading table data: ' + error.message);
    }
}

// Load table schema
async function loadTableSchema(tableName) {
    try {
        const response = await fetch(`/api/admin/database/table/${tableName}/schema`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load table schema');
        }

        const data = await response.json();
        const schemaBody = document.getElementById('schemaBody');
        schemaBody.innerHTML = '';

        for (const column of data.schema) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${column.name}</strong></td>
                <td>${column.type}</td>
                <td>${column.pk ? '✓ Yes' : 'No'}</td>
                <td>${column.notnull ? '✓ Yes' : 'No'}</td>
            `;
            schemaBody.appendChild(row);
        }

        document.getElementById('schemaInfo').style.display = 'block';

    } catch (error) {
        console.error('Error loading table schema:', error);
        // Don't throw, just hide schema info
        document.getElementById('schemaInfo').style.display = 'none';
    }
}

// Load table data
async function loadTableData(tableName) {
    try {
        const response = await fetch(`/api/admin/database/table/${tableName}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load table data');
        }

        const data = await response.json();
        allTableData = data;

        // Create table columns
        const tableHead = document.getElementById('tableHead');
        tableHead.innerHTML = '<tr>';
        for (const column of data.columns) {
            const th = document.createElement('th');
            th.textContent = column;
            tableHead.appendChild(th);
        }
        tableHead.innerHTML += '</tr>';

        // Populate table data
        displayTableData(data.rows);

        // Update record count
        document.getElementById('recordCount').textContent = `${data.row_count} record${data.row_count !== 1 ? 's' : ''}`;
        document.getElementById('recordsTitle').textContent = `${tableName} Records`;

    } catch (error) {
        console.error('Error loading table data:', error);
        throw error;
    }
}

// Display table data
function displayTableData(rows) {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    if (rows.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="100%" class="empty-message">No records found</td></tr>';
        return;
    }

    for (const row of rows) {
        const tr = document.createElement('tr');
        for (const key in row) {
            const td = document.createElement('td');
            let value = row[key];

            // Format special values
            if (value === null) {
                td.innerHTML = '<span class="null-value">NULL</span>';
            } else if (typeof value === 'boolean') {
                td.innerHTML = value ? '<span class="bool-true">True</span>' : '<span class="bool-false">False</span>';
            } else if (key.includes('password') || key.includes('hash')) {
                td.innerHTML = '<span class="sensitive-value">***hidden***</span>';
                td.title = 'Password field hidden for security';
            } else {
                // Truncate long values
                const displayValue = String(value).length > 100 
                    ? String(value).substring(0, 100) + '...' 
                    : String(value);
                td.textContent = displayValue;
            }
            tr.appendChild(td);
        }
        tableBody.appendChild(tr);
    }
}

// Filter table data
function filterTableData() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const tableBody = document.getElementById('tableBody');
    const rows = Array.from(tableBody.querySelectorAll('tr'));

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// Export database
async function exportDatabase() {
    try {
        const response = await fetch('/api/admin/database/info', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to export database');
        }

        const dbInfo = await response.json();

        // Collect all tables data
        const exportData = {
            timestamp: new Date().toISOString(),
            database_path: dbInfo.database_path,
            file_size_mb: dbInfo.file_size_mb,
            tables: {}
        };

        for (const table of dbInfo.tables) {
            try {
                const tableResponse = await fetch(`/api/admin/database/table/${table.name}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });

                if (tableResponse.ok) {
                    const tableData = await tableResponse.json();
                    exportData.tables[table.name] = tableData.rows;
                }
            } catch (error) {
                console.error(`Error exporting table ${table.name}:`, error);
            }
        }

        // Download as JSON
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `soil_app_export_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        alert('Database exported successfully!');

    } catch (error) {
        console.error('Error exporting database:', error);
        alert('Error exporting database: ' + error.message);
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userRole');
    window.location.href = '/pages/login.html';
}
