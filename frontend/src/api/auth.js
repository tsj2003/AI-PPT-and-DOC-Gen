import axios from 'axios';
import { getApiUrl } from '../config/api';

const API_URL = getApiUrl('/auth');

export const register = async (email, username, password) => {
  const response = await axios.post(`${API_URL}/register`, {
    email,
    username,
    password
  });
  
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  
  return response.data;
};

export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/login`, {
    username,
    password
  });
  
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  
  return response.data;
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
