import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import './DashboardComponents.css';

const CoursesDebug = () => {
  const { currentUser } = useAuth();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [logs, setLogs] = useState([]);

  const addLog = (message) => {
    setLogs(prevLogs => [...prevLogs, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      addLog('Starting to fetch courses...');
      
      const token = localStorage.getItem('token');
      if (!token) {
        const errorMsg = 'No authentication token found';
        setError(errorMsg);
        addLog(errorMsg);
        setLoading(false);
        return;
      }

      addLog(`Using token: ${token.substring(0, 10)}...`);
      
      const response = await axios.get('http://localhost:8000/api/v1/courses/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      addLog(`Received response with status: ${response.status}`);
      addLog(`Received ${response.data.length} courses`);
      
      if (response.data.length > 0) {
        addLog(`First course: ID=${response.data[0].id}, Name=${response.data[0].name}`);
      }
      
      setCourses(response.data);
      setLoading(false);
    } catch (err) {
      const errorMsg = `Error fetching courses: ${err.message}`;
      if (err.response) {
        addLog(`Error response: ${err.response.status} - ${JSON.stringify(err.response.data)}`);
      } else {
        addLog(errorMsg);
      }
      setError(errorMsg);
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-component">
      <h2>Courses Debug</h2>
      
      <div className="debug-section">
        <h3>Debug Logs</h3>
        <div className="debug-logs">
          {logs.map((log, index) => (
            <div key={index} className="log-entry">{log}</div>
          ))}
        </div>
      </div>
      
      <div className="debug-section">
        <h3>Courses Data</h3>
        {loading ? (
          <p>Loading courses...</p>
        ) : error ? (
          <p className="error-message">{error}</p>
        ) : (
          <>
            <p>Total courses: {courses.length}</p>
            <div className="courses-list">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Professor</th>
                    <th>Faculty ID</th>
                  </tr>
                </thead>
                <tbody>
                  {courses.map(course => (
                    <tr key={course.id}>
                      <td>{course.id}</td>
                      <td>{course.name}</td>
                      <td>{course.profesor_name}</td>
                      <td>{course.faculty_id || 'None'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
      
      <div className="debug-section">
        <h3>Test Course Selection</h3>
        <div className="form-group">
          <label htmlFor="test_course_id">Course</label>
          <select
            id="test_course_id"
            name="test_course_id"
          >
            <option value="">Select a course</option>
            {courses.map(course => (
              <option key={course.id} value={course.id}>{course.name}</option>
            ))}
          </select>
        </div>
      </div>
      
      <button 
        className="action-button" 
        onClick={fetchCourses} 
        disabled={loading}
      >
        Refresh Courses
      </button>
    </div>
  );
};

export default CoursesDebug;
