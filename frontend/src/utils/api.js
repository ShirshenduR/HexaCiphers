// API utility functions for HexaCiphers frontend

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

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
    // Return mock data for demo purposes when API is not available
    return getMockData(endpoint);
  }
};

// Mock data for demo purposes
const getMockData = (endpoint) => {
  switch (endpoint) {
    case '/stats':
      return {
        status: 'success',
        data: {
          total_posts: 15420,
          total_users: 3450,
          total_campaigns: 8,
          sentiment_distribution: {
            positive: 5200,
            negative: 3100,
            neutral: 7120
          },
          classification_distribution: {
            pro_india: 6800,
            anti_india: 1200,
            neutral: 7420
          }
        }
      };
    
    case '/posts':
      return {
        status: 'success',
        data: [
          {
            id: 1,
            content: "Coordinated attack on India's image detected through bot networks",
            classification: "Anti-India",
            sentiment: "negative",
            platform: "Twitter",
            created_at: new Date(Date.now() - 300000).toISOString()
          },
          {
            id: 2,
            content: "Multiple fake accounts spreading propaganda against Indian policies",
            classification: "Anti-India",
            sentiment: "negative", 
            platform: "Reddit",
            created_at: new Date(Date.now() - 600000).toISOString()
          }
        ]
      };
    
    case '/campaigns':
      return {
        status: 'success',
        data: [
          {
            id: 1,
            hashtag: "#BoycottIndia",
            volume: 350,
            risk_score: 0.85,
            first_detected: new Date(Date.now() - 3600000).toISOString(),
            last_detected: new Date().toISOString()
          },
          {
            id: 2,
            hashtag: "#PropagandaAlert",
            volume: 180,
            risk_score: 0.75,
            first_detected: new Date(Date.now() - 7200000).toISOString(),
            last_detected: new Date().toISOString()
          }
        ]
      };
    
    default:
      return {
        status: 'error',
        message: 'Endpoint not found',
        data: null
      };
  }
};

// API functions
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

export const collectRedditData = (subreddit, limit = 10) =>
  apiCall('/collect/reddit', {
    method: 'POST',
    body: JSON.stringify({ subreddit, limit })
  });

export const processText = (text) =>
  apiCall('/process/text', {
    method: 'POST',
    body: JSON.stringify({ text })
  });

export const classifyContent = (text) =>
  apiCall('/classify', {
    method: 'POST',
    body: JSON.stringify({ text })
  });

export const detectCampaigns = () =>
  apiCall('/campaigns/detect', {
    method: 'POST'
  });

export const createPost = (postData) =>
  apiCall('/posts', {
    method: 'POST',
    body: JSON.stringify(postData)
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