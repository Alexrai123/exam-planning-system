import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import './Dashboard.css';

// Dashboard components
import ExamsList from './dashboard/ExamsList';
import CoursesList from './dashboard/CoursesList';
import RoomsList from './dashboard/RoomsList';
import UserProfile from './dashboard/UserProfile';
import CalendarView from './dashboard/CalendarView';
import SampleDataButton from './dashboard/SampleDataButton';

const Dashboard = () => {
  const { currentUser, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState(null);
  const [stats, setStats] = useState({
    examsCount: 0,
    coursesCount: 0,
    roomsCount: 0
  });

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('No authentication token found');
          setLoading(false);
          return;
        }

        // Try to get user data if not already available
        if (!currentUser || !currentUser.name) {
          try {
            const userResponse = await axios.get('http://localhost:8000/api/v1/users/me', {
              headers: {
                Authorization: `Bearer ${token}`
              }
            });
            setUserData(userResponse.data);
          } catch (userErr) {
            console.error('Error fetching user data:', userErr);
            // Continue even if we can't get user data
            setUserData({ 
              name: 'User', 
              role: 'USER',
              email: currentUser?.email || 'user@example.com'
            });
          }
        } else {
          setUserData(currentUser);
        }

        // Fetch dashboard stats
        try {
          // Fetch exams count
          const examsResponse = await axios.get('http://localhost:8000/api/v1/exams/', {
            headers: { Authorization: `Bearer ${token}` }
          });
          
          // Fetch courses count
          const coursesResponse = await axios.get('http://localhost:8000/api/v1/courses/', {
            headers: { Authorization: `Bearer ${token}` }
          });
          
          // Fetch rooms count
          const roomsResponse = await axios.get('http://localhost:8000/api/v1/rooms/', {
            headers: { Authorization: `Bearer ${token}` }
          });
          
          setStats({
            examsCount: examsResponse.data.length || 0,
            coursesCount: coursesResponse.data.length || 0,
            roomsCount: roomsResponse.data.length || 0
          });
        } catch (statsErr) {
          console.error('Error fetching stats:', statsErr);
          // Continue even if we can't get stats
        }
      } catch (err) {
        console.error('Dashboard error:', err);
        setError('An error occurred. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [currentUser]);

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'exams':
        return <ExamsList />;
      case 'courses':
        return <CoursesList />;
      case 'rooms':
        return <RoomsList />;
      case 'profile':
        return <UserProfile userData={userData} />;
      case 'calendar':
        return <CalendarView />;
      default:
        return renderDashboardOverview();
    }
  };

  const renderDashboardOverview = () => {
    // Use userData which might come from currentUser or our direct API call
    const user = userData || currentUser || { name: 'User', role: 'USER' };
    const role = user.role || 'USER';

    return (
      <>
        <section className="welcome-section">
          <h2>Welcome to the Exam Planning System</h2>
          <p>
            This system helps you manage and schedule university exams efficiently.
            Use the navigation to access different features based on your role.
          </p>
          
          {/* Add sample data button for secretariat users */}
          {role === 'SECRETARIAT' && (
            <SampleDataButton onSuccess={() => {
              // Refresh stats after adding sample data
              fetchStats();
            }} />
          )}
        </section>

        <div className="stats-cards">
          <div className="stat-card">
            <div className="stat-icon exams-icon">
              <i className="fas fa-calendar-alt"></i>
            </div>
            <div className="stat-details">
              <h3>Exams</h3>
              <p className="stat-count">{stats.examsCount}</p>
              <p className="stat-label">Total Exams</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon courses-icon">
              <i className="fas fa-book"></i>
            </div>
            <div className="stat-details">
              <h3>Courses</h3>
              <p className="stat-count">{stats.coursesCount}</p>
              <p className="stat-label">Total Courses</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon rooms-icon">
              <i className="fas fa-door-open"></i>
            </div>
            <div className="stat-details">
              <h3>Rooms</h3>
              <p className="stat-count">{stats.roomsCount}</p>
              <p className="stat-label">Total Rooms</p>
            </div>
          </div>
        </div>

        {/* Role-specific content */}
        {role === 'SECRETARIAT' && (
          <section className="admin-actions">
            <h3>Admin Quick Actions</h3>
            <div className="admin-buttons">
              <button className="admin-button" onClick={() => setActiveTab('exams')}>
                Manage Exams
              </button>
              <button className="admin-button" onClick={() => setActiveTab('courses')}>
                Manage Courses
              </button>
              <button className="admin-button" onClick={() => setActiveTab('rooms')}>
                Manage Rooms
              </button>
            </div>
          </section>
        )}

        {role === 'PROFESSOR' && (
          <section className="professor-section">
            <h3>Professor Tools</h3>
            <div className="professor-tools">
              <button className="professor-button" onClick={() => setActiveTab('exams')}>
                View My Exams
              </button>
              <button className="professor-button" onClick={() => setActiveTab('courses')}>
                My Courses
              </button>
            </div>
          </section>
        )}

        {role === 'STUDENT' && (
          <section className="student-section">
            <h3>Student Information</h3>
            <div className="student-info">
              <button className="student-button" onClick={() => setActiveTab('exams')}>
                My Exam Schedule
              </button>
            </div>
          </section>
        )}
      </>
    );
  };

  // Add a function to fetch stats
  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }

      // Fetch exams count
      const examsResponse = await axios.get('http://localhost:8000/api/v1/exams/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Fetch courses count
      const coursesResponse = await axios.get('http://localhost:8000/api/v1/courses/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Fetch rooms count
      const roomsResponse = await axios.get('http://localhost:8000/api/v1/rooms/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setStats({
        examsCount: examsResponse.data.length || 0,
        coursesCount: coursesResponse.data.length || 0,
        roomsCount: roomsResponse.data.length || 0
      });
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  // Use userData which might come from currentUser or our direct API call
  const user = userData || currentUser || { name: 'User', role: 'USER' };

  return (
    <div className="dashboard-container">
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <h2>Exam Planning</h2>
        </div>
        <nav className="sidebar-nav">
          <ul>
            <li className={activeTab === 'dashboard' ? 'active' : ''}>
              <button onClick={() => setActiveTab('dashboard')}>
                <i className="fas fa-home"></i> Dashboard
              </button>
            </li>
            <li className={activeTab === 'exams' ? 'active' : ''}>
              <button onClick={() => setActiveTab('exams')}>
                <i className="fas fa-calendar-alt"></i> Exams
              </button>
            </li>
            <li className={activeTab === 'calendar' ? 'active' : ''}>
              <button onClick={() => setActiveTab('calendar')}>
                <i className="fas fa-calendar"></i> Calendar
              </button>
            </li>
            <li className={activeTab === 'courses' ? 'active' : ''}>
              <button onClick={() => setActiveTab('courses')}>
                <i className="fas fa-book"></i> Courses
              </button>
            </li>
            <li className={activeTab === 'rooms' ? 'active' : ''}>
              <button onClick={() => setActiveTab('rooms')}>
                <i className="fas fa-door-open"></i> Rooms
              </button>
            </li>
            <li className={activeTab === 'profile' ? 'active' : ''}>
              <button onClick={() => setActiveTab('profile')}>
                <i className="fas fa-user"></i> Profile
              </button>
            </li>
          </ul>
        </nav>
        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-button">
            <i className="fas fa-sign-out-alt"></i> Logout
          </button>
        </div>
      </aside>

      <main className="dashboard-main">
        <header className="dashboard-header">
          <div className="header-title">
            <h1>{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</h1>
          </div>
          <div className="user-info">
            <span>Welcome, {user.name || 'User'}</span>
            <span className="role-badge">{user.role || 'USER'}</span>
          </div>
        </header>

        <div className="dashboard-content">
          {error ? (
            <div className="error-message">{error}</div>
          ) : (
            renderTabContent()
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
