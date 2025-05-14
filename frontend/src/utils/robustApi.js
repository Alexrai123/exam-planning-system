import axios from 'axios';
import { API_URL } from '../config';

// Create axios instance with base URL
const robustApi = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  // Add a longer timeout to prevent quick network errors
  timeout: 10000,
});

// Add request interceptor to add auth token to requests
robustApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Log outgoing requests for debugging
    console.log(`API Request: ${config.method.toUpperCase()} ${config.baseURL}${config.url}`);
    
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor to handle common errors
robustApi.interceptors.response.use(
  (response) => {
    // Log successful responses for debugging
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  async (error) => {
    // Log error details for debugging
    console.error('API Error:', error.message || 'Unknown error');
    
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error(`Error response: ${error.response.status}`, 
                   error.response.data ? JSON.stringify(error.response.data) : 'No response data');
      
      // Handle 401 Unauthorized errors (expired token)
      if (error.response.status === 401) {
        console.warn('Unauthorized access, clearing token');
        localStorage.removeItem('token');
        window.location.href = '/';
      }
      
      // Handle 500 Internal Server Error
      if (error.response.status === 500) {
        console.error('Server error detected. This might be a backend issue.');
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received from server. The server might be down or unreachable.');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Request setup error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// Wrapper functions with retry logic
const MAX_RETRIES = 5; // Increase max retries
const RETRY_DELAY = 2000; // 2 seconds - increase delay between retries

// Helper function to delay execution
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// GET request with retry logic
export const get = async (url, config = {}, retries = MAX_RETRIES) => {
  try {
    return await robustApi.get(url, config);
  } catch (error) {
    // Retry on network errors, 500 errors, or if no response was received
    const shouldRetry = retries > 0 && (
      !error.response || // Network error
      error.response.status >= 500 || // Server error
      error.code === 'ECONNABORTED' // Timeout
    );
    
    if (shouldRetry) {
      console.log(`Retrying GET request to ${url}, ${retries} retries left`);
      await delay(RETRY_DELAY);
      return get(url, config, retries - 1);
    }
    throw error;
  }
};

// POST request with retry logic
export const post = async (url, data = {}, config = {}, retries = MAX_RETRIES) => {
  try {
    return await robustApi.post(url, data, config);
  } catch (error) {
    // Retry on network errors, 500 errors, or if no response was received
    const shouldRetry = retries > 0 && (
      !error.response || // Network error
      error.response.status >= 500 || // Server error
      error.code === 'ECONNABORTED' // Timeout
    );
    
    if (shouldRetry) {
      console.log(`Retrying POST request to ${url}, ${retries} retries left`);
      await delay(RETRY_DELAY);
      return post(url, data, config, retries - 1);
    }
    throw error;
  }
};

// PUT request with retry logic
export const put = async (url, data = {}, config = {}, retries = MAX_RETRIES) => {
  try {
    return await robustApi.put(url, data, config);
  } catch (error) {
    // Retry on network errors, 500 errors, or if no response was received
    const shouldRetry = retries > 0 && (
      !error.response || // Network error
      error.response.status >= 500 || // Server error
      error.code === 'ECONNABORTED' // Timeout
    );
    
    if (shouldRetry) {
      console.log(`Retrying PUT request to ${url}, ${retries} retries left`);
      await delay(RETRY_DELAY);
      return put(url, data, config, retries - 1);
    }
    throw error;
  }
};

// DELETE request with retry logic
export const del = async (url, config = {}, retries = MAX_RETRIES) => {
  try {
    return await robustApi.delete(url, config);
  } catch (error) {
    // Retry on network errors, 500 errors, or if no response was received
    const shouldRetry = retries > 0 && (
      !error.response || // Network error
      error.response.status >= 500 || // Server error
      error.code === 'ECONNABORTED' // Timeout
    );
    
    if (shouldRetry) {
      console.log(`Retrying DELETE request to ${url}, ${retries} retries left`);
      await delay(RETRY_DELAY);
      return del(url, config, retries - 1);
    }
    throw error;
  }
};

// PATCH request with retry logic
export const patch = async (url, data = {}, config = {}, retries = MAX_RETRIES) => {
  try {
    return await robustApi.patch(url, data, config);
  } catch (error) {
    // Retry on network errors, 500 errors, or if no response was received
    const shouldRetry = retries > 0 && (
      !error.response || // Network error
      error.response.status >= 500 || // Server error
      error.code === 'ECONNABORTED' // Timeout
    );
    
    if (shouldRetry) {
      console.log(`Retrying PATCH request to ${url}, ${retries} retries left`);
      await delay(RETRY_DELAY);
      return patch(url, data, config, retries - 1);
    }
    throw error;
  }
};

export default {
  get,
  post,
  put,
  delete: del,
  patch,
  instance: robustApi
};
