import React, { useState } from 'react';
import axios from 'axios';
import './DashboardComponents.css';

const CleanupDuplicatesButton = ({ onSuccess, entityType = 'rooms' }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [duplicatesFound, setDuplicatesFound] = useState(0);
  const [duplicatesRemoved, setDuplicatesRemoved] = useState(0);
  const [showMergeConfirm, setShowMergeConfirm] = useState(false);
  const [duplicateGroups, setDuplicateGroups] = useState([]);
  const [processingStep, setProcessingStep] = useState('');

  // Close the merge confirmation modal
  const closeMergeConfirm = () => {
    setShowMergeConfirm(false);
  };

  // Function to merge duplicate rooms by reassigning exams
  const mergeDuplicates = async () => {
    setProcessingStep('Merging duplicates...');
    let mergeSuccessCount = 0;
    
    try {
      const token = localStorage.getItem('token');
      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
      
      // Process each group of duplicates
      for (const group of duplicateGroups) {
        // Use the first item as the primary one to keep
        const primaryItem = group[0];
        
        // For each duplicate (except the primary)
        for (let i = 1; i < group.length; i++) {
          const duplicateItem = group[i];
          
          // If we're working with rooms
          if (entityType === 'rooms') {
            // Get all exams using this duplicate room
            const examsResponse = await axios.get('http://localhost:8000/api/v1/exams/', { headers });
            const exams = examsResponse.data;
            
            // Find exams using the duplicate room
            const affectedExams = exams.filter(exam => exam.sala_id === duplicateItem.id);
            
            // Update each exam to use the primary room instead
            for (const exam of affectedExams) {
              try {
                await axios.put(`http://localhost:8000/api/v1/exams/${exam.id}`, 
                  { sala_id: primaryItem.id },
                  { headers }
                );
                console.log(`Updated exam ${exam.id} to use room ${primaryItem.id} (${primaryItem.name})`);
              } catch (err) {
                console.error(`Failed to update exam ${exam.id}:`, err.response?.data || err.message);
              }
            }
            
            // Now try to delete the duplicate room
            try {
              await axios.delete(`http://localhost:8000/api/v1/rooms/${duplicateItem.id}`, { headers });
              mergeSuccessCount++;
            } catch (err) {
              console.error(`Failed to delete duplicate room ${duplicateItem.id}:`, err.response?.data || err.message);
            }
          }
          // Handle other entity types similarly if needed
        }
      }
      
      setDuplicatesRemoved(mergeSuccessCount);
      setMessage({
        type: 'success',
        text: `Successfully merged ${mergeSuccessCount} duplicate ${entityType}.`
      });
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      console.error(`Error merging duplicate ${entityType}:`, error);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || `Failed to merge duplicate ${entityType}`
      });
    } finally {
      setShowMergeConfirm(false);
      setProcessingStep('');
      setLoading(false);
    }
  };

  const cleanupDuplicates = async () => {
    setLoading(true);
    setMessage(null);
    setDuplicatesFound(0);
    setDuplicatesRemoved(0);
    setProcessingStep('Checking for duplicates...');
    
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

      // Get the API endpoint based on entity type
      let endpoint;
      switch (entityType) {
        case 'rooms':
          endpoint = 'rooms';
          break;
        case 'courses':
          endpoint = 'courses';
          break;
        case 'groups':
          endpoint = 'groups';
          break;
        default:
          endpoint = 'rooms';
      }

      // Fetch all entities
      const response = await axios.get(`http://localhost:8000/api/v1/${endpoint}/`, { headers });
      const entities = response.data;
      
      // Find duplicates by name (case insensitive)
      const nameMap = new Map();
      const duplicates = [];
      const duplicateGroupsMap = new Map();
      
      // Group entities by name
      entities.forEach(entity => {
        const name = entity.name.toLowerCase().trim();
        if (!duplicateGroupsMap.has(name)) {
          duplicateGroupsMap.set(name, [entity]);
        } else {
          duplicateGroupsMap.get(name).push(entity);
        }
      });
      
      // Filter out groups with only one entity
      const groups = Array.from(duplicateGroupsMap.values()).filter(group => group.length > 1);
      
      // Count total duplicates
      const totalDuplicates = groups.reduce((sum, group) => sum + group.length - 1, 0);
      setDuplicatesFound(totalDuplicates);
      
      if (totalDuplicates === 0) {
        setMessage({
          type: 'success',
          text: `No duplicate ${entityType} found.`
        });
        setLoading(false);
        return;
      }
      
      // Store duplicate groups for the merge function
      setDuplicateGroups(groups);
      
      // Check if any duplicates are used in exams
      setProcessingStep('Checking exam references...');
      const examsResponse = await axios.get('http://localhost:8000/api/v1/exams/', { headers });
      const exams = examsResponse.data;
      
      let hasReferences = false;
      
      if (entityType === 'rooms') {
        // Check if any duplicate rooms are used in exams
        for (const group of groups) {
          for (let i = 1; i < group.length; i++) {
            const isReferenced = exams.some(exam => exam.sala_id === group[i].id);
            if (isReferenced) {
              hasReferences = true;
              break;
            }
          }
          if (hasReferences) break;
        }
      }
      
      if (hasReferences) {
        // Show merge confirmation dialog
        setShowMergeConfirm(true);
      } else {
        // Try to delete duplicates directly
        let removedCount = 0;
        for (const group of groups) {
          // Keep the first one, delete the rest
          for (let i = 1; i < group.length; i++) {
            try {
              await axios.delete(`http://localhost:8000/api/v1/${endpoint}/${group[i].id}`, { headers });
              removedCount++;
            } catch (err) {
              console.error(`Failed to delete duplicate ${entityType}:`, err.response?.data || err.message);
            }
          }
        }
        
        setDuplicatesRemoved(removedCount);
        
        if (removedCount > 0) {
          setMessage({
            type: 'success',
            text: `Successfully removed ${removedCount} duplicate ${entityType}.`
          });
          
          if (onSuccess) {
            onSuccess();
          }
        } else {
          setMessage({
            type: 'warning',
            text: `Found ${totalDuplicates} duplicates, but couldn't remove any. There might be references not detected.`
          });
        }
      }
    } catch (error) {
      console.error(`Error cleaning up duplicate ${entityType}:`, error);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || `Failed to clean up duplicate ${entityType}`
      });
    } finally {
      if (!showMergeConfirm) {
        setLoading(false);
      }
      setProcessingStep('');
    }
  };

  return (
    <div className="cleanup-duplicates-container">
      <button 
        className="cleanup-button"
        onClick={cleanupDuplicates}
        disabled={loading}
      >
        {loading ? `Processing ${entityType}...` : `Clean up duplicate ${entityType}`}
      </button>
      
      {processingStep && <div className="processing-step">{processingStep}</div>}
      
      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
      
      {duplicatesFound > 0 && !showMergeConfirm && (
        <div className="duplicates-info">
          <p>Duplicates found: {duplicatesFound}</p>
          <p>Duplicates removed: {duplicatesRemoved}</p>
          {duplicatesFound > duplicatesRemoved && (
            <p className="warning-text">
              Some duplicates could not be removed because they are being used in exams.
            </p>
          )}
        </div>
      )}
      
      {/* Merge Confirmation Modal */}
      {showMergeConfirm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Merge Duplicate {entityType.charAt(0).toUpperCase() + entityType.slice(1)}</h3>
              <button className="close-button" onClick={closeMergeConfirm}>×</button>
            </div>
            <div className="modal-body">
              <p>Found {duplicatesFound} duplicate {entityType} that are being used by exams.</p>
              <p>Would you like to merge these duplicates? This will:</p>
              <ul>
                <li>Keep one {entityType.slice(0, -1)} from each duplicate group</li>
                <li>Reassign all exams from duplicate {entityType} to the kept one</li>
                <li>Delete the duplicate {entityType}</li>
              </ul>
              <p className="warning-text">This action cannot be undone.</p>
            </div>
            <div className="modal-footer">
              <button 
                className="action-button confirm-button"
                onClick={mergeDuplicates}
              >
                Merge Duplicates
              </button>
              <button 
                className="action-button cancel-button"
                onClick={closeMergeConfirm}
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

export default CleanupDuplicatesButton;
