import React from 'react';
import { AlertTriangle, Clock, MapPin } from 'lucide-react';

const RecentAlerts = ({ posts }) => {
  const getAlertLevel = (classification, sentiment) => {
    if (classification === 'Anti-India') return 'high';
    if (sentiment === 'negative') return 'medium';
    return 'low';
  };

  const getAlertColor = (level) => {
    switch (level) {
      case 'high': return 'text-red-600 bg-red-100 dark:bg-red-900/20';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
      case 'low': return 'text-green-600 bg-green-100 dark:bg-green-900/20';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-900/20';
    }
  };

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffInMinutes < 60) {
      return `${diffInMinutes}m ago`;
    } else if (diffInMinutes < 1440) {
      return `${Math.floor(diffInMinutes / 60)}h ago`;
    } else {
      return `${Math.floor(diffInMinutes / 1440)}d ago`;
    }
  };

  // Sample alerts if no posts available
  const sampleAlerts = [
    {
      id: 1,
      content: "Coordinated hashtag campaign detected: #BoycottIndia trending with suspicious activity",
      classification: "Anti-India",
      sentiment: "negative",
      platform: "Twitter",
      created_at: new Date(Date.now() - 300000).toISOString() // 5 minutes ago
    },
    {
      id: 2,
      content: "Multiple bot accounts spreading anti-India propaganda detected",
      classification: "Anti-India", 
      sentiment: "negative",
      platform: "Reddit",
      created_at: new Date(Date.now() - 900000).toISOString() // 15 minutes ago
    },
    {
      id: 3,
      content: "Unusual spike in negative sentiment posts about Indian policies",
      classification: "Neutral",
      sentiment: "negative", 
      platform: "Twitter",
      created_at: new Date(Date.now() - 1800000).toISOString() // 30 minutes ago
    }
  ];

  const alerts = posts.length > 0 ? posts : sampleAlerts;

  return (
    <div className="space-y-3">
      {alerts.slice(0, 5).map((alert, index) => {
        const alertLevel = getAlertLevel(alert.classification, alert.sentiment);
        const alertColor = getAlertColor(alertLevel);
        
        return (
          <div key={alert.id || index} className="flex items-start space-x-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
            <div className={`flex-shrink-0 p-1 rounded-full ${alertColor}`}>
              <AlertTriangle className="h-4 w-4" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-900 dark:text-white line-clamp-2">
                {alert.content}
              </p>
              <div className="mt-1 flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-3 w-3" />
                  <span>{alert.platform}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="h-3 w-3" />
                  <span>{formatTimeAgo(alert.created_at)}</span>
                </div>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${alertColor}`}>
                  {alertLevel.toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        );
      })}
      
      {alerts.length === 0 && (
        <div className="text-center py-8">
          <AlertTriangle className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
            No recent alerts
          </h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            All systems are operating normally.
          </p>
        </div>
      )}
    </div>
  );
};

export default RecentAlerts;