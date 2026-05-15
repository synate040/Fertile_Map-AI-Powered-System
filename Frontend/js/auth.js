// ==================== AUTHENTICATION ====================

// Check if user is logged in and update nav
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || 'null');

    const authNav = document.getElementById('authNav');
    const userNav = document.getElementById('userNav');

    if (authNav && userNav) {
        if (token && user) {
            authNav.style.display = 'none';
            userNav.style.display = 'flex';
        } else {
            authNav.style.display = 'flex';
            userNav.style.display = 'none';
        }
    }
}

// Form validation helper
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    // At least 6 characters
    return password.length >= 6;
}

function showFieldError(fieldElement, message) {
    fieldElement.classList.add('error');
    const errorEl = fieldElement.nextElementSibling;
    if (errorEl && errorEl.classList.contains('error-message')) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
        errorEl.style.animation = 'slideDown 0.3s ease';
    }
}

function clearFieldError(fieldElement) {
    fieldElement.classList.remove('error');
    const errorEl = fieldElement.nextElementSibling;
    if (errorEl && errorEl.classList.contains('error-message')) {
        errorEl.style.display = 'none';
    }
}

// Handle Login
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const errorDiv = document.getElementById('loginError');
    const loginBtn = document.getElementById('loginBtn');

    // Clear previous errors
    errorDiv.style.display = 'none';
    clearFieldError(email);
    clearFieldError(password);

    // Validate form
    let hasErrors = false;
    if (!email.value.trim()) {
        showFieldError(email, 'Email is required');
        hasErrors = true;
    } else if (!validateEmail(email.value)) {
        showFieldError(email, 'Please enter a valid email');
        hasErrors = true;
    }

    if (!password.value.trim()) {
        showFieldError(password, 'Password is required');
        hasErrors = true;
    }

    if (hasErrors) return;

    loginBtn.textContent = 'Logging in...';
    loginBtn.disabled = true;
    loginBtn.style.opacity = '0.7';

    try {
        const response = await API.post('/auth/login', { 
            email: email.value,
            password: password.value 
        });

        // Handle API response structure
        console.log('Login response:', response);
        const data = response.data || response;  // Handle both wrapped and unwrapped responses
        
        if (!data.token) {
            console.error('No token in login response');
            throw new Error('No token received from server');
        }
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('userEmail', data.user.email);
        localStorage.setItem('userRole', data.user.role);
        console.log('Token saved:', localStorage.getItem('token'));

        // Show success toast
        showToast('Login successful! Redirecting...', 'success', 1500);

        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = '/pages/dashboard.html';
        }, 500);

    } catch (error) {
        errorDiv.textContent = error.message || 'Login failed. Please try again.';
        errorDiv.style.display = 'block';
        errorDiv.style.animation = 'slideDown 0.3s ease';
        showToast(error.message || 'Login failed', 'error');
    } finally {
        loginBtn.textContent = 'Login';
        loginBtn.disabled = false;
        loginBtn.style.opacity = '1';
    }
}

// Handle Registration
async function handleRegister(event) {
    event.preventDefault();

    const fullName = document.getElementById('fullName');
    const email = document.getElementById('email');
    const farmName = document.getElementById('farmName');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const errorDiv = document.getElementById('registerError');
    const successDiv = document.getElementById('registerSuccess');
    const registerBtn = document.getElementById('registerBtn');

    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';

    // Clear previous field errors
    [fullName, email, farmName, password, confirmPassword].forEach(field => {
        clearFieldError(field);
    });

    // Validate form
    let hasErrors = false;
    if (!fullName.value.trim()) {
        showFieldError(fullName, 'Full name is required');
        hasErrors = true;
    }

    if (!email.value.trim()) {
        showFieldError(email, 'Email is required');
        hasErrors = true;
    } else if (!validateEmail(email.value)) {
        showFieldError(email, 'Please enter a valid email');
        hasErrors = true;
    }

    if (!farmName.value.trim()) {
        showFieldError(farmName, 'Farm name is required');
        hasErrors = true;
    }

    if (!password.value) {
        showFieldError(password, 'Password is required');
        hasErrors = true;
    } else if (!validatePassword(password.value)) {
        showFieldError(password, 'Password must be at least 6 characters');
        hasErrors = true;
    }

    if (password.value !== confirmPassword.value) {
        showFieldError(confirmPassword, 'Passwords do not match');
        hasErrors = true;
    }

    if (hasErrors) return;

    registerBtn.textContent = 'Creating Account...';
    registerBtn.disabled = true;
    registerBtn.style.opacity = '0.7';

    try {
        await API.post('/auth/register', {
            full_name: fullName.value,
            email: email.value,
            password: password.value,
            farm_name: farmName.value
        });

        successDiv.textContent = '✓ Account created successfully! Redirecting to login...';
        successDiv.style.display = 'block';
        successDiv.style.animation = 'slideDown 0.3s ease';
        showToast('Account created! Redirecting...', 'success');

        setTimeout(() => {
            window.location.href = '/pages/login.html';
        }, 2000);

    } catch (error) {
        errorDiv.textContent = error.message || 'Registration failed. Please try again.';
        errorDiv.style.display = 'block';
        errorDiv.style.animation = 'slideDown 0.3s ease';
        showToast(error.message || 'Registration failed', 'error');
    } finally {
        registerBtn.textContent = 'Create Account';
        registerBtn.disabled = false;
        registerBtn.style.opacity = '1';
    }
}

// Logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userRole');
    showToast('Logged out successfully!', 'success', 1500);
    setTimeout(() => {
        window.location.href = '/pages/login.html';
    }, 500);
}

// Protect page — redirect if not logged in
function requireAuth() {
    if (!localStorage.getItem('token')) {
        window.location.href = '/pages/login.html';
        return false;
    }
    return true;
}

// Run on page load
document.addEventListener('DOMContentLoaded', checkAuth);