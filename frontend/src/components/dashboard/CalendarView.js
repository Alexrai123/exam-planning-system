import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './DashboardComponents.css';
import './CalendarStyles.css';

// Setup the localizer by providing the moment object
const localizer = momentLocalizer(moment);

const CalendarView = () => {
  const { currentUser } = useAuth();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [courses, setCourses] = useState([]);
  const [date, setDate] = useState(new Date());
  const [view, setView] = useState('month');

  // Fetch courses first, then exams
  useEffect(() => {
    const fetchData = async () => {
      try {
        setError(null);
        const token = localStorage.getItem('token');
        if (!token) {
          setError('No authentication token found');
          setLoading(false);
          return;
        }

        // First fetch courses
        const coursesResponse = await axios.get('http://localhost:8000/api/v1/courses/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        setCourses(coursesResponse.data);
        
        // Then fetch exams
        const examsResponse = await axios.get('http://localhost:8000/api/v1/exams/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        // Transform exams into calendar events
        const calendarEvents = examsResponse.data.map(exam => {
          // Find the course name
          const course = coursesResponse.data.find(c => c.id === exam.course_id) || { name: `Course ${exam.course_id}` };
          
          // Create a date object from the date and time
          const examDate = new Date(`${exam.date}T${exam.time}`);
          
          // Create an end time (1 hour after start time)
          const endDate = new Date(examDate);
          endDate.setHours(endDate.getHours() + 1);
          
          return {
            id: exam.id,
            title: `${course.name} - ${exam.sala_name}`,
            start: examDate,
            end: endDate,
            resource: {
              ...exam,
              // Create virtual objects for display
              course: { name: course.name },
              sala: { name: exam.sala_name || 'N/A' },
              grupa: { name: exam.grupa_name || 'N/A' }
            }
          };
        });
        
        setEvents(calendarEvents);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load data. Please try again later.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Handle event selection
  const handleSelectEvent = (event) => {
    setSelectedEvent(event.resource);
    setShowModal(true);
  };

  // Close the modal
  const closeModal = () => {
    setShowModal(false);
    setSelectedEvent(null);
  };

  // Format date for display
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Handle calendar navigation and view changes
  const handleNavigate = (newDate) => {
    setDate(newDate);
  };

  const handleViewChange = (newView) => {
    setView(newView);
  };

  // Custom event styling based on status
  const eventStyleGetter = (event) => {
    const status = event.resource?.status || 'proposed';
    let backgroundColor;
    
    switch(status.toLowerCase()) {
      case 'proposed':
        backgroundColor = '#3498db'; // Blue
        break;
      case 'confirmed':
        backgroundColor = '#2ecc71'; // Green
        break;
      case 'cancelled':
        backgroundColor = '#e74c3c'; // Red
        break;
      case 'completed':
        backgroundColor = '#9b59b6'; // Purple
        break;
      default:
        backgroundColor = '#95a5a6'; // Gray
    }
    
    return {
      style: {
        backgroundColor,
        borderRadius: '5px',
        opacity: 0.8,
        color: 'white',
        border: '0px',
        display: 'block'
      }
    };
  };

  if (loading) {
    return <div className="loading">Loading calendar...</div>;
  }

  return (
    <div className="dashboard-component">
      <div className="component-header">
        <h2>Exam Calendar</h2>
        <p>View all scheduled exams in a calendar format</p>
        
        {/* Error message */}
        {error && <div className="error-message">{error}</div>}
      </div>
      
      <div className="calendar-container">
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 600 }}
          onSelectEvent={handleSelectEvent}
          eventPropGetter={eventStyleGetter}
          views={['month', 'week', 'day']}
          defaultView="month"
          view={view}
          onView={handleViewChange}
          date={date}
          onNavigate={handleNavigate}
        />
      </div>
      
      {/* Event Details Modal */}
      {showModal && selectedEvent && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Exam Details</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <div className="detail-row">
                <span className="detail-label">Course:</span>
                <span className="detail-value">{selectedEvent.course?.name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Date:</span>
                <span className="detail-value">{formatDate(selectedEvent.date)}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Time:</span>
                <span className="detail-value">{selectedEvent.time || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Room:</span>
                <span className="detail-value">{selectedEvent.sala?.name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Group:</span>
                <span className="detail-value">{selectedEvent.grupa?.name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Status:</span>
                <span className={`status-badge status-${(selectedEvent.status || 'proposed').toLowerCase()}`}>
                  {selectedEvent.status || 'Proposed'}
                </span>
              </div>
            </div>
            <div className="modal-footer">
              <button 
                className="action-button primary-button"
                onClick={closeModal}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CalendarView;
