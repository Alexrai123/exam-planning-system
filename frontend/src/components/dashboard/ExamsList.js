import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import './DashboardComponents.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEdit, faTrash, faSave, faPlus, faFileExcel, faDownload, faFilePdf } from '@fortawesome/free-solid-svg-icons';

const ExamsList = () => {
  const { currentUser } = useAuth();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [selectedExam, setSelectedExam] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [courses, setCourses] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [professors, setProfessors] = useState([]);
  const [groups, setGroups] = useState([]);
  const [faculties, setFaculties] = useState([]);
  const [selectedFaculty, setSelectedFaculty] = useState('');
  const [filteredCourses, setFilteredCourses] = useState([]);
  
  // Form state for create/edit
  const [formData, setFormData] = useState({
    date: '',
    time: '',
    course_id: '',
    sala_name: '',
    grupa_name: '',
    status: 'proposed'
  });

  const fetchExams = async () => {
    try {
      setError(null);
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://localhost:8000/api/v1/exams/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      // Debug: Log the exam data
      console.log('Exams data from API:', response.data);
      
      // Process the exam data to ensure all properties are valid
      const processedExams = response.data.map(exam => {
        // Debug: Log each exam's professor_agreement value
        console.log(`Exam ID ${exam.id}: professor_agreement = ${exam.professor_agreement}, status = ${exam.status}`);
        
        // For confirmed exams, ensure professor_agreement is true
        const isProfessorAgreement = exam.status === 'CONFIRMED' || exam.professor_agreement;
        
        return {
          id: exam.id,
          date: exam.date || '',
          time: exam.time || '',
          course_id: exam.course_id || '',
          sala_name: exam.sala_name || '',
          grupa_name: exam.grupa_name || '',
          status: exam.status || 'proposed',
          professor_agreement: isProfessorAgreement, // Ensure professor_agreement is included
          // Create virtual objects for display purposes
          course: { name: `Course ${exam.course_id}` },
          sala: { name: exam.sala_name || 'N/A' },
          grupa: { name: exam.grupa_name || 'N/A' }
        };
      });
      
      console.log('Processed exams:', processedExams);
      
      // If user is a professor, filter exams to only show those related to their courses
      if (currentUser && currentUser.role === 'PROFESSOR') {
        console.log('Filtering exams for professor:', currentUser.name);
        
        // First, fetch the professor's courses
        const coursesResponse = await axios.get('http://localhost:8000/api/v1/courses/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        // Filter courses to only include those taught by this professor
        const professorCourses = coursesResponse.data.filter(course => 
          course.profesor_name === currentUser.name
        );
        
        console.log('Professor courses:', professorCourses);
        
        // Get the course IDs taught by this professor
        const professorCourseIds = professorCourses.map(course => course.id);
        
        // Filter exams to only include those for the professor's courses
        const filteredExams = processedExams.filter(exam => 
          professorCourseIds.includes(exam.course_id)
        );
        
        console.log('Filtered exams for professor:', filteredExams);
        setExams(filteredExams);
      } else {
        // For non-professors (secretariat, students), show all exams
        setExams(processedExams);
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching exams:', err);
      setError('Failed to load exams. Please try again later.');
      setLoading(false);
    }
  };

  const fetchRelatedData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Fetch courses
      try {
        console.log('Fetching courses...');
        const coursesResponse = await axios.get('http://localhost:8000/api/v1/courses/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log('Courses response:', coursesResponse);
        
        if (coursesResponse.data && Array.isArray(coursesResponse.data)) {
          console.log(`Received ${coursesResponse.data.length} courses`);
          setCourses(coursesResponse.data);
          setFilteredCourses(coursesResponse.data);
        } else {
          console.error('Invalid courses data format:', coursesResponse.data);
          setCourses([]);
          setFilteredCourses([]);
        }
      } catch (courseErr) {
        console.error('Error fetching courses:', courseErr);
        setCourses([]);
        setFilteredCourses([]);
      }

      // Fetch rooms
      try {
        const roomsResponse = await axios.get('http://localhost:8000/api/v1/rooms/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log(`Received ${roomsResponse.data.length} rooms`);
        setRooms(roomsResponse.data);
      } catch (roomErr) {
        console.error('Error fetching rooms:', roomErr);
        setRooms([]);
      }

      // Fetch professors
      try {
        const professorsResponse = await axios.get('http://localhost:8000/api/v1/professors/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log(`Received ${professorsResponse.data.length} professors`);
        setProfessors(professorsResponse.data);
      } catch (profErr) {
        console.error('Error fetching professors:', profErr);
        setProfessors([]);
      }

      // Fetch groups
      try {
        const groupsResponse = await axios.get('http://localhost:8000/api/v1/groups/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log(`Received ${groupsResponse.data.length} groups`);
        setGroups(groupsResponse.data);
      } catch (groupErr) {
        console.error('Error fetching groups:', groupErr);
        setGroups([]);
      }
      
      // Fetch faculties
      try {
        const facultiesResponse = await axios.get('http://localhost:8000/api/v1/faculties/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log(`Received ${facultiesResponse.data.length} faculties`);
        setFaculties(facultiesResponse.data);
      } catch (facErr) {
        console.error('Error fetching faculties:', facErr);
        setFaculties([]);
      }
    } catch (err) {
      console.error('Error fetching related data:', err);
    }
  };

  useEffect(() => {
    fetchExams();
    fetchRelatedData();
  }, []);

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const safeGetString = (value, defaultValue = '') => {
    if (typeof value === 'string') return value;
    if (value === null || value === undefined) return defaultValue;
    return String(value);
  };

  const safeGetNumber = (value, defaultValue = null) => {
    if (typeof value === 'number') return value;
    if (value === null || value === undefined) return defaultValue;
    const parsed = parseInt(value, 10);
    return isNaN(parsed) ? defaultValue : parsed;
  };

  const formatDateForInput = (dateString) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return ''; // Invalid date
      return date.toISOString().split('T')[0];
    } catch (e) {
      console.error('Error formatting date:', e);
      return '';
    }
  };

  const handleViewExam = (exam) => {
    setSelectedExam(exam);
    setShowModal(true);
  };

  const handleEditExam = (exam) => {
    console.log('Opening edit modal for exam:', exam);
    
    // Store only the ID of the selected exam
    setSelectedExam({ id: exam.id });
    
    // Create a completely new form data object with primitive values only
    const newFormData = {
      date: typeof exam.date === 'string' ? exam.date.split('T')[0] : '',
      time: typeof exam.time === 'string' ? exam.time : '',
      course_id: typeof exam.course_id === 'number' ? String(exam.course_id) : '',
      sala_name: typeof exam.sala_name === 'string' ? exam.sala_name : '',
      grupa_name: typeof exam.grupa_name === 'string' ? exam.grupa_name : '',
      status: typeof exam.status === 'string' ? exam.status : 'proposed'
    };
    
    console.log('Setting form data:', newFormData);
    
    // Set the form data
    setFormData(newFormData);
    
    setShowEditModal(true);
  };

  const handleDeleteExam = (examId) => {
    // Only store the ID, not the entire exam object
    setSelectedExam({ id: examId });
    setShowDeleteModal(true);
  };

  const handleStatusChange = (exam) => {
    if (currentUser.role !== 'SECRETARIAT') {
      return; // Only secretariat can change status
    }
    
    setSelectedExam(exam);
    setFormData({
      ...formData,
      status: exam.status || 'PROPOSED'
    });
    setShowStatusModal(true);
  };

  // Removed publication functionality
  // const handlePublishExam = async (examId) => {
  //   if (currentUser.role !== 'SECRETARIAT') {
  //     return; // Only secretariat can publish exams
  //   }

  //   try {
  //     const token = localStorage.getItem('token');
  //     if (!token) {
  //       setError('No authentication token found');
  //       return;
  //     }

  //     // Set the publication date to current date and time
  //     const updateData = {
  //       publication_date: new Date().toISOString()
  //     };

  //     await axios.put(`http://localhost:8000/api/v1/exams/${examId}`, updateData, {
  //       headers: {
  //         'Authorization': `Bearer ${token}`,
  //         'Content-Type': 'application/json'
  //       }
  //     });

  //     setSuccess('Exam published successfully');
  //     fetchExams(); // Refresh the exams list

  //     // Clear success message after 3 seconds
  //     setTimeout(() => {
  //       setSuccess(null);
  //     }, 3000);
  //   } catch (err) {
  //     console.error('Error publishing exam:', err);
  //     setError(err.response?.data?.detail || 'Failed to publish exam. Please try again.');
  //   }
  // };

  const handleProfessorAgreement = async (examId, agreementStatus) => {
    if (currentUser.role !== 'PROFESSOR') {
      return; // Only professors can set agreement
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Update the professor agreement status
      const updateData = {
        professor_agreement: agreementStatus
      };

      await axios.put(`http://localhost:8000/api/v1/exams/${examId}`, updateData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      setSuccess(`Professor agreement ${agreementStatus ? 'confirmed' : 'withdrawn'}`);
      fetchExams(); // Refresh the exams list

      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error updating professor agreement:', err);
      setError(err.response?.data?.detail || 'Failed to update agreement status. Please try again.');
    }
  };

  const handleExportExcel = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Set loading state
      setLoading(true);
      
      // Make API request to get Excel file
      const response = await axios.get('http://localhost:8000/api/v1/exams/export/excel', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob' // Important: This tells axios to process the response as a binary blob
      });
      
      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]));
      
      // Create a temporary link element
      const link = document.createElement('a');
      link.href = url;
      
      // Set the file name from the Content-Disposition header if available
      // or use a default name
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'exam_schedule.xlsx';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/i);
        if (filenameMatch.length === 2) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      
      // Append the link to the body
      document.body.appendChild(link);
      
      // Trigger the download
      link.click();
      
      // Clean up: remove the link
      document.body.removeChild(link);
      
      // Show success message
      setSuccess('Excel file downloaded successfully');
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error exporting Excel file:', err);
      setError('Failed to export Excel file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPdf = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Set loading state
      setLoading(true);
      
      // Make API request to get PDF file
      const response = await axios.get('http://localhost:8000/api/v1/exams/export/pdf', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob' // Important: This tells axios to process the response as a binary blob
      });
      
      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]));
      
      // Create a temporary link element
      const link = document.createElement('a');
      link.href = url;
      
      // Set the file name from the Content-Disposition header if available
      // or use a default name
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'exam_schedule.pdf';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/i);
        if (filenameMatch && filenameMatch.length === 2) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      
      // Append the link to the body
      document.body.appendChild(link);
      
      // Trigger the download
      link.click();
      
      // Clean up: remove the link
      document.body.removeChild(link);
      
      // Show success message
      setSuccess('PDF file downloaded successfully');
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error exporting PDF file:', err);
      setError('Failed to export PDF file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateExam = () => {
    setFormData({
      date: '',
      time: '',
      course_id: '',
      sala_name: '',
      grupa_name: '',
      status: 'proposed'
    });
    setShowCreateModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setShowDeleteModal(false);
    setShowEditModal(false);
    setShowCreateModal(false);
    setShowStatusModal(false);
    setSelectedExam(null);
    setError(null);
    setSuccess(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleFacultyChange = (e) => {
    const facultyId = e.target.value;
    setSelectedFaculty(facultyId);
    
    if (facultyId) {
      // Filter courses by faculty, but also include courses with no faculty assigned
      console.log('Filtering courses for faculty:', facultyId);
      console.log('Total courses before filtering:', courses.length);
      
      const filtered = courses.filter(course => 
        course.faculty_id === facultyId || 
        !course.faculty_id || 
        course.faculty_id === null || 
        course.faculty_id === ''
      );
      
      console.log('Filtered courses count:', filtered.length);
      setFilteredCourses(filtered);
      
      // Reset course selection if the current selection is not in the filtered list
      const courseExists = filtered.some(course => course.id.toString() === formData.course_id);
      if (!courseExists) {
        setFormData({
          ...formData,
          course_id: ''
        });
      }
    } else {
      // If no faculty is selected, show all courses
      setFilteredCourses(courses);
    }
  };

  const confirmDelete = async () => {
    try {
      if (!selectedExam || !selectedExam.id) {
        setError('No exam selected for deletion');
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      await axios.delete(`http://localhost:8000/api/v1/exams/${selectedExam.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setSuccess('Exam deleted successfully');
      setShowDeleteModal(false);
      
      // Refresh exams list
      fetchExams();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error deleting exam:', err);
      if (err.response) {
        console.error('Error response:', err.response.status, err.response.data);
      } else if (err.request) {
        console.error('Error request:', err.request);
      } else {
        console.error('Error message:', err.message);
      }
      setError(err.response?.data?.detail || 'Failed to delete exam. Please try again.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Create a clean data object with explicit type conversions
      const examData = {};
      
      // Only add properties that have valid values
      if (formData.date) examData.date = formData.date;
      if (formData.time) examData.time = formData.time;
      if (formData.course_id) examData.course_id = parseInt(formData.course_id, 10);
      if (formData.sala_name) examData.sala_name = formData.sala_name;
      if (formData.grupa_name) examData.grupa_name = formData.grupa_name;
      if (formData.status) examData.status = formData.status;

      console.log('Submitting exam data:', examData);

      let response;
      
      if (showEditModal && selectedExam && selectedExam.id) {
        // Update existing exam
        response = await axios.put(`http://localhost:8000/api/v1/exams/${selectedExam.id}`, examData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        console.log('Update response:', response.data);
        setSuccess('Exam updated successfully');
      } else {
        // Create new exam
        response = await axios.post('http://localhost:8000/api/v1/exams/', examData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log('Create response:', response.data);
        setSuccess('Exam created successfully');
      }

      // Close modal and refresh exams list
      closeModal();
      fetchExams();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error saving exam:', err);
      if (err.response) {
        console.error('Error response:', err.response.status, err.response.data);
      } else if (err.request) {
        console.error('Error request:', err.request);
      } else {
        console.error('Error message:', err.message);
      }
      setError(err.response?.data?.detail || 'Failed to save exam. Please check your input and try again.');
    }
  };

  const handleSimpleUpdate = async (examId, newStatus) => {
    try {
      setError(null);
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Simple data object with just the status
      const statusData = {
        status: newStatus
      };

      console.log(`Updating exam ${examId} status to ${newStatus}`);

      // Make the API call
      const response = await axios.patch(
        `http://localhost:8000/api/v1/exams/${examId}/status`, 
        statusData, 
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log('Status update response:', response.data);
      setSuccess(`Exam status updated to ${newStatus}`);
      
      // Refresh exams list
      fetchExams();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error updating exam status:', err);
      setError(err.response?.data?.detail || 'Failed to update exam status. Please try again.');
    }
  };

  const updateExamStatus = async () => {
    try {
      if (!selectedExam || !selectedExam.id) {
        console.error('No exam selected or missing exam ID');
        setError('No exam selected. Please try again.');
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      console.log('Updating exam status:', selectedExam.id, 'to', formData.status);
      
      // The backend expects the enum value as defined in ExamStatus
      const examData = {
        status: formData.status
      };

      console.log('Sending data:', examData);

      const response = await axios.patch(
        `http://localhost:8000/api/v1/exams/${selectedExam.id}/status`, 
        examData, 
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log('Status update response:', response.data);
      
      setSuccess(`Exam status updated to ${formData.status}`);
      
      // Close modal and refresh exams list
      closeModal();
      fetchExams();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error updating exam status:', err);
      if (err.response) {
        console.error('Error response:', err.response.status, err.response.data);
      } else if (err.request) {
        console.error('Error request:', err.request);
      } else {
        console.error('Error message:', err.message);
      }
      setError(err.response?.data?.detail || 'Failed to update exam status. Please try again.');
    }
  };

  // Check if user has admin/secretariat role
  const isAdmin = currentUser && currentUser.role === 'SECRETARIAT';
  const isProfessor = currentUser && currentUser.role === 'PROFESSOR';
  const canEdit = isAdmin || isProfessor;

  if (loading) {
    return <div className="loading">Loading exams...</div>;
  }

  return (
    <div className="dashboard-component">
      <div className="component-header">
        <h2>Exams List</h2>
        <p>View all scheduled exams and their details</p>
        
        {/* Success message */}
        {success && <div className="success-message">{success}</div>}
        {/* Error message */}
        {error && <div className="error-message">{error}</div>}
        
        {/* Action buttons for secretariat */}
        {isAdmin && (
          <div className="action-bar">
            <button 
              className="action-button create-button"
              onClick={handleCreateExam}
            >
              <FontAwesomeIcon icon={faPlus} /> Create New Exam
            </button>
            <button 
              className="action-button export-button"
              onClick={handleExportExcel}
              disabled={loading}
            >
              <FontAwesomeIcon icon={faFileExcel} /> Export to Excel
            </button>
            <button 
              className="action-button pdf-button"
              onClick={handleExportPdf}
              disabled={loading}
            >
              <FontAwesomeIcon icon={faFilePdf} /> Export to PDF
            </button>
          </div>
        )}
        
        {/* Export button for professors */}
        {isProfessor && (
          <div className="action-bar">
            <button 
              className="action-button export-button"
              onClick={handleExportExcel}
              disabled={loading}
            >
              <FontAwesomeIcon icon={faFileExcel} /> Download Excel
            </button>
            <button 
              className="action-button pdf-button"
              onClick={handleExportPdf}
              disabled={loading}
            >
              <FontAwesomeIcon icon={faFilePdf} /> Download PDF
            </button>
          </div>
        )}
      </div>

      {exams.length === 0 ? (
        <div className="no-data">No exams scheduled at this time.</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Time</th>
                <th>Course</th>
                <th>Room</th>
                <th>Status</th>
                <th>Professor Agreement</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {exams.map((exam) => (
                <tr key={exam.id}>
                  <td>{exam.id}</td>
                  <td>{formatDate(exam.date)}</td>
                  <td>{exam.time || 'N/A'}</td>
                  <td>{exam.course?.name || 'N/A'}</td>
                  <td>{exam.sala?.name || 'N/A'}</td>
                  <td>
                    <span 
                      className={`status-badge status-${(exam.status || 'proposed').toLowerCase()}`}
                      style={{ cursor: currentUser.role === 'secretariat' ? 'pointer' : 'default' }}
                      onClick={() => currentUser.role === 'secretariat' ? handleStatusChange(exam) : null}
                    >
                      {exam.status 
                        ? exam.status.charAt(0).toUpperCase() + exam.status.slice(1).toLowerCase() 
                        : 'Proposed'}
                    </span>
                  </td>
                  {/* Publication date column removed */}
                  <td>
                    {isProfessor 
                      ? <input 
                          type="checkbox" 
                          checked={exam.status.includes('CONFIRMED') || exam.professor_agreement} 
                          onChange={() => handleProfessorAgreement(exam.id, !exam.professor_agreement)}
                          disabled={currentUser.role !== 'PROFESSOR' || exam.status.includes('CONFIRMED')}
                        />
                      : (exam.status.includes('CONFIRMED') || exam.professor_agreement) ? 'Yes' : 'No'
                    }
                  </td>
                  <td className="actions-cell">
                    <button 
                      className="action-button view-button"
                      onClick={() => handleViewExam(exam)}
                      title="View details"
                    >
                      <FontAwesomeIcon icon={faEye} />
                    </button>
                    
                    {canEdit && (
                      <>
                        <button 
                          className="action-button delete-button"
                          onClick={() => handleDeleteExam(exam.id)}
                          title="Delete exam"
                        >
                          <FontAwesomeIcon icon={faTrash} />
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Exam Details Modal */}
      {showModal && selectedExam && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Exam Details</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <div className="detail-row">
                <span className="detail-label">ID:</span>
                <span className="detail-value">{selectedExam.id}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Date:</span>
                <span className="detail-value">{formatDate(selectedExam.date)}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Time:</span>
                <span className="detail-value">{selectedExam.time}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Course:</span>
                <span className="detail-value">{selectedExam.course?.name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Room:</span>
                <span className="detail-value">{selectedExam.sala?.name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Status:</span>
                <span className="detail-value">
                  <span className={`status-badge status-${selectedExam.status?.toLowerCase() || 'proposed'}`}>
                    {selectedExam.status || 'Proposed'}
                  </span>
                </span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Professor:</span>
                <span className="detail-value">{selectedExam.professor?.name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Group:</span>
                <span className="detail-value">{selectedExam.grupa?.name || 'N/A'}</span>
              </div>
            </div>
            <div className="modal-footer">
              {canEdit && (
                <>
                  <button 
                    className="action-button edit-button"
                    onClick={() => {
                      closeModal();
                      handleEditExam(selectedExam);
                    }}
                  >
                    <FontAwesomeIcon icon={faEdit} /> Edit
                  </button>
                  <button 
                    className="action-button delete-button"
                    onClick={() => {
                      closeModal();
                      handleDeleteExam(selectedExam.id);
                    }}
                  >
                    <FontAwesomeIcon icon={faTrash} /> Delete
                  </button>
                </>
              )}
              <button className="action-button" onClick={closeModal}>Close</button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && selectedExam && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Confirm Delete</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <p>Are you sure you want to delete this exam?</p>
              <p className="warning-text">This action cannot be undone.</p>
            </div>
            <div className="modal-footer">
              <button 
                type="button"
                className="action-button delete-button"
                onClick={confirmDelete}
              >
                <FontAwesomeIcon icon={faTrash} /> Delete
              </button>
              <button 
                type="button"
                className="action-button cancel-button"
                onClick={closeModal}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit/Create Exam Modal */}
      {(showEditModal || showCreateModal) && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{showEditModal ? 'Edit Exam' : 'Create New Exam'}</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="form-group">
                  <label htmlFor="date">Date</label>
                  <input
                    type="date"
                    id="date"
                    name="date"
                    value={formData.date || ''}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="time">Time</label>
                  <input
                    type="time"
                    id="time"
                    name="time"
                    value={formData.time || ''}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="faculty">Faculty</label>
                  <select
                    id="faculty"
                    name="faculty"
                    value={selectedFaculty}
                    onChange={handleFacultyChange}
                  >
                    <option value="">All Faculties</option>
                    {faculties.map(faculty => (
                      <option key={faculty.id} value={faculty.id}>
                        {faculty.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="course_id">Course</label>
                  <select
                    id="course_id"
                    name="course_id"
                    value={formData.course_id || ''}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select a course</option>
                    {filteredCourses && filteredCourses.length > 0 ? (
                      filteredCourses.map(course => (
                        <option key={`course-${course.id}`} value={course.id}>
                          {course.name} - {course.profesor_name || 'No professor'}
                        </option>
                      ))
                    ) : (
                      <option value="" disabled>No courses available</option>
                    )}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="sala_name">Room</label>
                  <select
                    id="sala_name"
                    name="sala_name"
                    value={formData.sala_name || ''}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select a room</option>
                    {rooms.map(room => (
                      <option key={room.id} value={room.name}>{room.name}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="grupa_name">Group</label>
                  <select
                    id="grupa_name"
                    name="grupa_name"
                    value={formData.grupa_name || ''}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select a group</option>
                    {groups.map(group => (
                      <option key={group.id} value={group.name}>{group.name}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="status">Status</label>
                  <select
                    id="status"
                    name="status"
                    value={formData.status || 'proposed'}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="proposed">Proposed</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="cancelled">Cancelled</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button 
                  type="submit" 
                  className="action-button save-button"
                >
                  {showEditModal ? 'Update Exam' : 'Create Exam'}
                </button>
                <button 
                  type="button"
                  className="action-button cancel-button"
                  onClick={closeModal}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Status Change Modal */}
      {showStatusModal && selectedExam && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Change Exam Status</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <p>
                Update status for exam: <strong>{selectedExam.course?.name || 'N/A'}</strong> on <strong>{formatDate(selectedExam.date)}</strong>
              </p>
              
              <div className="form-group">
                <label htmlFor="status">Status</label>
                <select
                  id="status"
                  name="status"
                  value={formData.status || 'proposed'}
                  onChange={handleInputChange}
                  required
                  className="status-select"
                >
                  <option value="proposed">Proposed</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="cancelled">Cancelled</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              
              <div className="status-preview">
                <span>Preview: </span>
                <span className={`status-badge status-${(formData.status || 'proposed').toLowerCase()}`}>
                  {formData.status 
                    ? formData.status.charAt(0).toUpperCase() + formData.status.slice(1).toLowerCase() 
                    : 'Proposed'}
                </span>
              </div>
            </div>
            <div className="modal-footer">
              <button 
                type="button"
                className="action-button save-button"
                onClick={updateExamStatus}
              >
                <FontAwesomeIcon icon={faSave} /> Update Status
              </button>
              <button 
                type="button"
                className="action-button cancel-button"
                onClick={closeModal}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExamsList;
