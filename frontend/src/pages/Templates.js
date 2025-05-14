import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faUpload, faBook, faCalendarAlt, faUser, faSpinner, faFileExcel, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import './Templates.css';

const TemplateCard = ({ title, description, icon, downloadUrl }) => {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleDownload = () => {
    console.log('Download requested for:', title);
    
    // Add cache-busting timestamp to URL
    const timestamp = new Date().getTime();
    const cacheBustUrl = `${downloadUrl}?t=${timestamp}`;
    console.log('Download URL with cache busting:', cacheBustUrl);
    
    setIsLoading(true);
    
    // Simplified download function for public endpoints
    try {
      // Use axios to download the file
      axios({
        url: cacheBustUrl,
        method: 'GET',
        responseType: 'blob',
        headers: {
          'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        },
        // Add timeout to prevent hanging requests
        timeout: 10000 // 10 seconds
      })
        .then(response => {
          console.log('Response received:', response.status);
          const blob = new Blob([response.data], {
            type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
          });
          
          // Create a link and trigger download
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${title.toLowerCase().replace(/\s+/g, '_')}_template.xlsx`;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
          console.log('Download initiated');
        })
        .catch(error => {
          console.error('Error downloading template:', error);
          alert(`Failed to download template. Please try again later.`);
          
          // Fallback: Try direct window open with cache busting
          const timestamp = new Date().getTime();
          window.open(`${downloadUrl}?t=${timestamp}`, '_blank');
        })
        .finally(() => {
          setIsLoading(false);
        });
    } catch (error) {
      console.error('Unexpected error during download:', error);
      alert(`Download failed. Please try again later.`);
      setIsLoading(false);
    }
  };

  return (
    <div className="template-card">
      <div className="card-header">
        <div className="icon-container">
          {icon}
        </div>
        <h2 className="card-title">{title}</h2>
      </div>
      <div className="card-content">
        <p className="card-description">{description}</p>
      </div>
      <div className="card-actions">
        <button 
          className="download-button" 
          onClick={handleDownload}
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <FontAwesomeIcon icon={faSpinner} className="button-icon fa-spin" />
              Downloading...
            </>
          ) : (
            <>
              <FontAwesomeIcon icon={faDownload} className="button-icon" />
              Download Template
            </>
          )}
        </button>
      </div>
    </div>
  );
};



const Templates = () => {
  const { currentUser } = useAuth();
  // Direct API URLs for template downloads using public endpoints that don't require authentication
  const templates = [
    {
      title: 'Course Template',
      description: 'Excel template for adding or updating course information. Includes fields for course name, professor, faculty, and other details.',
      icon: <FontAwesomeIcon icon={faBook} className="template-icon" />,
      downloadUrl: `http://127.0.0.1:8000/api/v1/public/templates/course`
    },
    {
      title: 'Exam Template',
      description: 'Excel template for adding or updating exam information. Includes fields for faculty, specialization, course, date, time, room, and status.',
      icon: <FontAwesomeIcon icon={faCalendarAlt} className="template-icon" />,
      // Use dedicated download endpoint
      downloadUrl: `http://127.0.0.1:8000/api/v1/downloads/exam-template?t=${new Date().getTime()}`
    },
    {
      title: 'Student Template',
      description: 'Excel template for adding or updating student information. Includes fields for student name, email, group, and other details.',
      icon: <FontAwesomeIcon icon={faUser} className="template-icon" />,
      downloadUrl: `http://127.0.0.1:8000/api/v1/public/templates/student`
    }
  ];

  return (
    <div className="templates-container">
      <div className="templates-header">
        <h1>Excel Templates</h1>
        <p>
          Download Excel templates for managing data in the Exam Planning System. These templates can be used to prepare data for import into the system.
        </p>
      </div>

      <div className="templates-grid">
        {templates.map((template, index) => (
          <div key={index} className="template-grid-item">
            <TemplateCard {...template} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Templates;
