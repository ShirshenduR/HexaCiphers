import React, { useState, useEffect } from 'react';
import { AlertTriangle, TrendingUp, Users, Activity } from 'lucide-react';

const TwitterDashboardDebug = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/posts?limit=5');
      const data = await response.json();
      
      console.log('API Response:', data);
      
      if (data && data.data && Array.isArray(data.data)) {
        setAlerts(data.data);
      } else {
        setError('Invalid data structure');
      }
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-600">Error: {error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <h1 className="text-2xl font-bold mb-4">Debug Dashboard</h1>
      
      <div className="bg-white p-4 rounded shadow mb-4">
        <h2 className="text-lg font-semibold mb-2">Raw Data:</h2>
        <pre className="text-xs bg-gray-100 p-2 rounded overflow-auto max-h-40">
          {JSON.stringify(alerts, null, 2)}
        </pre>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-lg font-semibold mb-2">Rendered Alerts:</h2>
        <div className="space-y-2">
          {alerts.map((alert, index) => {
            try {
              return (
                <div key={index} className="border p-2 rounded">
                  <div className="text-sm font-medium">
                    Alert #{index + 1}
                  </div>
                  <div className="text-sm text-gray-600">
                    Content: {String(alert.content || 'No content')}
                  </div>
                  <div className="text-xs text-gray-500">
                    Created: {alert.created_at ? String(new Date(alert.created_at).toLocaleString()) : 'No date'}
                  </div>
                  <div className="text-xs text-gray-500">
                    Sentiment: {String(alert.sentiment || 'unknown')}
                  </div>
                </div>
              );
            } catch (renderError) {
              return (
                <div key={index} className="border p-2 rounded bg-red-50">
                  <div className="text-red-600">Error rendering alert {index}: {renderError.message}</div>
                </div>
              );
            }
          })}
        </div>
      </div>
    </div>
  );
};

export default TwitterDashboardDebug;
