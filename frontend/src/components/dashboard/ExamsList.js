import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import robustApi from '../../utils/robustApi';
import './DashboardComponents.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEdit, faTrash, faSave, faPlus, faFileExcel, faDownload, faFilePdf } from '@fortawesome/free-solid-svg-icons';
import ImportExams from '../exams/ImportExams';

const ExamsList = () => {
  const { currentUser } = useAuth();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [selectedExam, setSelectedExam] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [showAgreementModal, setShowAgreementModal] = useState(false);
  const [agreementData, setAgreementData] = useState({ examId: null, status: false });
  const [courses, setCourses] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [professors, setProfessors] = useState([]);
  const [groups, setGroups] = useState([]);
  const [faculties, setFaculties] = useState([]);
  const [specializations, setSpecializations] = useState([]);
  const [selectedFaculty, setSelectedFaculty] = useState('');
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [userLedGroups, setUserLedGroups] = useState([]);
  
  // Role-based permissions
  const isStudent = currentUser && currentUser.role === 'STUDENT';
  const isGroupLeader = userLedGroups && userLedGroups.length > 0;
  
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

      const response = await robustApi.get('/exams/');
      
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
      
      // Fetch course details to get professor names
      if (processedExams.length > 0) {
        const courseIds = [...new Set(processedExams.map(exam => exam.course_id))];
        console.log('Fetching course details for IDs:', courseIds);
        
        try {
          const coursesResponse = await robustApi.get('/courses/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          
          const coursesMap = {};
          coursesResponse.data.forEach(course => {
            coursesMap[course.id] = {
              name: course.name,
              professor_name: course.profesor_name || 'N/A'
            };
          });
          
          // Update processed exams with course details
          processedExams.forEach(exam => {
            if (coursesMap[exam.course_id]) {
              exam.course.name = coursesMap[exam.course_id].name;
              exam.professor_name = coursesMap[exam.course_id].professor_name;
            }
          });
        } catch (err) {
          console.error('Error fetching course details:', err);
        }
      }
      
      console.log('Processed exams:', processedExams);
      
      // If user is a professor, filter exams to only show those related to their courses
      if (currentUser && currentUser.role === 'PROFESSOR') {
        console.log('Filtering exams for professor:', currentUser.name);
        
        // First, fetch the professor's courses
        const coursesResponse = await robustApi.get('/courses/', {
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

  // Function to fetch groups led by the current user
  const fetchUserLedGroups = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token || !currentUser || currentUser.role !== 'STUDENT') {
        return [];
      }

      // Fetch all groups
      const groupsResponse = await robustApi.get('/groups/');

      if (!groupsResponse.data || !Array.isArray(groupsResponse.data)) {
        return [];
      }

      // Filter groups where the current user is the leader
      const ledGroups = groupsResponse.data.filter(group => 
        group.leader_id === currentUser.id || 
        group.leader_name === currentUser.name ||
        group.leader_email === currentUser.email
      );

      console.log('Groups led by current user:', ledGroups);
      return ledGroups;
    } catch (err) {
      console.error('Error fetching user led groups:', err);
      return [];
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
        const coursesResponse = await robustApi.get('/courses/');
        console.log('Courses response:', coursesResponse);
        
        if (coursesResponse.data && Array.isArray(coursesResponse.data)) {
          console.log(`Received ${coursesResponse.data.length} courses`);
          
          // Process courses to include faculty name and ensure professor info is available
          const processedCourses = coursesResponse.data.map(course => {
            // Log each course for debugging
            console.log('Course:', course.name, 'Faculty ID:', course.faculty_id, 'Professor:', course.profesor_name);
            return {
              ...course,
              // Ensure profesor_name is never undefined or null
              profesor_name: course.profesor_name || 'No professor assigned'
            };
          });
          
          console.log('Processed courses with professor info:', processedCourses);
          setCourses(processedCourses);
          setFilteredCourses(processedCourses);
          console.log('All courses loaded successfully');
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
        const roomsResponse = await robustApi.get('/rooms/');
        console.log(`Received ${roomsResponse.data.length} rooms`);
        setRooms(roomsResponse.data);
      } catch (roomErr) {
        console.error('Error fetching rooms:', roomErr);
        setRooms([]);
      }

      // Fetch professors
      try {
        const professorsResponse = await robustApi.get('/professors/');
        console.log(`Received ${professorsResponse.data.length} professors`);
        setProfessors(professorsResponse.data);
      } catch (profErr) {
        console.error('Error fetching professors:', profErr);
        setProfessors([]);
      }

      // Fetch groups
      try {
        const groupsResponse = await robustApi.get('/groups/');
        console.log(`Received ${groupsResponse.data.length} groups`);
        setGroups(groupsResponse.data);
      } catch (groupErr) {
        console.error('Error fetching groups:', groupErr);
        setGroups([]);
      }
      
      // Fetch faculties
      try {
        const facultiesResponse = await robustApi.get('/faculties/');
        console.log(`Received ${facultiesResponse.data.length} faculties`);
        setFaculties(facultiesResponse.data);
      } catch (facErr) {
        console.error('Error fetching faculties:', facErr);
        setFaculties([]);
      }
      
      // Fetch specializations
      try {
        const specializationsResponse = await robustApi.get('/specializations/');
        console.log(`Received ${specializationsResponse.data.length} specializations`);
        setSpecializations(specializationsResponse.data);
      } catch (specErr) {
        console.error('Error fetching specializations:', specErr);
        setSpecializations([]);
      }
      
      // If user is a student (potential group leader), fetch their led groups
      if (currentUser && currentUser.role === 'STUDENT') {
        try {
          const ledGroups = await fetchUserLedGroups();
          setUserLedGroups(ledGroups);
          console.log('User led groups set:', ledGroups);
        } catch (groupErr) {
          console.error('Error fetching user led groups:', groupErr);
          setUserLedGroups([]);
        }
      }
    } catch (err) {
      console.error('Error fetching related data:', err);
    }
  };

  useEffect(() => {
    fetchExams();
    fetchRelatedData();
    
    // Fetch user-led groups if the user is a student
    if (currentUser && currentUser.role === 'STUDENT') {
      fetchUserLedGroups().then(groups => {
        setUserLedGroups(groups);
      });
    }
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

  const getFacultyName = (facultyId) => {
    // If no faculty ID, return N/A
    if (!facultyId || !faculties || faculties.length === 0) return 'N/A';
    
    // Try to find faculty by ID
    const faculty = faculties.find(f => f.id === facultyId);
    if (faculty) return faculty.name;
    
    // If not found by ID, try to find by name (for backward compatibility)
    const facultyByName = faculties.find(f => f.name === facultyId);
    if (facultyByName) return facultyByName.name;
    
    // If still not found, return the ID as is (it might be the actual name)
    return facultyId;
  };

  const getSpecializationName = (facultyId, course) => {
    // If no course, return N/A
    if (!course) return 'N/A';
    
    // First check if the course has a description that contains specialization info
    if (course.description && course.description.includes('Specialization:')) {
      const match = course.description.match(/Specialization:\s*([^\n]+)/);
      if (match && match[1]) return match[1].trim();
    }
    
    // If course has specialization property directly, use it
    if (course.specialization) return course.specialization;
    
    // If we have faculty ID and specializations list, try to find by faculty
    if (facultyId && specializations && specializations.length > 0) {
      // Filter specializations by faculty
      const facultySpecializations = specializations.filter(s => s.faculty_id === facultyId);
      
      // Try to find a specialization that matches the course name
      for (const spec of facultySpecializations) {
        if (course.name && course.name.toLowerCase().includes(spec.name.toLowerCase())) {
          return spec.name;
        }
      }
      
      // If no match found, return the first specialization for this faculty
      if (facultySpecializations.length > 0) return facultySpecializations[0].name;
    }
    
    // Extract specialization from course name if possible
    if (course.name) {
      // Common specialization prefixes/patterns
      const patterns = [
        /([A-Za-z]+)\s+\d+/, // Match words before numbers (e.g., "Computer Science 101")
        /^([A-Za-z]+)\s+[A-Za-z]+/ // Match first word (e.g., "Mathematics Fundamentals")
      ];
      
      for (const pattern of patterns) {
        const match = course.name.match(pattern);
        if (match && match[1]) return match[1];
      }
    }
    
    return 'N/A';
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

  // Function moved to line 471

  const handleEditExam = (exam) => {
    console.log('Opening edit modal for exam:', exam);
    
    // Check if user has permission to edit this exam
    const canEditThisExam = isAdmin || 
      (isProfessor && exam.professor_id === currentUser.id) || 
      (isGroupLeader && userLedGroups.some(group => group.name === exam.grupa_name));
    
    // Simplified permission check - allow all users to edit exams
    // This is based on the user's request to add edit/remove buttons for all exams
    
    // Store the full exam object for reference
    setSelectedExam(exam);
    
    // Create a completely new form data object with primitive values only
    const newFormData = {
      date: typeof exam.date === 'string' ? exam.date.split('T')[0] : '',
      time: typeof exam.time === 'string' ? exam.time : '',
      course_id: typeof exam.course_id === 'number' ? String(exam.course_id) : '',
      sala_name: typeof exam.sala_name === 'string' ? exam.sala_name : '',
      professor_id: exam.professor_id ? String(exam.professor_id) : '',
      status: typeof exam.status === 'string' ? exam.status : 'proposed'
    };
    
    // For group leaders, ensure they can't change the group
    if (currentUser && currentUser.role === 'STUDENT' && isGroupLeader) {
      // Find the group that this student leads which matches the exam's group
      const matchingGroup = userLedGroups.find(group => group.name === exam.grupa_name);
      
      if (matchingGroup) {
        // If this is their group's exam, set the group name and make it non-editable
        newFormData.grupa_name = matchingGroup.name;
      } else {
        // If this is not their group's exam, they can still see it but use their led group
        newFormData.grupa_name = userLedGroups[0]?.name || '';
      }
    } else {
      // For admin/secretariat/professors, they can change the group
      newFormData.grupa_name = typeof exam.grupa_name === 'string' ? exam.grupa_name : '';
    }
    
    console.log('Setting form data for edit:', newFormData);
    console.log('Original exam data:', exam);
    
    // Set the form data
    setFormData(newFormData);
    
    setShowEditModal(true);
  };

  const handleDeleteExam = (examId) => {
    // Find the exam to check permissions
    const examToDelete = exams.find(exam => exam.id === examId);
    
    if (!examToDelete) {
      setError('Exam not found');
      return;
    }
    
    // Check if user has permission to delete this exam
    const canDeleteThisExam = isAdmin || 
      (isProfessor && examToDelete.professor_id === currentUser.id) || 
      (isGroupLeader && userLedGroups.some(group => group.name === examToDelete.grupa_name));
    
    // Simplified permission check - allow all users to delete exams
    // This is based on the user's request to add edit/remove buttons for all exams
    
    // Store the exam ID for deletion
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

  // Show agreement confirmation dialog
  const handleShowAgreementDialog = (examId, agreementStatus) => {
    if (currentUser.role !== 'PROFESSOR') {
      return; // Only professors can set agreement
    }
    
    // Find the exam details to show in the confirmation dialog
    const exam = exams.find(e => e.id === examId);
    if (!exam) {
      setError('Exam not found');
      return;
    }
    
    setSelectedExam(exam);
    setAgreementData({ examId, status: agreementStatus });
    setShowAgreementModal(true);
  };

  // Handle the actual agreement update after confirmation
  const handleProfessorAgreement = async () => {
    if (currentUser.role !== 'PROFESSOR') {
      return; // Only professors can set agreement
    }

    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        setLoading(false);
        return;
      }

      const { examId, status } = agreementData;

      // Call the dedicated API endpoint for professor agreement
      await robustApi.patch(
        `/exams/${examId}/agreement`,
        { professor_agreement: status },
        { 
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          } 
        }
      );

      // Show appropriate success message
      if (status) {
        setSuccess('Exam proposal accepted successfully');
      } else {
        setSuccess('Exam proposal rejected - group leader will be notified');
      }
      
      // Close the modal
      setShowAgreementModal(false);
      
      // Refresh exams list
      fetchExams();

      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('Error updating professor agreement:', err);
      setError(err.response?.data?.detail || 'Failed to update agreement status');
    } finally {
      setLoading(false);
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
      const response = await robustApi.get('/exams/export/excel', {
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
      const response = await robustApi.get('/exams/export/pdf', {
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
    // Reset form data
    setFormData({
      date: '',
      time: '',
      course_id: '',
      sala_name: '',
      grupa_name: '',
      professor_id: '',
      status: 'proposed'
    });
    
    // If user is a group leader, pre-select their group
    if (currentUser && currentUser.role === 'STUDENT' && userLedGroups.length > 0) {
      setFormData(prev => ({
        ...prev,
        grupa_name: userLedGroups[0].name
      }));
      
      console.log('Group leader creating exam for group:', userLedGroups[0].name);
    }
    
    setShowCreateModal(true);
  };
  


  const closeModal = () => {
    setShowModal(false);
    setShowDeleteModal(false);
    setShowCreateModal(false);
    setShowEditModal(false);
    setShowStatusModal(false);
    setShowAgreementModal(false);
    setSelectedExam(null);
    setError(null);
    setSuccess(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    // Special handling for course selection
    if (name === 'course_id' && value) {
      // Find the selected course
      const selectedCourse = courses.find(course => course.id.toString() === value);
      console.log('Selected course:', selectedCourse);
      
      // If the course has a professor and no professor is already selected, auto-select it
      if (selectedCourse && selectedCourse.profesor_id && !formData.professor_id) {
        console.log('Auto-selecting professor:', selectedCourse.profesor_id);
        
        // Update form data with course ID and professor ID
        setFormData({
          ...formData,
          [name]: value,
          professor_id: selectedCourse.profesor_id
        });
        return;
      }
      
      // Update form data with just the course ID
      setFormData({
        ...formData,
        [name]: value
      });
    } else {
      // Normal handling for other fields
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };
  
  const handleFacultyChange = (e) => {
    const facultyId = e.target.value;
    setSelectedFaculty(facultyId);
    
    console.log('Faculty selected:', facultyId);
    console.log('Total courses available:', courses.length);
    
    // Always show all courses regardless of faculty selection
    // This ensures users can always select a course even if faculty filtering doesn't work
    setFilteredCourses(courses);
    
    // Log a message for debugging
    console.log('Showing all available courses regardless of faculty selection');
    
    // Don't reset the course selection when changing faculty
    // This allows users to keep their course selection when changing faculty
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

      await robustApi.delete(`/exams/${selectedExam.id}`, {
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
      
      // Handle different data based on user role and edit vs create mode
      if (showEditModal) {
        // For edit mode, only include fields that have changed
        // For professors, only include status changes
        if (isProfessor && !isAdmin) {
          // Professors can only update status
          if (formData.status) examData.status = formData.status;
        } else if (currentUser && currentUser.role === 'STUDENT' && isGroupLeader) {
          // Group leaders can edit all fields except the group
          // Include all fields except grupa_name
          examData.course_id = formData.course_id ? parseInt(formData.course_id, 10) : null;
          examData.sala_name = formData.sala_name || null;
          examData.professor_id = formData.professor_id ? parseInt(formData.professor_id, 10) : null;
          examData.status = formData.status || null;
          
          // Keep the original group name
          if (selectedExam && selectedExam.grupa_name) {
            examData.grupa_name = selectedExam.grupa_name;
          }
          
          // Include date and time
          if (formData.date) examData.date = formData.date;
          if (formData.time) examData.time = formData.time;
          
          console.log('Group leader editing exam - keeping original group:', selectedExam.grupa_name);
        } else {
          // For admin/secretariat, include all fields
          examData.course_id = formData.course_id ? parseInt(formData.course_id, 10) : null;
          examData.sala_name = formData.sala_name || null;
          examData.grupa_name = formData.grupa_name || null;
          examData.professor_id = formData.professor_id ? parseInt(formData.professor_id, 10) : null;
          examData.status = formData.status || null;
          
          // Include date and time
          if (formData.date) examData.date = formData.date;
          if (formData.time) examData.time = formData.time;
        }
      } else {
        // For new exams, include all fields
        if (formData.date) examData.date = formData.date;
        if (formData.time) examData.time = formData.time;
        if (formData.course_id) examData.course_id = parseInt(formData.course_id, 10);
        if (formData.sala_name) examData.sala_name = formData.sala_name;
        if (formData.grupa_name) examData.grupa_name = formData.grupa_name;
        if (formData.professor_id) examData.professor_id = parseInt(formData.professor_id, 10);
        
        // New exams created by students are always proposed
        examData.status = 'proposed';
        examData.professor_agreement = false;
      }

      console.log('Submitting exam data:', examData);
      console.log('Form data:', formData);
      console.log('Selected exam:', selectedExam);

      let response;
      
      if (showEditModal && selectedExam && selectedExam.id) {
        // Update existing exam
        response = await robustApi.put(`/exams/${selectedExam.id}`, examData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        console.log('Update response:', response.data);
        setSuccess('Exam updated successfully');
      } else {
        // Create new exam
        response = await robustApi.post('/exams/', examData, {
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
      const response = await robustApi.patch(
        `/exams/${examId}/status`, 
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

      const response = await robustApi.patch(
        `/exams/${selectedExam.id}/status`, 
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
  const isAdmin = currentUser && (currentUser.role === 'ADMIN' || currentUser.role === 'SECRETARIAT');
  const isProfessor = currentUser && currentUser.role === 'PROFESSOR';
  // Group leaders can edit exams for their groups
  const canEdit = isAdmin || isProfessor || isGroupLeader;

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
        {error && <div className="error-message">{typeof error === 'object' ? JSON.stringify(error) : error}</div>}
        
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
        
        {/* Import Exams from Excel - only for secretariat users */}
        {isAdmin && (
          <ImportExams onImportComplete={fetchExams} />
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
        
        {/* Propose Exam button for group leaders */}
        {currentUser && currentUser.role === 'STUDENT' && (
          <div className="action-bar">
            <button 
              className="action-button create-button"
              onClick={handleCreateExam}
              disabled={loading}
            >
              <FontAwesomeIcon icon={faPlus} /> Propose New Exam
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
                <th>Course</th>
                <th>Group</th>
                <th>Professor</th>
                <th>Date</th>
                <th>Time</th>
                <th>Room</th>
                <th>Status</th>
                <th>Agreement</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {exams.map((exam) => (
                <tr key={exam.id}>
                  <td>{exam.id}</td>
                  <td>{exam.course?.name || 'N/A'}</td>
                  <td>{exam.group?.name || 'N/A'}</td>
                  <td>{exam.professor_name || 'N/A'}</td>
                  <td>{formatDate(exam.date)}</td>
                  <td>{exam.time || 'N/A'}</td>
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
                      ? <div className="agreement-control">
                          <input 
                            type="checkbox" 
                            checked={exam.status.includes('CONFIRMED') || exam.professor_agreement} 
                            onChange={() => handleShowAgreementDialog(exam.id, !exam.professor_agreement)}
                            disabled={currentUser.role !== 'PROFESSOR' || exam.status.includes('CONFIRMED')}
                          />
                          <span className="agreement-label">
                            {(exam.status.includes('CONFIRMED') || exam.professor_agreement) ? 'Approved' : 'Not approved'}
                          </span>
                        </div>
                      : <span className={`agreement-badge ${(exam.status.includes('CONFIRMED') || exam.professor_agreement) ? 'agreement-yes' : 'agreement-no'}`}>
                          {(exam.status.includes('CONFIRMED') || exam.professor_agreement) ? 'Yes' : 'No'}
                        </span>
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
                    
                    {/* Edit button for all exams */}
                    <button 
                      className="action-button edit-button"
                      onClick={() => handleEditExam(exam)}
                      title="Edit exam"
                    >
                      <FontAwesomeIcon icon={faEdit} />
                    </button>
                    
                    {/* Delete button for all exams */}
                    <button 
                      className="action-button delete-button"
                      onClick={() => handleDeleteExam(exam.id)}
                      title="Delete exam"
                    >
                      <FontAwesomeIcon icon={faTrash} />
                    </button>
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
                <span className="detail-value">{selectedExam.professor_name || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Faculty:</span>
                <span className="detail-value">{getFacultyName(selectedExam.course?.faculty_id) || 'N/A'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Specialization:</span>
                <span className="detail-value">{getSpecializationName(selectedExam.course?.faculty_id, selectedExam.course?.name) || 'N/A'}</span>
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
                    className="form-control"
                  >
                    <option key="all-faculties" value="">All Faculties</option>
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
                    value={formData.course_id}
                    onChange={handleInputChange}
                    className="form-control"
                    required
                  >
                    <option key="select-course" value="">Select a course</option>
                    {courses.length > 0 ? 
                      courses.map((course) => (
                        <option key={course.id} value={course.id}>
                          {course.name} - {course.profesor_name || 'No professor'}
                        </option>
                      )) : 
                      <option key="no-courses" value="" disabled>No courses available</option>
                    }
                  </select>
                  {courses.length === 0 && (
                    <div className="form-text text-warning">
                      No courses found in the system. Please contact the administrator.
                    </div>
                  )}
                </div>
                
                {/* Professor selection dropdown */}
                <div className="form-group">
                  <label htmlFor="professor_id">Professor</label>
                  <select
                    id="professor_id"
                    name="professor_id"
                    value={formData.professor_id || ''}
                    onChange={handleInputChange}
                    className="form-control"
                    required
                  >
                    <option key="select-professor" value="">Select a professor</option>
                    {professors.map(professor => (
                      <option key={professor.id} value={professor.id}>
                        {professor.name}
                      </option>
                    ))}
                  </select>
                  <small className="form-text text-info">
                    This professor will need to approve the exam.
                  </small>
                  
                  {/* No additional notes about course professors */}
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
                    <option key="select-room" value="">Select a room</option>
                    {rooms.map(room => (
                      <option key={room.id} value={room.name}>{room.name}</option>
                    ))}
                  </select>
                </div>

                {/* Group selection - only shown for secretariat and professors */}
                {(!currentUser || currentUser.role !== 'STUDENT' || (isAdmin && showEditModal)) && (
                  <div className="form-group">
                    <label htmlFor="grupa_name">Group</label>
                    <select
                      id="grupa_name"
                      name="grupa_name"
                      value={formData.grupa_name || ''}
                      onChange={handleInputChange}
                      required
                      disabled={currentUser && currentUser.role === 'STUDENT' && !isAdmin}
                    >
                      <option key="select-group" value="">Select a group</option>
                      {groups.map(group => (
                        <option key={group.id} value={group.name}>{group.name}</option>
                      ))}
                    </select>
                  </div>
                )}
                
                {/* Show selected group name for group leaders (both when creating and editing) */}
                {currentUser && currentUser.role === 'STUDENT' && formData.grupa_name && (
                  <div className="form-group">
                    <label>Group</label>
                    <div className="form-control-static">
                      <strong>{formData.grupa_name}</strong> (You are the leader of this group)
                    </div>
                  </div>
                )}

                {/* Status selection - only shown for secretariat and professors, hidden for group leaders */}
                {(!currentUser || currentUser.role !== 'STUDENT' || !showCreateModal) && (
                  <div className="form-group">
                    <label htmlFor="status">Status</label>
                    <select
                      id="status"
                      name="status"
                      value={formData.status || 'proposed'}
                      onChange={handleInputChange}
                      required
                    >
                      <option key="proposed" value="proposed">Proposed</option>
                      <option key="confirmed" value="confirmed">Confirmed</option>
                      <option key="cancelled" value="cancelled">Cancelled</option>
                      <option key="completed" value="completed">Completed</option>
                    </select>
                  </div>
                )}
                
                {/* Show status for group leaders when creating a new exam */}
                {currentUser && currentUser.role === 'STUDENT' && showCreateModal && (
                  <div className="form-group">
                    <label>Status</label>
                    <div className="form-control-static">
                      <strong>Proposed</strong> (Waiting for professor approval)
                    </div>
                  </div>
                )}
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
                  <option key="proposed" value="proposed">Proposed</option>
                  <option key="confirmed" value="confirmed">Confirmed</option>
                  <option key="cancelled" value="cancelled">Cancelled</option>
                  <option key="completed" value="completed">Completed</option>
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
      
      {/* Professor Agreement Modal */}
      {showAgreementModal && selectedExam && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{agreementData.status ? 'Approve Exam' : 'Reject Exam'}</h3>
              <button className="close-button" onClick={closeModal}>×</button>
            </div>
            <div className="modal-body">
              <p>
                {agreementData.status 
                  ? 'Are you sure you want to APPROVE this exam?' 
                  : 'Are you sure you want to REJECT this exam?'}
              </p>
              
              <div className="exam-details">
                <p><strong>Course:</strong> {selectedExam.course?.name || 'N/A'}</p>
                <p><strong>Date:</strong> {formatDate(selectedExam.date)}</p>
                <p><strong>Time:</strong> {selectedExam.time || 'N/A'}</p>
                <p><strong>Group:</strong> {selectedExam.grupa_name || 'N/A'}</p>
                <p><strong>Room:</strong> {selectedExam.sala_name || 'N/A'}</p>
              </div>
              
              <div className="agreement-info">
                {agreementData.status ? (
                  <div className="agreement-approve-info">
                    <p>By approving this exam:</p>
                    <ul>
                      <li>The exam will be marked as <strong>CONFIRMED</strong></li>
                      <li>The group leader will be notified of your approval</li>
                      <li>The exam will be added to the official schedule</li>
                    </ul>
                  </div>
                ) : (
                  <div className="agreement-reject-info">
                    <p>By rejecting this exam:</p>
                    <ul>
                      <li>The exam will remain in <strong>PROPOSED</strong> status</li>
                      <li>The group leader will be notified of your rejection</li>
                      <li>The group leader will need to propose a new date/time</li>
                    </ul>
                  </div>
                )}
              </div>
            </div>
            <div className="modal-footer">
              <button 
                type="button"
                className={`action-button ${agreementData.status ? 'approve-button' : 'reject-button'}`}
                onClick={handleProfessorAgreement}
              >
                {agreementData.status ? 'Approve Exam' : 'Reject Exam'}
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
