import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload, faSpinner, faFileExcel, faCheck, faTimes, faDownload } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import * as XLSX from 'xlsx';
import './GroupLeadersUpload.css';

const GroupLeadersUpload = ({ onUploadComplete }) => {
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

      // Get token
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        setIsUploading(false);
        return;
      }

      // Upload file
      const response = await axios.post(
        'http://localhost:8000/api/v1/group-leaders/upload',
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      setUploadResult(response.data);
      
      // Call the callback function if provided
      if (onUploadComplete && typeof onUploadComplete === 'function') {
        onUploadComplete();
      }
    } catch (err) {
      console.error('Error uploading file:', err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError(err.message || 'Error uploading file');
      }
    } finally {
      setIsUploading(false);
    }
  };

  const downloadTemplate = () => {
    // Create a sample Excel file template
    const headers = ['Name', 'Email', 'Group'];
    const sampleData = [
      ['John Doe', 'john.doe@student.usv.ro', 'CALC1A'],
      ['Jane Smith', 'jane.smith@student.usv.ro', '3111']
    ];
    
    // Create worksheet with headers and sample data
    const ws = XLSX.utils.aoa_to_sheet([headers, ...sampleData]);
    
    // Set column widths for better readability
    const colWidths = [
      { wch: 20 }, // Name column width
      { wch: 30 }, // Email column width
      { wch: 15 }  // Group column width
    ];
    ws['!cols'] = colWidths;
    
    // Create workbook and add the worksheet
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Group Leaders');
    
    // Generate Excel file and trigger download
    XLSX.writeFile(wb, 'group_leaders_template.xlsx');
  };

  return (
    <div className="group-leaders-upload">
      <div className="upload-header">
        <h3><FontAwesomeIcon icon={faFileExcel} /> Upload Group Leaders</h3>
        <p>
          Upload an Excel file with group leaders information. The file should include the following columns:
          Name, Email (@student.usv.ro), and Group. Each item should be in its own column.
        </p>
        <p className="note">
          <strong>Note:</strong> Groups that already have leaders assigned will be skipped to preserve existing assignments.
        </p>
        <button 
          className="template-button" 
          onClick={downloadTemplate}
        >
          <FontAwesomeIcon icon={faDownload} /> Download Excel Template
        </button>
      </div>

      <div className="upload-form">
        <div className="file-input-container">
          <input 
            type="file" 
            id="group-leaders-file" 
            accept=".xlsx,.xls" 
            onChange={handleFileChange} 
            className="file-input"
          />
          <label htmlFor="group-leaders-file" className="file-input-label">
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
              Upload Group Leaders
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="upload-error">
          <FontAwesomeIcon icon={faTimes} />
          {error}
        </div>
      )}

      {uploadResult && (
        <div className="upload-result">
          <div className="result-header">
            <FontAwesomeIcon icon={faCheck} className="success-icon" />
            <h3>Upload Completed</h3>
          </div>
          <div className="result-stats">
            <div className="stat-item">
              <span className="stat-label">Users Created:</span>
              <span className="stat-value">{uploadResult.created_users}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Groups Updated:</span>
              <span className="stat-value">{uploadResult.updated_groups}</span>
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

export default GroupLeadersUpload;
