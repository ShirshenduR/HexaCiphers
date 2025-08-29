import React, { useState, useEffect } from 'react';
import { AlertTriangle, TrendingUp, Users, Activity, Shield } from 'lucide-react';
import SentimentChart from './SentimentChart';

const TwitterDashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [metrics, setMetrics] = useState({
    totalPosts: 0,
    antiIndiaContent: 0,
    activeCampaigns: 0,
    highRiskUsers: 0
  });
  const [isMonitoring, setIsMonitoring] = useState(false);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [alertsRes, campaignsRes, metricsRes] = await Promise.all([
        fetch('/api/twitter/alerts?status=active'),
        fetch('/api/twitter/campaigns?status=active'),
        fetch('/api/twitter/metrics')
      ]);

      setAlerts(await alertsRes.json());
      setCampaigns(await campaignsRes.json());
      setMetrics(await metricsRes.json());
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const startMonitoring = async () => {
    const keywords = [
      'boycott india', 'anti india', 'kashmir freedom', 'khalistan',
      'modi dictator', 'india terrorist', 'hindu extremist'
    ];

    try {
      await fetch('/api/twitter/start-monitoring', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keywords })
      });
      setIsMonitoring(true);
    } catch (error) {
      console.error('Error starting monitoring:', error);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-blue-600 bg-blue-100';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Anti-India Campaign Monitor
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Real-time monitoring of Twitter/X.com for anti-India campaigns
            </p>
          </div>
          <div className="flex space-x-4">
            <button
              onClick={startMonitoring}
              disabled={isMonitoring}
              className={`px-6 py-2 rounded-lg font-medium ${
                isMonitoring
                  ? 'bg-green-100 text-green-800 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {isMonitoring ? 'Monitoring Active' : 'Start Monitoring'}
            </button>
          </div>
        </div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Total Posts (24h)
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {metrics.totalPosts.toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center">
              <AlertTriangle className="h-8 w-8 text-red-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Anti-India Content
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {metrics.antiIndiaContent.toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  Active Campaigns
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {metrics.activeCampaigns}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center">
              <Users className="h-8 w-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  High Risk Users
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {metrics.highRiskUsers}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Alerts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Active Alerts
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {alerts.map((alert, index) => (
                <div key={index} className="border-l-4 border-red-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">
                        {alert.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {alert.description}
                      </p>
                      <p className="text-xs text-gray-500 mt-2">
                        {new Date(alert.created_at).toLocaleString()}
                      </p>
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded ${getSeverityColor(alert.severity)}`}>
                      {alert.severity}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Detected Campaigns
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {campaigns.map((campaign, index) => (
                <div key={index} className="border border-gray-200 dark:border-gray-700 rounded p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium text-gray-900 dark:text-white">
                      {campaign.campaign_name || 'Unnamed Campaign'}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded ${getSeverityColor(campaign.severity_level)}`}>
                      {campaign.severity_level}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <p>Participants: {campaign.participant_count}</p>
                    <p>Hashtags: {campaign.hashtags?.join(', ')}</p>
                    <p>Engagement: {campaign.total_engagement?.toLocaleString()}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sentiment Analysis Chart */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Sentiment Analysis Overview
          </h2>
          <SentimentChart />
        </div>
      </div>
    </div>
  );
};

export default TwitterDashboard;