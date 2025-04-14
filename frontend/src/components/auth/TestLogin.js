import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const TestLogin = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loginResponse, setLoginResponse] = useState(null);
  const [userData, setUserData] = useState(null);

  // Check if already logged in
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/test-dashboard');
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setLoginResponse(null);
    setUserData(null);

    try {
      console.log('Test login with:', email, password);
      
      // Direct fetch to login endpoint
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });
      
      // Try to parse the response as JSON
      let data;
      try {
        data = await response.json();
        console.log('Login response:', data);
        setLoginResponse(data);
      } catch (jsonError) {
        console.error('Error parsing JSON response:', jsonError);
        throw new Error('Invalid response from server');
      }
      
      if (response.ok && data.access_token) {
        // Store token and redirect
        localStorage.setItem('token', data.access_token);
        console.log('Login successful, token stored');
        
        // Fetch user data to verify token works
        try {
          const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
            headers: {
              'Authorization': `Bearer ${data.access_token}`
            }
          });
          
          if (userResponse.ok) {
            const userData = await userResponse.json();
            console.log('User data fetched successfully:', userData);
            setUserData(userData);
            setTimeout(() => {
              navigate('/test-dashboard');
            }, 1000); // Short delay to show success message
          } else {
            let userError;
            try {
              userError = await userResponse.json();
            } catch (e) {
              userError = { detail: 'Could not parse error response' };
            }
            console.error('Error fetching user data:', userError);
            setError(`Login successful but couldn't fetch user data: ${typeof userError.detail === 'string' ? userError.detail : JSON.stringify(userError)}`);
            // Still keep the token
          }
        } catch (userErr) {
          console.error('Error in user data fetch:', userErr);
          setError(`Login successful but error fetching user data: ${userErr.message || 'Unknown error'}`);
          // Still keep the token
        }
      } else {
        // Handle login failure
        const errorMessage = data.detail || 'Login failed';
        setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
        // Clear any existing token
        localStorage.removeItem('token');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Login failed: ' + (err.message || 'Unknown error'));
      // Clear any existing token
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = async (testEmail, testPassword) => {
    setEmail(testEmail);
    setPassword(testPassword);
    
    // Submit the form programmatically
    const event = { preventDefault: () => {} };
    await handleSubmit(event);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Exam Planning System</h2>
        <h3 className="login-subtitle">Test Login</h3>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        {userData && (
          <div className="success-message">
            Login successful as {userData.name} ({userData.role})!
          </div>
        )}
        
        {loginResponse && !error && !userData && (
          <div className="success-message">
            Login successful! Token received.
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-input-container">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button 
                type="button" 
                className="toggle-password-button"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <div className="login-help">
          <p>Quick login with test credentials:</p>
          <div className="quick-login-buttons">
            <button 
              onClick={() => handleQuickLogin('admin@example.com', 'password')}
              className="quick-login-button admin"
              disabled={loading}
            >
              Login as Admin
            </button>
            <button 
              onClick={() => handleQuickLogin('professor@example.com', 'password')}
              className="quick-login-button professor"
              disabled={loading}
            >
              Login as Professor
            </button>
            <button 
              onClick={() => handleQuickLogin('student@example.com', 'password')}
              className="quick-login-button student"
              disabled={loading}
            >
              Login as Student
            </button>
          </div>
          <p>After login, you'll be redirected to the <a href="/test-dashboard">test dashboard</a>.</p>
        </div>
      </div>
    </div>
  );
};

export default TestLogin;
