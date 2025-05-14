import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const LoginBypass = () => {
  const navigate = useNavigate();
  const [status, setStatus] = useState('Checking API...');
  const [error, setError] = useState(null);

  useEffect(() => {
    const attemptLogin = async () => {
      try {
        // Clear any existing tokens
        localStorage.removeItem('token');
        
        // Step 1: Check if API is accessible
        setStatus('Checking API connection...');
        try {
          await axios.get(`${API_URL}/`);
          setStatus('API connection successful');
        } catch (error) {
          setStatus('API connection failed. Trying login anyway...');
        }
        
        // Step 2: Attempt login with hardcoded credentials
        setStatus('Attempting login...');
        const formData = new URLSearchParams();
        formData.append('username', 'admin@example.com');
        formData.append('password', 'password');
        
        const loginResponse = await axios.post(`${API_URL}/auth/login`, formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          timeout: 10000
        });
        
        if (loginResponse.data && loginResponse.data.access_token) {
          setStatus('Login successful, got token');
          localStorage.setItem('token', loginResponse.data.access_token);
          
          // Step 3: Get user data
          setStatus('Getting user data...');
          const userResponse = await axios.get(`${API_URL}/users/me`, {
            headers: {
              'Authorization': `Bearer ${loginResponse.data.access_token}`
            },
            timeout: 5000
          });
          
          setStatus('User data retrieved successfully');
          console.log('User data:', userResponse.data);
          
          // Step 4: Store minimal user data in localStorage as a fallback
          const userData = {
            id: userResponse.data.id,
            name: userResponse.data.name,
            email: userResponse.data.email,
            role: userResponse.data.role
          };
          
          localStorage.setItem('user', JSON.stringify(userData));
          setStatus('Redirecting to dashboard...');
          
          // Redirect to emergency dashboard after a short delay
          setTimeout(() => {
            navigate('/emergency-dashboard');
          }, 1000);
        } else {
          setError('No token received from server');
        }
      } catch (error) {
        console.error('Login bypass error:', error);
        setError(error.message || 'Unknown error occurred');
        setStatus('Login failed');
      }
    };
    
    attemptLogin();
  }, [navigate]);
  
  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center',
      height: '100vh',
      padding: '20px',
      textAlign: 'center'
    }}>
      <h2>Emergency Login System</h2>
      <div style={{ marginTop: '20px', fontSize: '18px' }}>
        Status: {status}
      </div>
      {error && (
        <div style={{ 
          marginTop: '20px', 
          color: 'red', 
          padding: '10px', 
          border: '1px solid red',
          borderRadius: '5px',
          maxWidth: '80%'
        }}>
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default LoginBypass;
