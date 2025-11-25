// API configuration for different environments

const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:8000'
  },
  production: {
    // Update this when you deploy your backend
    baseURL: import.meta.env.VITE_API_URL || 'https://your-backend-url.com'
  }
};

const environment = import.meta.env.MODE || 'development';
export const API_BASE_URL = API_CONFIG[environment].baseURL;

// Helper function to get full API endpoint
export const getApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};
