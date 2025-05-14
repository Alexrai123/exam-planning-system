import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const DirectLoginTest = () => {
  const [status, setStatus] = useState('Ready to test');
  const [logs, setLogs] = useState([]);
  
  const addLog = (message) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testLogin = async () => {
    setStatus('Testing...');
    addLog('Starting login test...');
    
    try {
      // Clear any existing tokens
      localStorage.removeItem('token');
      addLog('Cleared existing tokens');
      
      // Create form data for login
      const formData = new URLSearchParams();
      formData.append('username', 'admin@usv.ro');
      formData.append('password', 'password123');
      
      addLog('Attempting direct API login with admin@usv.ro / password123');
      
      // Make direct API call with detailed logging
      try {
        const loginResponse = await axios.post(`${API_URL}/auth/login`, formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          timeout: 10000
        });
        
        addLog(`Login response status: ${loginResponse.status}`);
        addLog(`Login response data: ${JSON.stringify(loginResponse.data)}`);
        
        if (loginResponse.data && loginResponse.data.access_token) {
          localStorage.setItem('token', loginResponse.data.access_token);
          addLog('Token stored in localStorage');
          setStatus('Login successful');
          
          // Try to get user data
          try {
            addLog('Attempting to fetch user data...');
            const userResponse = await axios.get(`${API_URL}/users/me`, {
              headers: {
                'Authorization': `Bearer ${loginResponse.data.access_token}`
              }
            });
            
            addLog(`User data response: ${JSON.stringify(userResponse.data)}`);
            setStatus('Login and user data fetch successful');
          } catch (userError) {
            addLog(`Error fetching user data: ${userError.message}`);
            if (userError.response) {
              addLog(`User data error status: ${userError.response.status}`);
              addLog(`User data error details: ${JSON.stringify(userError.response.data)}`);
            }
          }
        } else {
          addLog('No token in response');
          setStatus('Login failed - No token received');
        }
      } catch (loginError) {
        addLog(`Login error: ${loginError.message}`);
        if (loginError.response) {
          addLog(`Login error status: ${loginError.response.status}`);
          addLog(`Login error details: ${JSON.stringify(loginError.response.data)}`);
        }
        setStatus('Login failed');
      }
    } catch (error) {
      addLog(`Unexpected error: ${error.message}`);
      setStatus('Test failed');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Direct Login Test</h1>
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={testLogin}
          style={{
            padding: '10px 20px',
            backgroundColor: '#4a90e2',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Test Login API
        </button>
        <span style={{ marginLeft: '20px', fontWeight: 'bold' }}>
          Status: {status}
        </span>
      </div>
      
      <div style={{ 
        border: '1px solid #ddd', 
        borderRadius: '4px',
        padding: '10px',
        height: '400px',
        overflowY: 'auto',
        backgroundColor: '#f5f5f5',
        fontFamily: 'monospace'
      }}>
        <h3>Test Logs:</h3>
        {logs.map((log, index) => (
          <div key={index} style={{ margin: '5px 0', borderBottom: '1px solid #eee' }}>
            {log}
          </div>
        ))}
        {logs.length === 0 && <div>No logs yet. Click "Test Login API" to start.</div>}
      </div>
    </div>
  );
};

export default DirectLoginTest;
