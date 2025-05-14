import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload, faSpinner, faFileExcel, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import './ImportExams.css';

const ImportExams = ({ onImportComplete }) => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setUploadResult(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select an Excel file first');
      return;
    }

    // Check file extension
    const fileExt = file.name.split('.').pop().toLowerCase();
    if (!['xlsx', 'xls'].includes(fileExt)) {
      setError('Only Excel files (.xlsx, .xls) are allowed');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      // Create form data
      const formData = new FormData();
      formData.append('file', file);

      // No need to check for authentication token with public endpoint

      // Use XMLHttpRequest with the public endpoint that doesn't require authentication
      const xhr = new XMLHttpRequest();
      xhr.open('POST', 'http://127.0.0.1:8000/api/v1/public/imports/exams', true);
      // No need for Authorization header with public endpoint
      
      // Set up event handlers
      xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
          const response = JSON.parse(xhr.responseText);
          setUploadResult(response);
          if (onImportComplete && typeof onImportComplete === 'function') {
            onImportComplete();
          }
          setIsUploading(false);
        } else {
          console.error('Upload failed:', xhr.statusText);
          try {
            // Try to parse the error response as JSON
            const errorResponse = JSON.parse(xhr.responseText);
            if (errorResponse.detail) {
              setError(`Upload failed: ${errorResponse.detail}`);
            } else {
              setError(`Upload failed: ${xhr.statusText || 'Unknown error'}`);
            }
          } catch (e) {
            setError(`Upload failed: ${xhr.statusText || 'Unknown error'}`);
          }
          setIsUploading(false);
        }
      };
      
      xhr.onerror = function() {
        console.error('Network error during upload');
        setError('Network error during upload. Please try again.');
        setIsUploading(false);
      };
      
      // Send the form data
      xhr.send(formData);
      
      // Create a dummy response to keep the rest of the code happy
      const response = { data: 'Uploading...' };

      // The result will be set by the xhr.onload handler
      // No need to set it here or call onImportComplete here
      // Just return to prevent the code from continuing execution
      return;
    } catch (err) {
      console.error('Error uploading file:', err);
      // Handle different error formats
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (typeof err.message === 'string' && err.message.includes('date/time format')) {
        setError('Invalid date format. Please use either YYYY-MM-DD (e.g., 2025-06-15) or DD/MM/YYYY (e.g., 15/06/2025)');
      } else {
        setError(err.message || 'Error uploading file');
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="import-section">
      <div className="import-header">
        <h2><FontAwesomeIcon icon={faFileExcel} /> Import Exams from Excel</h2>
        <p>
          Upload an Excel file with exam data to import into the system. The file should follow the format of the Exam Template.
          Make sure to include the required columns: Course Name, Professor Name, Date (YYYY-MM-DD) or Date (DD/MM/YYYY), Time (HH:MM), Room, Group.
          Both date formats are supported: YYYY-MM-DD (e.g., 2025-06-15) and DD/MM/YYYY (e.g., 15/06/2025).
        </p>
      </div>

      <div className="import-form">
        <div className="file-input-container">
          <input 
            type="file" 
            id="exam-file" 
            accept=".xlsx,.xls" 
            onChange={handleFileChange} 
            className="file-input"
          />
          <label htmlFor="exam-file" className="file-input-label">
            <FontAwesomeIcon icon={faFileExcel} />
            {file ? file.name : 'Choose Excel File'}
          </label>
        </div>

        <button 
          className="upload-button" 
          onClick={handleUpload}
          disabled={isUploading || !file}
        >
          {isUploading ? (
            <>
              <FontAwesomeIcon icon={faSpinner} className="fa-spin" />
              Uploading...
            </>
          ) : (
            <>
              <FontAwesomeIcon icon={faUpload} />
              Upload and Import
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="import-error">
          <FontAwesomeIcon icon={faTimes} />
          {error}
        </div>
      )}

      {uploadResult && (
        <div className="import-result">
          <div className="result-header">
            <FontAwesomeIcon icon={faCheck} className="success-icon" />
            <h3>Import Completed</h3>
          </div>
          <div className="result-stats">
            <div className="stat-item">
              <span className="stat-label">Exams Created:</span>
              <span className="stat-value">{uploadResult.exams_created}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Exams Updated:</span>
              <span className="stat-value">{uploadResult.exams_updated}</span>
            </div>
          </div>
          {uploadResult.errors && uploadResult.errors.length > 0 && (
            <div className="result-errors">
              <h4>Errors:</h4>
              <ul>
                {uploadResult.errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ImportExams;
