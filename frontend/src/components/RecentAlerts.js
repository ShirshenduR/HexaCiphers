import React from 'react';
import { AlertTriangle, Clock, MapPin } from 'lucide-react';

const RecentAlerts = ({ posts, darkMode }) => {
  const getAlertLevel = (classification, sentiment) => {
    if (classification === 'Anti-India') return 'high';
    if (sentiment === 'negative') return 'medium';
    return 'low';
  };

  const getAlertColor = (level) => {
    switch (level) {
      case 'high': return 'text-red-300 bg-red-500/20';
      case 'medium': return 'text-yellow-300 bg-yellow-500/20';
      case 'low': return 'text-green-300 bg-green-500/20';
      default: return 'text-white/60 bg-white/10';
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

  return (
    <div className="space-y-3">
      {posts.length > 0 ? (
        posts.slice(0, 5).map((alert, index) => {
          const alertLevel = getAlertLevel(alert.classification, alert.sentiment);
          const alertColor = getAlertColor(alertLevel);
          
          return (
          <div key={alert.id || index} className="flex items-start space-x-3 p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all duration-200 backdrop-blur-sm">
            <div className={`flex-shrink-0 p-2 rounded-full ${alertColor}`}>
              <AlertTriangle className="h-4 w-4" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white/90 line-clamp-2 font-medium">
                {alert.content}
              </p>
              <div className="mt-2 flex items-center space-x-3 text-xs text-white/60">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-3 w-3" />
                  <span>{alert.platform}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="h-3 w-3" />
                  <span>{formatTimeAgo(alert.created_at)}</span>
                </div>
                <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${alertColor} border border-current/20`}>
                  {alertLevel.toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        );
      })) : (
        <div className="text-center py-8">
          <AlertTriangle className="mx-auto h-12 w-12 text-white/40" />
          <h3 className="mt-2 text-sm font-medium text-white">
            No recent alerts
          </h3>
          <p className="mt-1 text-sm text-white/60">
            Start monitoring to see alerts from Twitter activity.
          </p>
        </div>
      )}
    </div>
  );
};

export default RecentAlerts;