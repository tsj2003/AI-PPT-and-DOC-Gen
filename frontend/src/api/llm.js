import axios from 'axios';
import { getToken, logout } from './auth';

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

export const generateContent = async (sectionId, additionalContext = null) => {
  try {
    const response = await axios.post('/generate/', {
      section_id: sectionId,
      additional_context: additionalContext
    }, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const refineContent = async (sectionId, refinePrompt) => {
  try {
    const response = await axios.post('/refine/', {
      section_id: sectionId,
      refine_prompt: refinePrompt
    }, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const addFeedback = async (sectionId, isLiked) => {
  try {
    const response = await axios.post('/feedback/', {
      section_id: sectionId,
      is_liked: isLiked
    }, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const addComment = async (sectionId, content) => {
  try {
    const response = await axios.post('/comments/', {
      section_id: sectionId,
      content
    }, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const getComments = async (sectionId) => {
  try {
    const response = await axios.get(`/sections/${sectionId}/comments/`, getAuthHeader());
    return response.data;
  } catch (error) {
    handleAuthError(error);
  }
};

export const exportProject = async (projectId, includeImages = false) => {
  try {
    const config = {
      ...getAuthHeader(),
      responseType: 'blob'
    };
    let url = `/export/${projectId}/`;
    if (includeImages) {
      url += `?include_images=true`;
    }
    const response = await axios.get(url, config);
    return response;
  } catch (error) {
    handleAuthError(error);
  }
};
