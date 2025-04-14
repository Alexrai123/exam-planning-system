import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import './DashboardComponents.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEdit, faTrash, faPlus } from '@fortawesome/free-solid-svg-icons';

const RoomsList = () => {
  const { currentUser } = useAuth();
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  // Form state for create/edit
  const [formData, setFormData] = useState({
    name: ''
  });

  const fetchRooms = async () => {
    try {
      setError(null);
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://localhost:8000/api/v1/rooms/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setRooms(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching rooms:', err);
      setError('Failed to load rooms. Please try again later.');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  const handleViewRoom = (room) => {
    setSelectedRoom(room);
    setShowModal(true);
  };

  const handleEditRoom = (room) => {
    setFormData({
      name: room.name || ''
    });
    setSelectedRoom(room);
    setShowEditModal(true);
  };

  const handleDeleteRoom = (room) => {
    setSelectedRoom(room);
    setShowDeleteModal(true);
  };

  const handleCreateRoom = () => {
    setFormData({
      name: ''
    });
    setShowCreateModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setShowDeleteModal(false);
    setShowEditModal(false);
    setShowCreateModal(false);
    setSelectedRoom(null);
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

      // First check if there are any exams using this room
      const examsResponse = await axios.get('http://localhost:8000/api/v1/exams/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      const roomExams = examsResponse.data.filter(exam => exam.sala_id === selectedRoom.id);
      
      if (roomExams.length > 0) {
        setError(`Cannot delete room. There are ${roomExams.length} exam(s) scheduled in this room. Please reassign or delete those exams first.`);
        return;
      }

      await axios.delete(`http://localhost:8000/api/v1/rooms/${selectedRoom.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setSuccess('Room deleted successfully');
      setShowDeleteModal(false);
      
      // Refresh rooms list
      fetchRooms();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error deleting room:', err);
      if (err.response?.status === 400 && err.response?.data?.detail?.includes('foreign key constraint')) {
        setError('Cannot delete this room because it is being used by one or more exams. Please reassign or delete those exams first.');
      } else {
        setError(err.response?.data?.detail || 'Failed to delete room. Please try again.');
      }
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

      // Check for duplicate room name
      const roomName = formData.name.trim();
      const isDuplicate = rooms.some(room => 
        room.name.toLowerCase() === roomName.toLowerCase() && 
        (!showEditModal || (showEditModal && room.id !== selectedRoom.id))
      );

      if (isDuplicate) {
        setError(`A room with the name "${roomName}" already exists. Please use a different name.`);
        return;
      }

      const roomData = {
        name: roomName, // Use trimmed name
      };

      if (showEditModal) {
        // Update existing room
        await axios.put(`http://localhost:8000/api/v1/rooms/${selectedRoom.id}`, roomData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        setSuccess('Room updated successfully');
      } else {
        // Create new room
        await axios.post('http://localhost:8000/api/v1/rooms/', roomData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        setSuccess('Room created successfully');
      }

      // Close modal and refresh rooms list
      closeModal();
      fetchRooms();
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error saving room:', err);
      setError(err.response?.data?.detail || 'Failed to save room. Please check your input and try again.');
    }
  };

  // Check if user has admin/secretariat role
  const isAdmin = currentUser && currentUser.role === 'SECRETARIAT';
  const canEdit = isAdmin; // Only admins can edit rooms

  if (loading) {
    return <div className="loading">Loading rooms...</div>;
  }

  return (
    <div className="dashboard-component">
      <div className="component-header">
        <h2>Rooms List</h2>
        <p>View all available rooms and their details</p>
        
        {/* Success message */}
        {success && <div className="success-message">{success}</div>}
        {/* Error message */}
        {error && <div className="error-message">{error}</div>}
        
        {isAdmin && (
          <div className="admin-actions">
            <button 
              className="create-button"
              onClick={handleCreateRoom}
            >
              <FontAwesomeIcon icon={faPlus} /> Create Room
            </button>
          </div>
        )}
      </div>

      {rooms.length === 0 ? (
        <div className="no-data">No rooms available at this time.</div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {rooms.map((room) => (
                <tr key={room.id}>
                  <td>{room.id}</td>
                  <td>{room.name}</td>
                  <td>
                    <div className="action-buttons">
                      <button
                        className="action-button view-button"
                        onClick={() => handleViewRoom(room)}
                        title="View Details"
                      >
                        <FontAwesomeIcon icon={faEye} />
                      </button>
                      {canEdit && (
                        <>
                          <button
                            className="action-button edit-button"
                            onClick={() => handleEditRoom(room)}
                            title="Edit Room"
                          >
                            <FontAwesomeIcon icon={faEdit} />
                          </button>
                          <button
                            className="action-button delete-button"
                            onClick={() => handleDeleteRoom(room)}
                            title="Delete Room"
                          >
                            <FontAwesomeIcon icon={faTrash} />
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Room Details Modal */}
      {showModal && selectedRoom && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Room Details</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <div className="room-details">
                <div className="detail-row">
                  <span className="detail-label">Room Name:</span>
                  <span className="detail-value">{selectedRoom.name}</span>
                </div>
              </div>
            </div>
            <div className="modal-footer">
              {canEdit && (
                <>
                  <button 
                    className="action-button edit-button"
                    onClick={() => {
                      closeModal();
                      handleEditRoom(selectedRoom);
                    }}
                  >
                    <FontAwesomeIcon icon={faEdit} /> Edit
                  </button>
                  <button 
                    className="action-button delete-button"
                    onClick={() => {
                      closeModal();
                      handleDeleteRoom(selectedRoom);
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
      {showDeleteModal && selectedRoom && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Confirm Delete</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <p>Are you sure you want to delete the room <strong>{selectedRoom.name}</strong>?</p>
              <p className="warning-text">This action cannot be undone. Deleting this room may affect related exams.</p>
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

      {/* Edit/Create Room Modal */}
      {(showEditModal || showCreateModal) && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{showEditModal ? 'Edit Room' : 'Create New Room'}</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="form-group">
                  <label htmlFor="name">Room Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button 
                  type="submit" 
                  className="action-button save-button"
                >
                  {showEditModal ? 'Update Room' : 'Create Room'}
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

export default RoomsList;
