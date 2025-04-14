const axios = require('axios');

// Use a token for a secretariat user
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzEzMTIzMDAwfQ.gYxG9oL_HxYFvPwqgXt1xRYFkJJR1JlzBCkS-5ogmX0';
const API_URL = 'http://localhost:8000/api/v1';

const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};

// Function to add a course
const addCourse = async (course) => {
  try {
    const response = await axios.post(`${API_URL}/courses/`, course, { headers });
    console.log(`Added course: ${course.name}`);
    return response.data;
  } catch (err) {
    console.error(`Failed to add course ${course.name}:`, err.message);
    return null;
  }
};

// Function to add a room
const addRoom = async (room) => {
  try {
    const response = await axios.post(`${API_URL}/rooms/`, room, { headers });
    console.log(`Added room: ${room.name}`);
    return response.data;
  } catch (err) {
    console.error(`Failed to add room ${room.name}:`, err.message);
    return null;
  }
};

// Function to add a group
const addGroup = async (group) => {
  try {
    const response = await axios.post(`${API_URL}/groups/`, group, { headers });
    console.log(`Added group: ${group.name}`);
    return response.data;
  } catch (err) {
    console.error(`Failed to add group ${group.name}:`, err.message);
    return null;
  }
};

// Function to add an exam
const addExam = async (exam) => {
  try {
    const response = await axios.post(`${API_URL}/exams/`, exam, { headers });
    console.log(`Added exam for course ID: ${exam.course_id}`);
    return response.data;
  } catch (err) {
    console.error(`Failed to add exam:`, err.message);
    return null;
  }
};

// Sample courses data
const courses = [
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
const rooms = [
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
const groups = [
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

// Main function to add all data
const addAllData = async () => {
  try {
    console.log('Starting to add sample data...');
    
    // Add courses
    const addedCourses = [];
    for (const course of courses) {
      const result = await addCourse(course);
      if (result) addedCourses.push(result);
    }
    
    // Add rooms
    const addedRooms = [];
    for (const room of rooms) {
      const result = await addRoom(room);
      if (result) addedRooms.push(result);
    }
    
    // Add groups
    const addedGroups = [];
    for (const group of groups) {
      const result = await addGroup(group);
      if (result) addedGroups.push(result);
    }
    
    // Create exams using the added entities
    if (addedCourses.length > 0 && addedRooms.length > 0 && addedGroups.length > 0) {
      const today = new Date();
      
      // Create sample exams
      const exams = [
        {
          date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7).toISOString().split('T')[0],
          time: '09:00:00',
          course_id: addedCourses[0].id,
          sala_id: addedRooms[0].id,
          grupa_id: addedGroups[0].id,
          status: 'proposed'
        },
        {
          date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 8).toISOString().split('T')[0],
          time: '11:00:00',
          course_id: addedCourses[1].id,
          sala_id: addedRooms[1].id,
          grupa_id: addedGroups[1].id,
          status: 'confirmed'
        },
        {
          date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 9).toISOString().split('T')[0],
          time: '14:00:00',
          course_id: addedCourses[2].id,
          sala_id: addedRooms[2].id,
          grupa_id: addedGroups[2].id,
          status: 'proposed'
        },
        {
          date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 10).toISOString().split('T')[0],
          time: '10:00:00',
          course_id: addedCourses[3].id,
          sala_id: addedRooms[3].id,
          grupa_id: addedGroups[3].id,
          status: 'confirmed'
        },
        {
          date: new Date(today.getFullYear(), today.getMonth(), today.getDate() + 11).toISOString().split('T')[0],
          time: '13:00:00',
          course_id: addedCourses[4].id,
          sala_id: addedRooms[4].id,
          grupa_id: addedGroups[4].id,
          status: 'proposed'
        }
      ];
      
      // Add exams
      for (const exam of exams) {
        await addExam(exam);
      }
    }
    
    console.log('All sample data added successfully!');
  } catch (error) {
    console.error('Error adding sample data:', error.message);
  }
};

// Run the function
addAllData();
