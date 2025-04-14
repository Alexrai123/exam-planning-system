import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Sample courses data
const sampleCourses = [
  {
    name: 'Introduction to Computer Science',
    description: 'Fundamentals of computer science, including algorithms, data structures, and programming concepts.',
    credits: 6,
    year: 1,
    semester: 1
  },
  {
    name: 'Database Systems',
    description: 'Design and implementation of database systems, SQL, normalization, and transaction management.',
    credits: 5,
    year: 2,
    semester: 1
  },
  {
    name: 'Web Development',
    description: 'Frontend and backend web development technologies, including HTML, CSS, JavaScript, and frameworks.',
    credits: 5,
    year: 2,
    semester: 2
  },
  {
    name: 'Artificial Intelligence',
    description: 'Introduction to AI concepts, machine learning algorithms, and neural networks.',
    credits: 6,
    year: 3,
    semester: 1
  },
  {
    name: 'Software Engineering',
    description: 'Software development methodologies, project management, and quality assurance.',
    credits: 5,
    year: 3,
    semester: 2
  }
];

// Sample rooms data
const sampleRooms = [
  {
    name: 'A101',
    building: 'Building A',
    floor: 1,
    capacity: 120
  },
  {
    name: 'B203',
    building: 'Building B',
    floor: 2,
    capacity: 80
  },
  {
    name: 'C305',
    building: 'Building C',
    floor: 3,
    capacity: 60
  },
  {
    name: 'D102',
    building: 'Building D',
    floor: 1,
    capacity: 100
  },
  {
    name: 'E201',
    building: 'Building E',
    floor: 2,
    capacity: 50
  }
];

// Sample groups data
const sampleGroups = [
  {
    name: '1A',
    year: 1,
    specialization: 'Computer Science'
  },
  {
    name: '2B',
    year: 2,
    specialization: 'Software Engineering'
  },
  {
    name: '3C',
    year: 3,
    specialization: 'Cybersecurity'
  },
  {
    name: '2A',
    year: 2,
    specialization: 'Data Science'
  },
  {
    name: '3A',
    year: 3,
    specialization: 'Artificial Intelligence'
  }
];

// Function to add sample data to the backend
export const addSampleData = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No authentication token found');
      return { success: false, message: 'No authentication token found' };
    }

    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    // Add sample courses
    const coursesPromises = sampleCourses.map(course => 
      axios.post(`${API_URL}/courses/`, course, { headers })
    );
    
    // Add sample rooms
    const roomsPromises = sampleRooms.map(room => 
      axios.post(`${API_URL}/rooms/`, room, { headers })
    );
    
    // Add sample groups
    const groupsPromises = sampleGroups.map(group => 
      axios.post(`${API_URL}/groups/`, group, { headers })
    );
    
    // Wait for all requests to complete
    await Promise.all([
      ...coursesPromises, 
      ...roomsPromises, 
      ...groupsPromises
    ]);
    
    // Now that we have courses, rooms, and groups, we can create exams
    // First, get the IDs of the created entities
    const coursesResponse = await axios.get(`${API_URL}/courses/`, { headers });
    const roomsResponse = await axios.get(`${API_URL}/rooms/`, { headers });
    const groupsResponse = await axios.get(`${API_URL}/groups/`, { headers });
    
    const courses = coursesResponse.data;
    const rooms = roomsResponse.data;
    const groups = groupsResponse.data;
    
    // Create sample exams
    const today = new Date();
    const sampleExams = [
      {
        date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7).toISOString().split('T')[0],
        time: '09:00:00',
        course_id: courses[0]?.id,
        sala_id: rooms[0]?.id,
        grupa_id: groups[0]?.id,
        status: 'proposed'
      },
      {
        date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 8).toISOString().split('T')[0],
        time: '11:00:00',
        course_id: courses[1]?.id,
        sala_id: rooms[1]?.id,
        grupa_id: groups[1]?.id,
        status: 'confirmed'
      },
      {
        date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 9).toISOString().split('T')[0],
        time: '14:00:00',
        course_id: courses[2]?.id,
        sala_id: rooms[2]?.id,
        grupa_id: groups[2]?.id,
        status: 'proposed'
      },
      {
        date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 10).toISOString().split('T')[0],
        time: '10:00:00',
        course_id: courses[3]?.id,
        sala_id: rooms[3]?.id,
        grupa_id: groups[3]?.id,
        status: 'confirmed'
      },
      {
        date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 11).toISOString().split('T')[0],
        time: '13:00:00',
        course_id: courses[4]?.id,
        sala_id: rooms[4]?.id,
        grupa_id: groups[4]?.id,
        status: 'proposed'
      }
    ];
    
    // Add sample exams
    const examsPromises = sampleExams.map(exam => 
      axios.post(`${API_URL}/exams/`, exam, { headers })
    );
    
    await Promise.all(examsPromises);
    
    return { success: true, message: 'Sample data added successfully' };
  } catch (error) {
    console.error('Error adding sample data:', error);
    return { 
      success: false, 
      message: error.response?.data?.detail || 'Failed to add sample data' 
    };
  }
};
