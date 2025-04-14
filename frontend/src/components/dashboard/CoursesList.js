import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import './DashboardComponents.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEdit, faTrash, faPlus } from '@fortawesome/free-solid-svg-icons';

const CoursesList = () => {
  const { currentUser } = useAuth();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [professors, setProfessors] = useState([]);
  
  // Form state for create/edit
  const [formData, setFormData] = useState({
    name: '',
    profesor_name: '',
    year: '',
    semester: '',
    description: '',
    credits: ''
  });

  const fetchCourses = async () => {
    try {
      setError(null);
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://localhost:8000/api/v1/courses/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      // Process the course data to ensure all properties are valid
      const processedCourses = response.data.map(course => {
        return {
          id: course.id,
          name: course.name || '',
          profesor_name: course.profesor_name || '',
          credits: course.credits || '',
          // Create a virtual professor object for display purposes
          professor: { name: course.profesor_name || 'N/A' }
        };
      });
      
      setCourses(processedCourses);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching courses:', err);
      setError('Failed to load courses. Please try again later.');
      setLoading(false);
    }
  };

  const fetchProfessors = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      // Fetch professors (users with role PROFESSOR)
      const usersResponse = await axios.get('http://localhost:8000/api/v1/users/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const professorsList = usersResponse.data.filter(user => user.role === 'PROFESSOR');
      setProfessors(professorsList);
    } catch (err) {
      console.error('Error fetching professors:', err);
    }
  };

  useEffect(() => {
    fetchCourses();
    fetchProfessors();
  }, []);

  const handleViewCourse = (course) => {
    setSelectedCourse(course);
    setShowModal(true);
  };

  const handleEditCourse = (course) => {
    setSelectedCourse(course);
    setFormData({
      name: course.name || '',
      profesor_name: course.profesor_name || '',
      year: course.year || '',
      semester: course.semester || '',
      description: course.description || '',
      credits: course.credits || ''
    });
    setShowEditModal(true);
  };

  const handleDeleteCourse = (course) => {
    setSelectedCourse(course);
    setShowDeleteModal(true);
  };

  const handleCreateCourse = () => {
    setFormData({
      name: '',
      profesor_name: '',
      year: '',
      semester: '',
      description: '',
      credits: ''
    });
    setShowCreateModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setShowDeleteModal(false);
    setShowEditModal(false);
    setShowCreateModal(false);
    setSelectedCourse(null);
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

  const confirmDelete = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      await axios.delete(`http://localhost:8000/api/v1/courses/${selectedCourse.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setSuccess('Course deleted successfully');
      setShowDeleteModal(false);
      
      // Refresh courses list
      fetchCourses();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error deleting course:', err);
      setError(err.response?.data?.detail || 'Failed to delete course. Please try again.');
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

      const courseData = {
        ...formData,
        profesor_name: formData.profesor_name,
        credits: formData.credits ? parseInt(formData.credits) : null
      };

      if (showEditModal) {
        // Update existing course
        await axios.put(`http://localhost:8000/api/v1/courses/${selectedCourse.id}`, courseData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        setSuccess('Course updated successfully');
      } else {
        // Create new course
        await axios.post('http://localhost:8000/api/v1/courses/', courseData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        setSuccess('Course created successfully');
      }

      // Close modal and refresh courses list
      closeModal();
      fetchCourses();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error saving course:', err);
      setError(err.response?.data?.detail || 'Failed to save course. Please check your input and try again.');
    }
  };

  // Check if user has admin/secretariat role
  const isAdmin = currentUser && currentUser.role === 'SECRETARIAT';
  const isProfessor = currentUser && currentUser.role === 'PROFESSOR';
  const canEdit = isAdmin || isProfessor;

  if (loading) {
    return <div className="loading">Loading courses...</div>;
  }

  return (
    <div className="dashboard-component">
      <div className="component-header">
        <h2>Courses List</h2>
        <p>View all available courses and their details</p>
        
        {/* Success message */}
        {success && <div className="success-message">{success}</div>}
        {/* Error message */}
        {error && <div className="error-message">{error}</div>}
        
        {/* Create button for admins and professors */}
        {canEdit && (
          <div className="action-bar">
            <button 
              className="action-button create-button"
              onClick={handleCreateCourse}
            >
              <FontAwesomeIcon icon={faPlus} /> Create New Course
            </button>
          </div>
        )}
      </div>

      {courses.length === 0 ? (
        <div className="no-data">No courses available at this time.</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Professor</th>
                <th>Year</th>
                <th>Semester</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((course) => (
                <tr key={course.id}>
                  <td>{course.id}</td>
                  <td>{course.name}</td>
                  <td>{course.professor.name || 'N/A'}</td>
                  <td>{course.year || 'N/A'}</td>
                  <td>{course.semester || 'N/A'}</td>
                  <td className="actions-cell">
                    <button 
                      className="action-button view-button"
                      onClick={() => handleViewCourse(course)}
                      title="View details"
                    >
                      <FontAwesomeIcon icon={faEye} />
                    </button>
                    
                    {canEdit && (
                      <>
                        <button 
                          className="action-button edit-button"
                          onClick={() => handleEditCourse(course)}
                          title="Edit course"
                        >
                          <FontAwesomeIcon icon={faEdit} />
                        </button>
                        
                        <button 
                          className="action-button delete-button"
                          onClick={() => handleDeleteCourse(course)}
                          title="Delete course"
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

      {/* Course Details Modal */}
      {showModal && selectedCourse && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Course Details</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <div className="detail-row">
                <span className="detail-label">ID:</span>
                <span className="detail-value">{selectedCourse.id}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Name:</span>
                <span className="detail-value">{selectedCourse.name}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Professor:</span>
                <span className="detail-value">{selectedCourse.professor.name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Year:</span>
                <span className="detail-value">{selectedCourse.year || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Semester:</span>
                <span className="detail-value">{selectedCourse.semester || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Description:</span>
                <span className="detail-value">{selectedCourse.description || 'No description available'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Credits:</span>
                <span className="detail-value">{selectedCourse.credits || 'N/A'}</span>
              </div>
            </div>
            <div className="modal-footer">
              {canEdit && (
                <>
                  <button 
                    className="action-button edit-button"
                    onClick={() => {
                      closeModal();
                      handleEditCourse(selectedCourse);
                    }}
                  >
                    <FontAwesomeIcon icon={faEdit} /> Edit
                  </button>
                  <button 
                    className="action-button delete-button"
                    onClick={() => {
                      closeModal();
                      handleDeleteCourse(selectedCourse);
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
      {showDeleteModal && selectedCourse && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Confirm Delete</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <p>Are you sure you want to delete the course <strong>{selectedCourse.name}</strong>?</p>
              <p className="warning-text">This action cannot be undone. Deleting this course may affect related exams.</p>
            </div>
            <div className="modal-footer">
              <button 
                className="action-button delete-button"
                onClick={confirmDelete}
              >
                <FontAwesomeIcon icon={faTrash} /> Delete
              </button>
              <button 
                className="action-button cancel-button"
                onClick={closeModal}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit/Create Course Modal */}
      {(showEditModal || showCreateModal) && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{showEditModal ? 'Edit Course' : 'Create New Course'}</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="form-group">
                  <label htmlFor="name">Course Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="profesor_name">Professor</label>
                  <select
                    id="profesor_name"
                    name="profesor_name"
                    value={formData.profesor_name}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select a professor</option>
                    {professors.map(professor => (
                      <option key={professor.id} value={professor.name}>
                        {professor.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="year">Year</label>
                  <select
                    id="year"
                    name="year"
                    value={formData.year}
                    onChange={handleInputChange}
                  >
                    <option value="">Select a year</option>
                    <option value="1">Year 1</option>
                    <option value="2">Year 2</option>
                    <option value="3">Year 3</option>
                    <option value="4">Year 4</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="semester">Semester</label>
                  <select
                    id="semester"
                    name="semester"
                    value={formData.semester}
                    onChange={handleInputChange}
                  >
                    <option value="">Select a semester</option>
                    <option value="1">Semester 1</option>
                    <option value="2">Semester 2</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="credits">Credits</label>
                  <input
                    type="number"
                    id="credits"
                    name="credits"
                    value={formData.credits}
                    onChange={handleInputChange}
                    min="1"
                    max="30"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="description">Description</label>
                  <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows="4"
                  ></textarea>
                </div>
              </div>
              <div className="modal-footer">
                <button 
                  type="submit" 
                  className="action-button save-button"
                >
                  {showEditModal ? 'Update Course' : 'Create Course'}
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
    </div>
  );
};

export default CoursesList;
