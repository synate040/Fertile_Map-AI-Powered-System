// ==================== API HELPER ====================
const API_BASE = '/api';

class API {
    static getToken() {
        return localStorage.getItem('token');
    }

    static getHeaders(isFormData = false) {
        const headers = {};
        const token = this.getToken();
        if (token) {
            console.log('[API] Using token:', token.substring(0, 20) + '...');
            headers['Authorization'] = `Bearer ${token}`;
        } else {
            console.warn('[API] No token found in localStorage');
        }
        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }
        return headers;
    }

    static async get(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: this.getHeaders()
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Request failed');
        }
        return response.json();
    }

    static async post(endpoint, data) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Request failed');
        }
        return response.json();
    }

    static async postForm(endpoint, formData) {
        const headers = this.getHeaders(true);
        console.log('[API.postForm] Endpoint:', endpoint);
        console.log('[API.postForm] Headers:', headers);
        const token = this.getToken();
        console.log('[API.postForm] Token from storage:', token);
        
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: headers,
            body: formData
        });
        if (!response.ok) {
            const error = await response.json();
            console.error('[API.postForm] Error response:', error);
            throw new Error(error.error || 'Request failed');
        }
        return response.json();
    }

    static async delete(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'DELETE',
            headers: this.getHeaders()
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Request failed');
        }
        return response.json();
    }
}