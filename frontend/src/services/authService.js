import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Create axios instance with base URL
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add interceptor to add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth service functions
const authService = {
  // Login user
  login: async (email, password) => {
    // Clear any existing token first to avoid conflicts
    localStorage.removeItem('token');
    
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    try {
      console.log('Attempting login with:', { email, formData: formData.toString() });
      
      // Use direct fetch API instead of axios for more control
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });
      
      console.log('Login response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Login failed:', errorData);
        throw new Error(errorData.detail || 'Login failed');
      }
      
      const data = await response.json();
      console.log('Login successful, received data:', data);
      
      // Store token in localStorage
      if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        return data;
      } else {
        throw new Error('No token received from server');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Get current user info
  getCurrentUser: async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      return null;
    }

    try {
      console.log('Fetching current user with token:', token);
      const response = await fetch(`${API_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch user: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Current user response:', data);
      return data;
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('token');
  },

  // Check if user is logged in
  isLoggedIn: () => {
    return !!localStorage.getItem('token');
  }
};

export default authService;
