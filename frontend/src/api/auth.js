import axios from 'axios';
import { getApiUrl } from '../config/api';

const API_URL = getApiUrl('/auth');
console.log('Auth API URL:', API_URL);

export const register = async (email, username, password) => {
  try {
    console.log('Attempting register to:', `${API_URL}/register`);
    console.log('Register payload:', { email, username, password: '***' });
    
    const response = await axios.post(`${API_URL}/register`, {
      email,
      username,
      password
    });
    
    console.log('Register response:', response.data);
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  } catch (error) {
    console.error('Register error:', error);
    console.error('Error details:', {
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url,
      message: error.response?.data?.detail || error.message
    });
    
    // Show user-friendly error message
    const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
    
    if (error.response?.status === 400) {
      if (errorMessage.includes('already registered')) {
        alert('Registration failed: This email or username is already registered. Please try logging in instead.');
      } else {
        alert(`Registration Error: ${errorMessage}`);
      }
    } else {
      alert(`Registration Error: ${errorMessage}`);
    }
    throw error;
  }
};

export const login = async (username, password) => {
  try {
    console.log('Attempting login to:', `${API_URL}/login`);
    console.log('Login payload:', { username, password: '***' });
    
    const response = await axios.post(`${API_URL}/login`, {
      username,
      password
    });
    
    console.log('Login response:', response.data);
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    console.error('Error details:', {
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url,
      message: error.response?.data?.detail || error.message
    });
    
    // Show user-friendly error message
    const errorMessage = error.response?.data?.detail || 'Login failed. Please check your credentials.';
    
    if (error.response?.status === 401) {
      if (errorMessage.includes('Incorrect username or password')) {
        alert('Login failed: Invalid username or password. Please check your credentials or create a new account if you haven\'t registered yet.');
      } else {
        alert(`Authentication Error: ${errorMessage}`);
      }
    } else {
      alert(`Login Error: ${errorMessage}`);
    }
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const getToken = () => {
  return localStorage.getItem('token');
};

export const isAuthenticated = () => {
  return !!getToken();
};
