import React, { createContext, useState, useEffect, useContext } from 'react';
import authService from '../services/authService';

// Create the auth context
const AuthContext = createContext(null);

// Auth context provider component
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Load user on initial render if token exists
  useEffect(() => {
    const loadUser = async () => {
      // Set loading to true while we check authentication
      setLoading(true);
      
      if (authService.isLoggedIn()) {
        try {
          const userData = await authService.getCurrentUser();
          setCurrentUser(userData);
          setIsAuthenticated(true);
        } catch (err) {
          console.error('Failed to load user:', err);
          // Clear any invalid token
          authService.logout();
          setError('Session expired. Please login again.');
          setIsAuthenticated(false);
          setCurrentUser(null);
        }
      } else {
        // Make sure we reset state if no token exists
        setIsAuthenticated(false);
        setCurrentUser(null);
      }
      
      // Always set loading to false when done
      setLoading(false);
    };

    loadUser();
  }, []);

  // Login function
  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    
    // Clear any existing data first
    setCurrentUser(null);
    setIsAuthenticated(false);
    authService.logout(); // Clear any existing token
    
    try {
      // Step 1: Login and get token
      console.log('Attempting to login with email:', email);
      const loginResponse = await authService.login(email, password);
      console.log('Login successful, token received');
      
      // Step 2: Fetch user data with the new token
      try {
        console.log('Fetching user data...');
        const userData = await authService.getCurrentUser();
        console.log('User data fetched successfully:', userData);
        
        // Set user data and authentication state
        setCurrentUser(userData);
        setIsAuthenticated(true);
        setLoading(false);
        return userData;
      } catch (userError) {
        console.error('Error fetching user data:', userError);
        
        // Even if we can't fetch complete user data, create minimal user info
        // This prevents login loops by ensuring we have some user data
        const minimalUserData = { 
          email: email,
          role: 'UNKNOWN' // Default role until we can fetch the actual role
        };
        
        setCurrentUser(minimalUserData);
        setIsAuthenticated(true);
        setLoading(false);
        return minimalUserData;
      }
    } catch (err) {
      console.error('Login failed:', err);
      
      // Clear everything on login failure
      authService.logout();
      setCurrentUser(null);
      setIsAuthenticated(false);
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
      setLoading(false);
      
      throw err;
    }
  };

  // Logout function
  const logout = () => {
    authService.logout();
    setCurrentUser(null);
    setIsAuthenticated(false);
  };

  // Context value
  const value = {
    currentUser,
    isAuthenticated,
    loading,
    error,
    login,
    logout,
    token: authService.getToken() // Expose token for API calls
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
