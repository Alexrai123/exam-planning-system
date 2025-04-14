import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const SimpleTestDashboard = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tokenInfo, setTokenInfo] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('No authentication token found');
          setLoading(false);
          return;
        }

        // Store token info for debugging
        try {
          // Parse JWT token (without verification)
          const tokenParts = token.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            setTokenInfo({
              subject: payload.sub,
              expires: new Date(payload.exp * 1000).toLocaleString(),
              issuedAt: new Date(payload.iat * 1000).toLocaleString()
            });
          }
        } catch (tokenErr) {
          console.error('Error parsing token:', tokenErr);
        }

        // Try to get user data
        try {
          console.log('Fetching user data with token:', token);
          const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (!userResponse.ok) {
            const errorData = await userResponse.json().catch(() => ({}));
            throw new Error(`Failed to fetch user: ${userResponse.status} - ${errorData.detail || 'Unknown error'}`);
          }
          
          const userData = await userResponse.json();
          console.log('User data:', userData);
          setUserData(userData);
        } catch (userErr) {
          console.error('Error fetching user data:', userErr);
          setError('Failed to load user data: ' + userErr.message);
        }
      } catch (err) {
        console.error('Dashboard error:', err);
        setError('An error occurred: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/test-login');
  };

  const handleTryAgain = () => {
    setLoading(true);
    setError(null);
    window.location.reload();
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Authentication Error</h2>
        <p>{error}</p>
        {tokenInfo && (
          <div className="token-info">
            <h3>Token Information</h3>
            <p>Subject (email): {tokenInfo.subject}</p>
            <p>Expires: {tokenInfo.expires}</p>
            <p>Issued: {tokenInfo.issuedAt}</p>
          </div>
        )}
        <div className="error-actions">
          <button onClick={handleTryAgain} className="retry-button">Try Again</button>
          <button onClick={handleLogout} className="logout-button">Back to Login</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Exam Planning System</h1>
        <div className="user-info">
          <span>Welcome, {userData?.name || userData?.email || 'User'}</span>
          <span className="role-badge">{userData?.role || 'USER'}</span>
          <button onClick={handleLogout} className="logout-button">Logout</button>
        </div>
      </header>

      <main className="dashboard-content">
        <section className="welcome-section">
          <h2>Test Dashboard</h2>
          <p>
            This is a simplified test dashboard to verify authentication is working.
          </p>
          <div className="user-data-display">
            <h3>Your User Data:</h3>
            <pre>{JSON.stringify(userData, null, 2)}</pre>
            
            {tokenInfo && (
              <div className="token-info">
                <h3>Token Information</h3>
                <p>Subject (email): {tokenInfo.subject}</p>
                <p>Expires: {tokenInfo.expires}</p>
                <p>Issued: {tokenInfo.issuedAt}</p>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="dashboard-footer">
        <p>&copy; {new Date().getFullYear()} Exam Planning System</p>
      </footer>
    </div>
  );
};

export default SimpleTestDashboard;
