import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import './DashboardComponents.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSync, faDownload, faCheck, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';

const ExternalDataImport = () => {
  const { currentUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [externalData, setExternalData] = useState({
    professors: [],
    rooms: [],
    faculties: [],
    subgroups: []
  });
  const [stats, setStats] = useState({
    professors: { count: 0 },
    rooms: { count: 0 },
    faculties: { count: 0 },
    subgroups: { count: 0 }
  });

  const fetchExternalData = async () => {
    setFetchLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found. Please log in again.');
        setFetchLoading(false);
        return;
      }

      const response = await axios.get('http://localhost:8000/api/v1/external-data/fetch', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      setExternalData(response.data);
      
      // Update stats
      setStats({
        professors: { count: response.data.professors.length },
        rooms: { count: response.data.rooms.length },
        faculties: { count: response.data.faculties.length },
        subgroups: { count: response.data.subgroups.length }
      });
      
      setSuccess('External data fetched successfully!');
    } catch (err) {
      console.error('Error fetching external data:', err);
      setError(err.response?.data?.detail || 'Failed to fetch external data. Please try again.');
    } finally {
      setFetchLoading(false);
    }
  };

  const importData = async (dataType) => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found. Please log in again.');
        setLoading(false);
        return;
      }

      const response = await axios.post(`http://localhost:8000/api/v1/external-data/import/${dataType}`, {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      setSuccess(`${dataType} data imported successfully! ${response.data.imported_count} new items added, ${response.data.updated_count} items updated.`);
    } catch (err) {
      console.error(`Error importing ${dataType} data:`, err);
      setError(err.response?.data?.detail || `Failed to import ${dataType} data. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

  const importAllData = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found. Please log in again.');
        setLoading(false);
        return;
      }

      const response = await axios.post('http://localhost:8000/api/v1/external-data/import/all', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      setSuccess('All data imported successfully!');
    } catch (err) {
      console.error('Error importing all data:', err);
      setError(err.response?.data?.detail || 'Failed to import all data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Check if user is authorized to access this component
  // Make role check more flexible by normalizing to uppercase
  if (currentUser?.role?.toUpperCase() !== 'SECRETARIAT') {
    return (
      <div className="component-container">
        <div className="access-denied">
          <FontAwesomeIcon icon={faExclamationTriangle} size="3x" />
          <h2>Access Denied</h2>
          <p>You do not have permission to access this feature.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="component-container">
      <div className="component-header">
        <h2>External Data Import</h2>
        <p>Import data from the university's API to replace test data.</p>
      </div>

      {error && (
        <div className="alert alert-danger">
          <FontAwesomeIcon icon={faExclamationTriangle} /> {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          <FontAwesomeIcon icon={faCheck} /> {success}
        </div>
      )}

      <div className="action-buttons">
        <button 
          className="primary-button" 
          onClick={fetchExternalData} 
          disabled={fetchLoading}
        >
          {fetchLoading ? (
            <>
              <FontAwesomeIcon icon={faSync} spin /> Fetching Data...
            </>
          ) : (
            <>
              <FontAwesomeIcon icon={faSync} /> Fetch External Data
            </>
          )}
        </button>
        
        <button 
          className="success-button" 
          onClick={importAllData} 
          disabled={loading || stats.professors.count === 0}
        >
          {loading ? (
            <>
              <FontAwesomeIcon icon={faDownload} spin /> Importing All Data...
            </>
          ) : (
            <>
              <FontAwesomeIcon icon={faDownload} /> Import All Data
            </>
          )}
        </button>
      </div>

      <div className="data-sections">
        {/* Professors Section */}
        <div className="data-section">
          <div className="data-section-header">
            <h3>Professors</h3>
            <span className="data-count">{stats.professors.count} items</span>
          </div>
          
          <div className="data-section-content">
            <p>Import professor data including names, departments, email addresses, and phone numbers.</p>
            
            <div className="data-sample">
              {externalData.professors.slice(0, 3).map((professor, index) => (
                <div key={index} className="data-item">
                  <strong>{professor.name}</strong>
                  <div className="data-details">
                    {professor.specialization && <span>Department: {professor.specialization}</span>}
                    {professor.email && <span>Email: {professor.email}</span>}
                  </div>
                </div>
              ))}
              {stats.professors.count > 3 && (
                <div className="data-more">
                  + {stats.professors.count - 3} more professors
                </div>
              )}
            </div>
            
            <button 
              className="secondary-button" 
              onClick={() => importData('professors')} 
              disabled={loading || stats.professors.count === 0}
            >
              {loading ? 'Importing...' : 'Import Professors'}
            </button>
          </div>
        </div>

        {/* Rooms Section */}
        <div className="data-section">
          <div className="data-section-header">
            <h3>Rooms</h3>
            <span className="data-count">{stats.rooms.count} items</span>
          </div>
          
          <div className="data-section-content">
            <p>Import room data including names, buildings, capacities, and computer availability.</p>
            
            <div className="data-sample">
              {externalData.rooms.slice(0, 3).map((room, index) => (
                <div key={index} className="data-item">
                  <strong>{room.name}</strong>
                  <div className="data-details">
                    {room.building && <span>Building: {room.building}</span>}
                    {room.capacity > 0 && <span>Capacity: {room.capacity}</span>}
                    {room.computers > 0 && <span>Computers: {room.computers}</span>}
                  </div>
                </div>
              ))}
              {stats.rooms.count > 3 && (
                <div className="data-more">
                  + {stats.rooms.count - 3} more rooms
                </div>
              )}
            </div>
            
            <button 
              className="secondary-button" 
              onClick={() => importData('rooms')} 
              disabled={loading || stats.rooms.count === 0}
            >
              {loading ? 'Importing...' : 'Import Rooms'}
            </button>
          </div>
        </div>

        {/* Groups Section */}
        <div className="data-section">
          <div className="data-section-header">
            <h3>Groups</h3>
            <span className="data-count">{stats.subgroups.count} items</span>
          </div>
          
          <div className="data-section-content">
            <p>Import group data including names, years, and specializations.</p>
            
            <div className="data-sample">
              {externalData.subgroups.slice(0, 3).map((group, index) => (
                <div key={index} className="data-item">
                  <strong>{group.name}</strong>
                  <div className="data-details">
                    {group.year > 0 && <span>Year: {group.year}</span>}
                    {group.specialization && <span>Specialization: {group.specialization}</span>}
                  </div>
                </div>
              ))}
              {stats.subgroups.count > 3 && (
                <div className="data-more">
                  + {stats.subgroups.count - 3} more groups
                </div>
              )}
            </div>
            
            <button 
              className="secondary-button" 
              onClick={() => importData('groups')} 
              disabled={loading || stats.subgroups.count === 0}
            >
              {loading ? 'Importing...' : 'Import Groups'}
            </button>
          </div>
        </div>

        {/* Faculties Section */}
        <div className="data-section">
          <div className="data-section-header">
            <h3>Faculties</h3>
            <span className="data-count">{stats.faculties.count} items</span>
          </div>
          
          <div className="data-section-content">
            <p>View faculty data including short names and full names.</p>
            
            <div className="data-sample">
              {externalData.faculties.slice(0, 3).map((faculty, index) => (
                <div key={index} className="data-item">
                  <strong>{faculty.short_name}</strong>
                  <div className="data-details">
                    {faculty.long_name && <span>{faculty.long_name}</span>}
                  </div>
                </div>
              ))}
              {stats.faculties.count > 3 && (
                <div className="data-more">
                  + {stats.faculties.count - 3} more faculties
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExternalDataImport;
