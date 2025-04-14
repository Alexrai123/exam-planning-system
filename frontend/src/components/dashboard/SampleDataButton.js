import React, { useState } from 'react';
import axios from 'axios';
import './DashboardComponents.css';

const SampleDataButton = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  // Sample courses data
  const sampleCourses = [
    {
      name: 'Introduction to Computer Science',
      description: 'Fundamentals of computer science, including algorithms, data structures, and programming concepts.',
      credits: 6,
      year: 1,
      semester: 1
    },
    {
      name: 'Database Systems',
      description: 'Design and implementation of database systems, SQL, normalization, and transaction management.',
      credits: 5,
      year: 2,
      semester: 1
    },
    {
      name: 'Web Development',
      description: 'Frontend and backend web development technologies, including HTML, CSS, JavaScript, and frameworks.',
      credits: 5,
      year: 2,
      semester: 2
    },
    {
      name: 'Artificial Intelligence',
      description: 'Introduction to AI concepts, machine learning algorithms, and neural networks.',
      credits: 6,
      year: 3,
      semester: 1
    },
    {
      name: 'Software Engineering',
      description: 'Software development methodologies, project management, and quality assurance.',
      credits: 5,
      year: 3,
      semester: 2
    }
  ];

  // Sample rooms data
  const sampleRooms = [
    {
      name: 'A101',
      building: 'Building A',
      floor: 1,
      capacity: 120
    },
    {
      name: 'B203',
      building: 'Building B',
      floor: 2,
      capacity: 80
    },
    {
      name: 'C305',
      building: 'Building C',
      floor: 3,
      capacity: 60
    },
    {
      name: 'D102',
      building: 'Building D',
      floor: 1,
      capacity: 100
    },
    {
      name: 'E201',
      building: 'Building E',
      floor: 2,
      capacity: 50
    }
  ];

  // Sample groups data
  const sampleGroups = [
    {
      name: '1A',
      year: 1,
      specialization: 'Computer Science',
      setGrupa_id: null
    },
    {
      name: '2B',
      year: 2,
      specialization: 'Software Engineering',
      setGrupa_id: null
    },
    {
      name: '3C',
      year: 3,
      specialization: 'Cybersecurity',
      setGrupa_id: null
    },
    {
      name: '2A',
      year: 2,
      specialization: 'Data Science',
      setGrupa_id: null
    },
    {
      name: '3A',
      year: 3,
      specialization: 'Artificial Intelligence',
      setGrupa_id: null
    }
  ];

  const handleAddSampleData = async () => {
    setLoading(true);
    setMessage(null);
    
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setMessage({
          type: 'error',
          text: 'No authentication token found. Please log in again.'
        });
        setLoading(false);
        return;
      }

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      const API_URL = 'http://localhost:8000/api/v1';
      
      // First, get the current user's ID (for professor_id in courses)
      let userId;
      try {
        const userResponse = await axios.get(`${API_URL}/users/me`, { headers });
        userId = userResponse.data.id;
        console.log('Current user ID:', userId);
      } catch (err) {
        console.error('Failed to get current user ID:', err.response?.data || err.message);
        setMessage({
          type: 'error',
          text: 'Failed to get user information. Please try again.'
        });
        setLoading(false);
        return;
      }
      
      // Add courses with professor_id
      const addedCourses = [];
      for (const course of sampleCourses) {
        try {
          // Add the professor_id to the course data
          const courseWithProfessor = {
            ...course,
            profesor_id: userId
          };
          
          const response = await axios.post(`${API_URL}/courses/`, courseWithProfessor, { headers });
          addedCourses.push(response.data);
          console.log(`Added course: ${course.name}`);
        } catch (err) {
          console.error(`Failed to add course ${course.name}:`, err.response?.data || err.message);
          // Continue with other courses even if one fails
        }
      }
      
      // Add rooms
      const addedRooms = [];
      for (const room of sampleRooms) {
        try {
          const response = await axios.post(`${API_URL}/rooms/`, room, { headers });
          addedRooms.push(response.data);
          console.log(`Added room: ${room.name}`);
        } catch (err) {
          console.error(`Failed to add room ${room.name}:`, err.response?.data || err.message);
          // Continue with other rooms even if one fails
        }
      }
      
      // Add groups
      const addedGroups = [];
      for (const group of sampleGroups) {
        try {
          const response = await axios.post(`${API_URL}/groups/`, group, { headers });
          addedGroups.push(response.data);
          console.log(`Added group: ${group.name}`);
        } catch (err) {
          console.error(`Failed to add group ${group.name}:`, err.response?.data || err.message);
          // Continue with other groups even if one fails
        }
      }
      
      // Create exams using the added entities
      if (addedCourses.length > 0 && addedRooms.length > 0 && addedGroups.length > 0) {
        const today = new Date();
        
        // Create sample exams
        const exams = [
          {
            date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7).toISOString().split('T')[0],
            time: '09:00:00',
            course_id: addedCourses[0].id,
            sala_id: addedRooms[0].id,
            grupa_id: addedGroups[0].id,
            status: 'proposed'
          },
          {
            date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 8).toISOString().split('T')[0],
            time: '11:00:00',
            course_id: addedCourses[1].id,
            sala_id: addedRooms[1].id,
            grupa_id: addedGroups[1].id,
            status: 'confirmed'
          },
          {
            date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 9).toISOString().split('T')[0],
            time: '14:00:00',
            course_id: addedCourses[2].id,
            sala_id: addedRooms[2].id,
            grupa_id: addedGroups[2].id,
            status: 'proposed'
          },
          {
            date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 10).toISOString().split('T')[0],
            time: '10:00:00',
            course_id: addedCourses[3].id,
            sala_id: addedRooms[3].id,
            grupa_id: addedGroups[3].id,
            status: 'confirmed'
          },
          {
            date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 11).toISOString().split('T')[0],
            time: '13:00:00',
            course_id: addedCourses[4].id,
            sala_id: addedRooms[4].id,
            grupa_id: addedGroups[4].id,
            status: 'proposed'
          }
        ];
        
        // Add exams
        for (const exam of exams) {
          try {
            await axios.post(`${API_URL}/exams/`, exam, { headers });
            console.log(`Added exam for course ID: ${exam.course_id}`);
          } catch (err) {
            console.error(`Failed to add exam:`, err.response?.data || err.message);
            // Continue with other exams even if one fails
          }
        }
      }
      
      setMessage({
        type: 'success',
        text: 'Sample data added successfully!'
      });
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      console.error('Error adding sample data:', error);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Failed to add sample data'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sample-data-container">
      <button 
        className="sample-data-button"
        onClick={handleAddSampleData}
        disabled={loading}
      >
        {loading ? 'Adding Sample Data...' : 'Add Sample Data'}
      </button>
      
      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default SampleDataButton;
