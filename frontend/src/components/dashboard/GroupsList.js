import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import './DashboardComponents.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faEdit, faTrash, faUsers } from '@fortawesome/free-solid-svg-icons';
import GroupLeadersUpload from '../groups/GroupLeadersUpload';

const GroupsList = () => {
  const { currentUser } = useAuth();
  const [groups, setGroups] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    year: '',
    specialization: '',
    leader_id: ''
  });

  useEffect(() => {
    fetchGroups();
    fetchStudents();
  }, []);

  const fetchGroups = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://localhost:8000/api/v1/groups/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setGroups(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching groups:', err);
      setError('Failed to fetch groups. Please try again later.');
      setLoading(false);
    }
  };

  const fetchStudents = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No authentication token found');
        return;
      }

      // This endpoint doesn't exist yet, but we'll assume it will be created
      const response = await axios.get('http://localhost:8000/api/v1/users/students', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStudents(response.data);
    } catch (err) {
      console.error('Error fetching students:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleCreateGroup = () => {
    setFormData({
      name: '',
      year: '',
      specialization: '',
      leader_id: ''
    });
    setShowCreateModal(true);
  };

  const handleEditGroup = (group) => {
    setSelectedGroup(group);
    setFormData({
      name: group.name,
      year: group.year || '',
      specialization: group.specialization || '',
      leader_id: group.leader ? group.leader.id : ''
    });
    setShowEditModal(true);
  };

  const handleDeleteGroup = (group) => {
    setSelectedGroup(group);
    setShowDeleteModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setShowCreateModal(false);
    setShowEditModal(false);
    setShowDeleteModal(false);
    setSelectedGroup(null);
    setError(null);
    setSuccess(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      if (showCreateModal) {
        await axios.post('http://localhost:8000/api/v1/groups/', formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setSuccess('Group created successfully');
      } else if (showEditModal && selectedGroup) {
        await axios.put(`http://localhost:8000/api/v1/groups/${selectedGroup.name}`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setSuccess('Group updated successfully');
      }

      // Refresh groups list
      fetchGroups();
      
      // Close modal after a delay
      setTimeout(() => {
        closeModal();
      }, 1500);
    } catch (err) {
      console.error('Error submitting form:', err);
      setError(err.response?.data?.detail || 'An error occurred. Please try again.');
    }
  };

  const confirmDelete = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token || !selectedGroup) {
        setError('No authentication token or group selected');
        return;
      }

      await axios.delete(`http://localhost:8000/api/v1/groups/${selectedGroup.name}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setSuccess('Group deleted successfully');
      
      // Refresh groups list
      fetchGroups();
      
      // Close modal after a delay
      setTimeout(() => {
        closeModal();
      }, 1500);
    } catch (err) {
      console.error('Error deleting group:', err);
      setError(err.response?.data?.detail || 'An error occurred. Please try again.');
    }
  };

  const assignLeader = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      if (!token || !selectedGroup) {
        setError('No authentication token or group selected');
        return;
      }

      await axios.put(`http://localhost:8000/api/v1/groups/${selectedGroup.name}/leader?leader_id=${formData.leader_id}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setSuccess('Group leader assigned successfully');
      
      // Refresh groups list
      fetchGroups();
      
      // Close modal after a delay
      setTimeout(() => {
        closeModal();
      }, 1500);
    } catch (err) {
      console.error('Error assigning group leader:', err);
      setError(err.response?.data?.detail || 'An error occurred. Please try again.');
    }
  };

  // Check if user is secretariat
  const isAdmin = currentUser && (currentUser.role === 'ADMIN' || currentUser.role === 'SECRETARIAT');
  const isSecretariat = currentUser && currentUser.role === 'SECRETARIAT';

  return (
    <div className="dashboard-component">
      <div className="component-header">
        <h2>Groups Management</h2>
        {isSecretariat && (
          <button 
            className="action-button create-button"
            onClick={handleCreateGroup}
          >
            <FontAwesomeIcon icon={faPlus} /> Create Group
          </button>
        )}
      </div>

      {/* Group Leaders Upload - only for secretariat users */}
      {isSecretariat && (
        <div className="section-container">
          <div className="section-header">
            <h3><FontAwesomeIcon icon={faUsers} /> Group Leaders Management</h3>
            <p>Upload a list of group leaders (name and @student.usv.ro email)</p>
          </div>
          <GroupLeadersUpload onUploadComplete={fetchGroups} />
        </div>
      )}

      {/* Group list */}
      <div className="data-table-container">
        {loading ? (
          <div className="loading">Loading groups...</div>
        ) : error && !success ? (
          <div className="error-message">{error}</div>
        ) : groups.length === 0 ? (
          <div className="empty-state">
            <p>No groups found.</p>
            {isSecretariat && (
              <button 
                className="action-button create-button"
                onClick={handleCreateGroup}
              >
                <FontAwesomeIcon icon={faPlus} /> Create Group
              </button>
            )}
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Year</th>
                <th>Specialization</th>
                <th>Group Leader</th>
              </tr>
            </thead>
            <tbody>
              {groups.map((group) => (
                <tr key={group.name}>
                  <td>{group.name}</td>
                  <td>{group.year || 'N/A'}</td>
                  <td>{group.specialization || 'N/A'}</td>
                  <td>
                    {group.leader ? group.leader.name : 'Not assigned'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Create/Edit Group Modal */}
      {(showCreateModal || showEditModal) && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{showCreateModal ? 'Create Group' : 'Edit Group'}</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {success && <div className="success-message">{success}</div>}
                {error && <div className="error-message">{error}</div>}
                
                <div className="form-group">
                  <label htmlFor="name">Group Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    disabled={showEditModal} // Can't change name when editing
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="year">Year</label>
                  <input
                    type="number"
                    id="year"
                    name="year"
                    value={formData.year}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="specialization">Specialization</label>
                  <input
                    type="text"
                    id="specialization"
                    name="specialization"
                    value={formData.specialization}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button 
                  type="submit"
                  className="action-button save-button"
                  disabled={loading}
                >
                  {loading ? 'Saving...' : 'Save'}
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

      {/* Delete Group Modal */}
      {showDeleteModal && selectedGroup && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Confirm Delete</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              {success && <div className="success-message">{success}</div>}
              {error && <div className="error-message">{error}</div>}
              
              <p>Are you sure you want to delete the group "{selectedGroup.name}"?</p>
              <p className="warning-text">This action cannot be undone.</p>
            </div>
            <div className="modal-footer">
              <button 
                type="button"
                className="action-button delete-button"
                onClick={confirmDelete}
                disabled={loading}
              >
                {loading ? 'Deleting...' : 'Delete'}
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

export default GroupsList;
