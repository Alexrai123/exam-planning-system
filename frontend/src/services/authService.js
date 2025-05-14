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

// Add response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // If we get a 401 Unauthorized error, clear the token
    if (error.response && error.response.status === 401) {
      console.warn('Received 401 Unauthorized, clearing token');
      localStorage.removeItem('token');
    }
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
      console.log('Attempting login with:', { email });
      
      // Use direct axios call with timeout to prevent hanging
      const response = await axios.post(`${API_URL}/auth/login`, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        timeout: 10000 // 10 second timeout
      });
      
      // Check if we got a valid response
      if (!response || !response.data) {
        console.error('Invalid response from server');
        throw new Error('Invalid response from server');
      }
      
      console.log('Login response received');
      
      // Store token in localStorage
      if (response.data && response.data.access_token) {
        const token = response.data.access_token;
        console.log('Token received, storing in localStorage');
        localStorage.setItem('token', token);
        return response.data;
      } else {
        console.error('No token in response:', response.data);
        throw new Error('No token received from server');
      }
    } catch (error) {
      // Clear token on error
      localStorage.removeItem('token');
      
      if (error.response) {
        console.error('Login error response:', error.response.status, error.response.data);
      } else if (error.request) {
        console.error('Login error - no response received:', error.request);
      } else {
        console.error('Login error:', error.message);
      }
      
      throw error;
    }
  },

  // Get current user info
  getCurrentUser: async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.warn('getCurrentUser called with no token in localStorage');
      return null;
    }

    try {
      console.log('Fetching current user with token');
      
      // Use direct axios call with timeout to prevent hanging
      const response = await axios.get(`${API_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        timeout: 5000 // 5 second timeout to prevent hanging
      });
      
      // Validate the response
      if (!response || !response.data) {
        console.error('Invalid user data response');
        throw new Error('Invalid user data response');
      }
      
      console.log('Current user data received');
      return response.data;
    } catch (error) {
      // Handle different types of errors
      if (error.response) {
        console.error('Get user error response:', error.response.status, error.response.data);
        
        // If we get a 401 Unauthorized, the token is invalid or expired
        if (error.response.status === 401) {
          console.warn('Token is invalid or expired, clearing token from localStorage');
          localStorage.removeItem('token');
        }
      } else if (error.request) {
        console.error('Get user error - no response received:', error.request);
        // Network error or timeout - don't clear token as it might be a temporary issue
      } else {
        console.error('Get user error:', error.message);
      }
      
      throw error;
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('token');
  },

  // Check if user is logged in
  isLoggedIn: () => {
    return localStorage.getItem('token') !== null;
  },
  
  // Get the current token
  getToken: () => {
    return localStorage.getItem('token');
  },
};

export default authService;
