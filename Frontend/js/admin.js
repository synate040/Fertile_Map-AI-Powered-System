// ==================== ADMIN PANEL SCRIPT ====================

let currentEditingUserId = null;

document.addEventListener('DOMContentLoaded', () => {
    checkAuth(true); // Check if user is admin
    loadAdminStats();
    loadUsers();
    setupSearch();
});

/**
 * Check if current user is admin
 */
function checkAuth(requireAdmin = false) {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/pages/login.html';
        return;
    }

    if (requireAdmin) {
        // Decode token to check role
        try {
            const decoded = JSON.parse(atob(token.split('.')[1]));
            const userData = JSON.parse(localStorage.getItem('user'));
            
            // For now, we'll let them access and the API will reject if not admin
            // The API decorator @admin_required will handle this
        } catch (e) {
            console.error('Error decoding token:', e);
        }
    }
}

/**
 * Load admin statistics
 */
function loadAdminStats() {
    const token = localStorage.getItem('token');
    
    fetch('/api/admin/stats', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (response.status === 403) {
            alert('You do not have admin access');
            window.location.href = '/pages/dashboard.html';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        document.getElementById('totalUsers').textContent = data.total_users;
        document.getElementById('adminCount').textContent = data.admin_count;
        document.getElementById('totalAnalyses').textContent = data.total_analyses;
    })
    .catch(error => {
        console.error('Error loading stats:', error);
        alert('Failed to load admin statistics');
    });
}

/**
 * Load all users
 */
function loadUsers() {
    const token = localStorage.getItem('token');
    
    fetch('/api/admin/users', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (response.status === 403) {
            alert('You do not have admin access');
            window.location.href = '/pages/dashboard.html';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        displayUsers(data.users);
    })
    .catch(error => {
        console.error('Error loading users:', error);
        alert('Failed to load users');
    });
}

/**
 * Display users in table
 */
function displayUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    
    if (!users || users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading-text">No users found</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => {
        const isAdmin = user.role === 'admin';
        const roleBadge = isAdmin 
            ? '<span class="role-badge admin">👑 Admin</span>'
            : '<span class="role-badge user">👤 User</span>';
        
        const createdDate = new Date(user.created_at).toLocaleDateString();
        
        return `
            <tr>
                <td>${user.id}</td>
                <td><span class="user-email">${user.email}</span></td>
                <td>${user.full_name || '-'}</td>
                <td>${user.farm_name || '-'}</td>
                <td>${roleBadge}</td>
                <td><span class="user-date">${createdDate}</span></td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-edit btn-xs" onclick="openRoleModal(${user.id}, '${user.email}', '${user.role}')">Edit</button>
                        <button class="btn btn-danger btn-xs" onclick="openDeleteModal(${user.id}, '${user.email}')">Delete</button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

/**
 * Setup search functionality
 */
function setupSearch() {
    const searchInput = document.getElementById('searchUsers');
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('#usersTableBody tr');
        
        rows.forEach(row => {
            const email = row.querySelector('.user-email')?.textContent.toLowerCase() || '';
            const fullName = row.cells[2]?.textContent.toLowerCase() || '';
            
            if (email.includes(searchTerm) || fullName.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

/**
 * Refresh users list
 */
function refreshUsers() {
    loadUsers();
}

/**
 * Open role change modal
 */
function openRoleModal(userId, email, currentRole) {
    currentEditingUserId = userId;
    
    document.getElementById('roleUserInfo').textContent = `Changing role for: ${email}`;
    
    // Set current role
    const radios = document.querySelectorAll('input[name="userRole"]');
    radios.forEach(radio => {
        radio.checked = (radio.value === currentRole);
    });
    
    document.getElementById('roleModal').classList.add('show');
}

/**
 * Close role modal
 */
function closeRoleModal() {
    document.getElementById('roleModal').classList.remove('show');
    currentEditingUserId = null;
}

/**
 * Update user role preview
 */
function updateUserRolePreview() {
    // This could be used to show preview of changes
}

/**
 * Save user role change
 */
function saveUserRole() {
    const selectedRole = document.querySelector('input[name="userRole"]:checked').value;
    const token = localStorage.getItem('token');
    
    fetch(`/api/admin/users/${currentEditingUserId}/role`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ role: selectedRole })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        alert('User role updated successfully');
        closeRoleModal();
        loadUsers();
        loadAdminStats();
    })
    .catch(error => {
        console.error('Error updating role:', error);
        alert('Failed to update user role');
    });
}

/**
 * Open delete confirmation modal
 */
function openDeleteModal(userId, email) {
    currentEditingUserId = userId;
    
    document.getElementById('deleteUserInfo').innerHTML = `
        Are you sure you want to delete the user:<br>
        <strong>${email}</strong>?
    `;
    
    document.getElementById('deleteModal').classList.add('show');
}

/**
 * Close delete modal
 */
function closeDeleteModal() {
    document.getElementById('deleteModal').classList.remove('show');
    currentEditingUserId = null;
}

/**
 * Confirm delete user
 */
function confirmDeleteUser() {
    const token = localStorage.getItem('token');
    
    fetch(`/api/admin/users/${currentEditingUserId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        alert('User deleted successfully');
        closeDeleteModal();
        loadUsers();
        loadAdminStats();
    })
    .catch(error => {
        console.error('Error deleting user:', error);
        alert('Failed to delete user');
    });
}

/**
 * Logout user
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/pages/login.html';
}
