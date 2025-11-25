import axios from 'axios';
import { getToken, logout } from './auth';

const API_URL = '/projects/';

const getAuthHeader = () => {
  const token = getToken();
  if (!token) {
    logout();
    throw new Error('No authentication token found');
  }
  return {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  };
};

const handleAuthError = (error) => {
  if (error.response && (error.response.status === 401 || error.response.status === 403)) {
    logout();
    window.location.href = '/login';
  }
  throw error;
};

export const createProject = async (projectData) => {
  try {
    const response = await axios.post(API_URL, projectData, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const getProjects = async () => {
  try {
    const response = await axios.get(API_URL, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const getProject = async (projectId) => {
  try {
    const response = await axios.get(`${API_URL}${projectId}`, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const deleteProject = async (projectId) => {
  try {
    await axios.delete(`${API_URL}${projectId}`, getAuthHeader());
  } catch (error) {
    handleAuthError(error);
  }
};
