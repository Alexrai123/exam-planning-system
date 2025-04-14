import React, { useState } from 'react';
import axios from 'axios';
import './DashboardComponents.css';

const UserProfile = ({ userData }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: userData?.name || '',
    email: userData?.email || '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Validate passwords match if changing password
    if (formData.password && formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Validate password length if changing password
    if (formData.password && formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Only include password if it's being changed
      const updateData = {
        name: formData.name,
        email: formData.email
      };

      if (formData.password) {
        updateData.password = formData.password;
      }

      await axios.put('http://localhost:8000/api/v1/users/me', updateData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setSuccess('Profile updated successfully');
      setIsEditing(false);
      
      // Reset password fields
      setFormData({
        ...formData,
        password: '',
        confirmPassword: ''
      });
    } catch (err) {
      console.error('Error updating profile:', err);
      setError(err.response?.data?.detail || 'Failed to update profile. Please try again later.');
    }
  };

  const cancelEdit = () => {
    setIsEditing(false);
    setFormData({
      name: userData?.name || '',
      email: userData?.email || '',
      password: '',
      confirmPassword: ''
    });
    setError(null);
    setSuccess(null);
  };

  return (
    <div className="dashboard-component">
      <div className="component-header">
        <h2>User Profile</h2>
        <p>View and manage your profile information</p>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="profile-container">
        <div className="profile-avatar">
          <div className="avatar-circle">
            {userData?.name ? userData.name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div className="role-indicator">
            <span className="role-badge">{userData?.role || 'USER'}</span>
          </div>
        </div>

        {isEditing ? (
          <form className="profile-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">New Password (leave blank to keep current)</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm New Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="action-button save-button">
                Save Changes
              </button>
              <button 
                type="button" 
                className="action-button cancel-button"
                onClick={cancelEdit}
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="profile-details">
            <div className="detail-row">
              <span className="detail-label">Name:</span>
              <span className="detail-value">{userData?.name || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Email:</span>
              <span className="detail-value">{userData?.email || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Role:</span>
              <span className="detail-value">{userData?.role || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Account ID:</span>
              <span className="detail-value">{userData?.id || 'N/A'}</span>
            </div>

            <div className="profile-actions">
              <button 
                className="action-button edit-button"
                onClick={() => setIsEditing(true)}
              >
                Edit Profile
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserProfile;
