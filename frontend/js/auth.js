// Authentication functions

function getToken() {
    return localStorage.getItem(config.TOKEN_KEY);
}

function getUser() {
    const user = localStorage.getItem(config.USER_KEY);
    return user ? JSON.parse(user) : null;
}

function setAuth(token, user) {
    localStorage.setItem(config.TOKEN_KEY, token);
    localStorage.setItem(config.USER_KEY, JSON.stringify(user));
}

function clearAuth() {
    localStorage.removeItem(config.TOKEN_KEY);
    localStorage.removeItem(config.USER_KEY);
}

function isAuthenticated() {
    return getToken() !== null;
}

function isAdmin() {
    const user = getUser();
    return user && user.role === 'Admin';
}

function checkAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

function logout() {
    clearAuth();
    window.location.href = 'index.html';
}

// API call helper with authentication
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${config.API_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}