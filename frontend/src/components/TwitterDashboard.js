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
  const [sentimentData, setSentimentData] = useState({
    positive: 0,
    negative: 0,
    neutral: 0
  });

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [postsRes, campaignsRes, statsRes] = await Promise.all([
        fetch('/api/posts?limit=10'),
        fetch('/api/campaigns'),
        fetch('/api/stats')
      ]);

      const postsData = await postsRes.json();
      const campaignsData = await campaignsRes.json();
      const statsData = await statsRes.json();

      // Set alerts from recent posts with validation
      if (postsData && postsData.data && Array.isArray(postsData.data)) {
        setAlerts(postsData.data);
      } else {
        setAlerts([]);
      }

      // Set campaigns with validation
      if (campaignsData && campaignsData.data && Array.isArray(campaignsData.data)) {
        setCampaigns(campaignsData.data);
      } else {
        setCampaigns([]);
      }
      
      // Update metrics from stats with validation
      if (statsData && statsData.data) {
        const stats = statsData.data;
        setMetrics({
          totalPosts: stats.total_posts || 0,
          antiIndiaContent: (stats.classification_distribution && stats.classification_distribution.anti_india) || 0,
          activeCampaigns: stats.total_campaigns || 0,
          highRiskUsers: (stats.riskMetrics && stats.riskMetrics.flagged_users) || 0
        });

        // Update sentiment data with validation
        const sentimentDist = stats.sentiment_distribution || {};
        setSentimentData({
          positive: sentimentDist.positive || 0,
          negative: sentimentDist.negative || 0,
          neutral: sentimentDist.neutral || 0
        });
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Set default values on error
      setAlerts([]);
      setCampaigns([]);
      setMetrics({
        totalPosts: 0,
        antiIndiaContent: 0,
        activeCampaigns: 0,
        highRiskUsers: 0
      });
      setSentimentData({
        positive: 0,
        negative: 0,
        neutral: 0
      });
    }
  };

  const startMonitoring = async () => {
    try {
      // Use the dashboard data collection endpoint
      await fetch('/api/collect/dashboard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      setIsMonitoring(true);
      // Refresh dashboard data after collection
      fetchDashboardData();
    } catch (error) {
      console.error('Error starting monitoring:', error);
    }
  };

  const getSeverityColor = (sentiment) => {
    switch (sentiment) {
      case 'negative': return 'text-red-600 bg-red-100';
      case 'positive': return 'text-green-600 bg-green-100';
      case 'neutral': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
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
              {alerts && alerts.length > 0 ? alerts.map((alert, index) => (
                <div key={index} className="border-l-4 border-red-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">
                        Recent Post Alert
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {typeof alert.content === 'string' ? alert.content : 'Content not available'}
                      </p>
                      <p className="text-xs text-gray-500 mt-2">
                        {alert.created_at ? new Date(alert.created_at).toLocaleString() : 'Date not available'}
                      </p>
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded ${getSeverityColor(alert.sentiment || 'low')}`}>
                      {alert.sentiment || 'unknown'}
                    </span>
                  </div>
                </div>
              )) : (
                <p className="text-gray-500 text-center py-4">No alerts available</p>
              )}
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Detected Campaigns
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {campaigns && campaigns.length > 0 ? campaigns.map((campaign, index) => (
                <div key={index} className="border border-gray-200 dark:border-gray-700 rounded p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium text-gray-900 dark:text-white">
                      {campaign.campaign_name || 'Unnamed Campaign'}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded ${getSeverityColor(campaign.severity_level)}`}>
                      {campaign.severity_level || 'unknown'}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <p>Participants: {campaign.participant_count || 0}</p>
                    <p>Hashtags: {Array.isArray(campaign.hashtags) ? campaign.hashtags.join(', ') : 'N/A'}</p>
                    <p>Engagement: {campaign.total_engagement ? campaign.total_engagement.toLocaleString() : '0'}</p>
                  </div>
                </div>
              )) : (
                <p className="text-gray-500 text-center py-4">No campaigns detected</p>
              )}
            </div>
          </div>
        </div>

        {/* Sentiment Analysis Chart */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Sentiment Analysis Overview
          </h2>
          <SentimentChart data={sentimentData} />
        </div>
      </div>
    </div>
  );
};

export default TwitterDashboard;