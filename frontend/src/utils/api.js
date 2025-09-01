// API utility functions for HexaCiphers frontend

// Use relative URLs since nginx will proxy /api requests to backend
const API_BASE_URL = '/api';

// Generic API call function
const apiCall = async (endpoint, options = {}) => {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API call failed: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    // Throw error to let components handle API failures properly
    throw error;
  }
};

// API functions for Twitter-focused functionality
export const fetchStats = () => apiCall('/stats');

export const fetchRecentPosts = (limit = 10) => 
  apiCall(`/posts?limit=${limit}`);

export const fetchCampaigns = () => apiCall('/campaigns');

export const fetchUsers = () => apiCall('/users');

export const collectTwitterData = (keywords, limit = 10) =>
  apiCall('/collect/twitter', {
    method: 'POST',
    body: JSON.stringify({ keywords, limit })
  });

export const classifyContent = (text) =>
  apiCall('/classify', {
    method: 'POST',
    body: JSON.stringify({ text })
  });

export const analyzeUrl = (url) =>
  apiCall('/analyze-url', {
    method: 'POST',
    body: JSON.stringify({ url })
  });

export const detectCampaigns = () =>
  apiCall('/campaigns/detect', {
    method: 'POST'
  });

export const healthCheck = () => apiCall('/health');

// Utility functions
export const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

export const getRiskLevel = (score) => {
  if (score >= 0.7) return 'high';
  if (score >= 0.4) return 'medium';
  return 'low';
};

export const getRiskColor = (level) => {
  switch (level) {
    case 'high': return 'text-red-600 bg-red-100 dark:bg-red-900/20';
    case 'medium': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
    case 'low': return 'text-green-600 bg-green-100 dark:bg-green-900/20';
    default: return 'text-gray-600 bg-gray-100 dark:bg-gray-900/20';
  }
};