// Test login script to verify authentication
const axios = require('axios');
const fs = require('fs');

const API_URL = 'http://localhost:8000/api/v1';
const email = 'ana.petrescu@student.usv.ro';
const password = 'Student2025!';

async function testLogin() {
  try {
    console.log(`Attempting to login with ${email}`);
    
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await axios.post(`${API_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      timeout: 10000
    });
    
    if (response.data && response.data.access_token) {
      console.log('Login successful!');
      console.log('Token:', response.data.access_token);
      
      // Save token to file for testing
      fs.writeFileSync('token.txt', response.data.access_token);
      
      // Test token by making a request to get user info
      try {
        const userResponse = await axios.get(`${API_URL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${response.data.access_token}`
          }
        });
        
        console.log('User info retrieved successfully:');
        console.log(JSON.stringify(userResponse.data, null, 2));
      } catch (userError) {
        console.error('Error fetching user info:', userError.message);
        if (userError.response) {
          console.error('Response status:', userError.response.status);
          console.error('Response data:', userError.response.data);
        }
      }
    } else {
      console.error('No token in response:', response.data);
    }
  } catch (error) {
    console.error('Login error:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

testLogin();
