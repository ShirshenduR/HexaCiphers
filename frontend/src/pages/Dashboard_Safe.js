import React, { useState, useEffect } from 'react';
import { AlertTriangle, TrendingUp, Users, Activity, Shield } from 'lucide-react';
import SentimentChart from '../components/SentimentChart';

const Dashboard = () => {
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [postsRes, campaignsRes, statsRes] = await Promise.all([
        fetch('/api/posts?limit=10'),
        fetch('/api/campaigns'),
        fetch('/api/stats')
      ]);

      const postsData = await postsRes.json();
      const campaignsData = await campaignsRes.json();
      const statsData = await statsRes.json();

      // Safely set alerts from recent posts
      if (postsData && postsData.data && Array.isArray(postsData.data)) {
        setAlerts(postsData.data);
      } else {
        setAlerts([]);
      }

      // Safely set campaigns
      if (campaignsData && campaignsData.data && Array.isArray(campaignsData.data)) {
        setCampaigns(campaignsData.data);
      } else {
        setCampaigns([]);
      }
      
      // Safely update metrics from stats
      if (statsData && statsData.data && typeof statsData.data === 'object') {
        const stats = statsData.data;
        setMetrics({
          totalPosts: Number(stats.total_posts) || 0,
          antiIndiaContent: Number((stats.classification_distribution && stats.classification_distribution.anti_india)) || 0,
          activeCampaigns: Number(stats.total_campaigns) || 0,
          highRiskUsers: Number((stats.riskMetrics && stats.riskMetrics.flagged_users)) || 0
        });

        // Safely update sentiment data
        const sentimentDist = stats.sentiment_distribution || {};
        setSentimentData({
          positive: Number(sentimentDist.positive) || 0,
          negative: Number(sentimentDist.negative) || 0,
          neutral: Number(sentimentDist.neutral) || 0
        });
      }
      
      setError(null);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setError(error.message);
      // Set safe defaults on error
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
    } finally {
      setLoading(false);
    }
  };

  const startMonitoring = async () => {
    try {
      const response = await fetch('/api/collect/dashboard', { method: 'POST' });
      const data = await response.json();
      if (data.status === 'success') {
        // Refresh dashboard data after collection
        fetchDashboardData();
      }
    } catch (error) {
      console.error('Error starting monitoring:', error);
    }
  };

  if (loading && alerts.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-16 w-16 text-red-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
          <button 
            onClick={fetchDashboardData}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

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
              className="px-6 py-2 rounded-lg font-medium bg-blue-600 text-white hover:bg-blue-700"
            >
              Collect Fresh Data
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

        {/* Alerts and Campaigns Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Recent Posts
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {alerts && alerts.length > 0 ? alerts.map((alert, index) => {
                // Safely extract and validate data
                const content = alert && typeof alert.content === 'string' ? alert.content : 'Content not available';
                const createdAt = alert && alert.created_at ? alert.created_at : null;
                const sentiment = alert && alert.sentiment ? alert.sentiment : 'unknown';
                
                return (
                  <div key={`alert-${index}-${alert.id || index}`} className="border-l-4 border-blue-500 pl-4 py-2">
                    <div className="flex justify-between items-start">
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 dark:text-white">
                          Recent Post #{index + 1}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1 break-words">
                          {content.length > 150 ? `${content.substring(0, 150)}...` : content}
                        </p>
                        <p className="text-xs text-gray-500 mt-2">
                          {createdAt ? new Date(createdAt).toLocaleString() : 'Date not available'}
                        </p>
                      </div>
                      <span className={`px-2 py-1 text-xs font-medium rounded ml-2 flex-shrink-0 ${
                        sentiment === 'negative' ? 'text-red-600 bg-red-100' :
                        sentiment === 'positive' ? 'text-green-600 bg-green-100' :
                        'text-blue-600 bg-blue-100'
                      }`}>
                        {sentiment}
                      </span>
                    </div>
                  </div>
                );
              }) : (
                <p className="text-gray-500 text-center py-4">No recent posts available</p>
              )}
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Detected Campaigns
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {campaigns && campaigns.length > 0 ? campaigns.map((campaign, index) => (
                <div key={`campaign-${index}-${campaign.id || index}`} className="border border-gray-200 dark:border-gray-700 rounded p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium text-gray-900 dark:text-white">
                      {campaign && campaign.campaign_name ? String(campaign.campaign_name) : 'Unnamed Campaign'}
                    </h3>
                    <span className="px-2 py-1 text-xs font-medium rounded text-gray-600 bg-gray-100">
                      {campaign && campaign.severity_level ? String(campaign.severity_level) : 'unknown'}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <p>Participants: {campaign && campaign.participant_count ? Number(campaign.participant_count) : 0}</p>
                    <p>Hashtags: {campaign && Array.isArray(campaign.hashtags) ? campaign.hashtags.join(', ') : 'N/A'}</p>
                    <p>Engagement: {campaign && campaign.total_engagement ? Number(campaign.total_engagement).toLocaleString() : '0'}</p>
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

export default Dashboard;
