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
      if (authService.isLoggedIn()) {
        try {
          const userData = await authService.getCurrentUser();
          setCurrentUser(userData);
          setIsAuthenticated(true);
        } catch (err) {
          console.error('Failed to load user:', err);
          authService.logout(); // Clear invalid token
          setError('Session expired. Please login again.');
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  // Login function
  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      // First attempt to login and get token
      const loginResponse = await authService.login(email, password);
      console.log('Login successful, token received:', loginResponse);
      
      // Then fetch the user data
      try {
        const userData = await authService.getCurrentUser();
        console.log('User data fetched successfully:', userData);
        setCurrentUser(userData);
        setIsAuthenticated(true);
        return userData;
      } catch (userError) {
        console.error('Error fetching user data after login:', userError);
        // Even if we can't fetch user data, we're still authenticated with a token
        setIsAuthenticated(true);
        // Just set minimal user info based on email
        const minimalUserData = { email: email };
        setCurrentUser(minimalUserData);
        return minimalUserData;
      }
    } catch (err) {
      console.error('Login failed:', err);
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
      setIsAuthenticated(false);
      throw err;
    } finally {
      setLoading(false);
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
    loading,
    error,
    isAuthenticated,
    login,
    logout
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
