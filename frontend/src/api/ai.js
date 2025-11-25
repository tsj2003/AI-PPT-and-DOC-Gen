import axios from 'axios';
import { getToken, logout } from './auth';
import { getApiUrl } from '../config/api';

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

export const generateTitle = async (topic) => {
  try {
    const response = await axios.post(getApiUrl('/ai/generate-title/'), {
      topic
    }, getAuthHeader());
    return response.data.title;
  } catch (error) {
    return handleAuthError(error);
  }
};

export const generateOutline = async (topic, documentType, numSections = 5) => {
  try {
    const response = await axios.post(getApiUrl('/ai/generate-outline/'), {
      topic,
      document_type: documentType,
      num_sections: numSections
    }, getAuthHeader());
    return response.data.sections;
  } catch (error) {
    return handleAuthError(error);
  }
};

export const generateSlideImage = async (prompt, enableImage = true) => {
  try {
    const response = await axios.post(getApiUrl('/ai/generate-slide-image/'), {
      prompt,
      enable_image: enableImage
    }, getAuthHeader());
    return response.data;
  } catch (error) {
    return handleAuthError(error);
  }
};
