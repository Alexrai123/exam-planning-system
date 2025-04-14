import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/auth/Login';
import TestLogin from './components/auth/TestLogin';
import Dashboard from './components/Dashboard';
import SimpleTestDashboard from './components/SimpleTestDashboard';
import ForgotPassword from './components/auth/ForgotPassword';
import Register from './components/auth/Register';
import './App.css';

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  // Check if token exists in localStorage as a fallback
  const hasToken = !!localStorage.getItem('token');
  
  if (!isAuthenticated && !hasToken) {
    return <Navigate to="/" />;
  }
  
  return children;
};

// Simple protected route that only checks for token
const SimpleProtectedRoute = ({ children }) => {
  const hasToken = !!localStorage.getItem('token');
  
  if (!hasToken) {
    return <Navigate to="/test-login" />;
  }
  
  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/test-login" element={<TestLogin />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/test-dashboard" 
            element={
              <SimpleProtectedRoute>
                <SimpleTestDashboard />
              </SimpleProtectedRoute>
            } 
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
