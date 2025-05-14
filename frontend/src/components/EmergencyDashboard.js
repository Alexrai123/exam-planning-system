import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const EmergencyDashboard = () => {
  const [userData, setUserData] = useState(null);
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get user data from localStorage
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          setUserData(JSON.parse(storedUser));
        } else {
          // Try to fetch user data from API
          const token = localStorage.getItem('token');
          if (token) {
            const userResponse = await axios.get(`${API_URL}/users/me`, {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });
            setUserData(userResponse.data);
            localStorage.setItem('user', JSON.stringify(userResponse.data));
          }
        }

        // Fetch exams
        const token = localStorage.getItem('token');
        if (token) {
          const examsResponse = await axios.get(`${API_URL}/exams`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          setExams(examsResponse.data);
        }
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/emergency-login';
  };

  if (loading) {
    return (
      <div className="emergency-dashboard loading">
        <h2>Loading...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="emergency-dashboard error">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={handleLogout}>Go Back to Login</button>
      </div>
    );
  }

  return (
    <div className="emergency-dashboard">
      <header>
        <h1>Emergency Dashboard</h1>
        <div className="user-info">
          {userData && (
            <>
              <span>Welcome, {userData.name} ({userData.role})</span>
              <button onClick={handleLogout}>Logout</button>
            </>
          )}
        </div>
      </header>

      <main>
        <section className="dashboard-section">
          <h2>Exams</h2>
          {exams.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Course</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Room</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {exams.map((exam) => (
                  <tr key={exam.id}>
                    <td>{exam.course?.name || 'N/A'}</td>
                    <td>{new Date(exam.date).toLocaleDateString()}</td>
                    <td>{exam.start_time} - {exam.end_time}</td>
                    <td>{exam.room?.name || 'N/A'}</td>
                    <td>{exam.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No exams found.</p>
          )}
        </section>
      </main>

      <footer>
        <p>This is an emergency dashboard to bypass authentication issues.</p>
        <p>
          <Link to="/emergency-login">Return to Emergency Login</Link>
        </p>
      </footer>

      <style jsx>{`
        .emergency-dashboard {
          font-family: Arial, sans-serif;
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
        }
        
        header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 30px;
          padding-bottom: 10px;
          border-bottom: 1px solid #eee;
        }
        
        .user-info {
          display: flex;
          align-items: center;
          gap: 15px;
        }
        
        button {
          padding: 8px 15px;
          background-color: #4a90e2;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        
        button:hover {
          background-color: #3a80d2;
        }
        
        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
        }
        
        th, td {
          padding: 12px 15px;
          text-align: left;
          border-bottom: 1px solid #ddd;
        }
        
        th {
          background-color: #f8f9fa;
        }
        
        tr:hover {
          background-color: #f5f5f5;
        }
        
        footer {
          margin-top: 50px;
          padding-top: 20px;
          border-top: 1px solid #eee;
          text-align: center;
          color: #666;
        }
      `}</style>
    </div>
  );
};

export default EmergencyDashboard;
