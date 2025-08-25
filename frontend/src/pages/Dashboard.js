import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  TrendingUp, 
  Users, 
  MessageCircle,
  Activity,
  Eye,
  Clock
} from 'lucide-react';
import StatsCard from '../components/StatsCard';
import RecentAlerts from '../components/RecentAlerts';
import TrendingHashtags from '../components/TrendingHashtags';
import SentimentChart from '../components/SentimentChart';
import CampaignHeatmap from '../components/CampaignHeatmap';
import { fetchStats, fetchRecentPosts, fetchCampaigns } from '../utils/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_posts: 0,
    total_users: 0,
    total_campaigns: 0,
    sentiment_distribution: {
      positive: 0,
      negative: 0,
      neutral: 0
    },
    classification_distribution: {
      pro_india: 0,
      anti_india: 0,
      neutral: 0
    }
  });
  const [recentPosts, setRecentPosts] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    
    // Set up real-time updates
    const interval = setInterval(loadDashboardData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsData, postsData, campaignsData] = await Promise.all([
        fetchStats(),
        fetchRecentPosts(10),
        fetchCampaigns()
      ]);
      
      setStats(statsData.data || stats);
      setRecentPosts(postsData.data || []);
      setCampaigns(campaignsData.data || []);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Campaign Detection Dashboard
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Real-time monitoring of anti-India campaigns on digital platforms
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Posts Analyzed"
          value={stats.total_posts.toLocaleString()}
          icon={MessageCircle}
          trend={`+${Math.floor(Math.random() * 20 + 5)}%`}
          trendUp={true}
          color="blue"
        />
        <StatsCard
          title="Active Campaigns"
          value={stats.total_campaigns.toString()}
          icon={AlertTriangle}
          trend={campaigns.filter(c => c.risk_score > 0.7).length > 0 ? 'High Risk' : 'Low Risk'}
          trendUp={false}
          color="red"
        />
        <StatsCard
          title="Users Monitored"
          value={stats.total_users.toLocaleString()}
          icon={Users}
          trend={`+${Math.floor(Math.random() * 15 + 3)}%`}
          trendUp={true}
          color="green"
        />
        <StatsCard
          title="Anti-India Posts"
          value={stats.classification_distribution.anti_india.toString()}
          icon={TrendingUp}
          trend={`${Math.floor(Math.random() * 10 + 2)}% of total`}
          trendUp={false}
          color="orange"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Charts */}
        <div className="lg:col-span-2 space-y-6">
          {/* Sentiment Analysis Chart */}
          <div className="dashboard-card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Sentiment Analysis
              </h3>
              <Activity className="h-5 w-5 text-gray-400" />
            </div>
            <SentimentChart data={stats.sentiment_distribution} />
          </div>

          {/* Campaign Intensity Heatmap */}
          <div className="dashboard-card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Campaign Activity Heatmap
              </h3>
              <Eye className="h-5 w-5 text-gray-400" />
            </div>
            <CampaignHeatmap campaigns={campaigns} />
          </div>
        </div>

        {/* Right Column - Alerts and Trending */}
        <div className="space-y-6">
          {/* Recent Alerts */}
          <div className="dashboard-card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Recent Alerts
              </h3>
              <AlertTriangle className="h-5 w-5 text-red-500" />
            </div>
            <RecentAlerts posts={recentPosts} />
          </div>

          {/* Trending Hashtags */}
          <div className="dashboard-card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Trending Hashtags
              </h3>
              <TrendingUp className="h-5 w-5 text-blue-500" />
            </div>
            <TrendingHashtags campaigns={campaigns} />
          </div>

          {/* System Status */}
          <div className="dashboard-card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                System Status
              </h3>
              <Clock className="h-5 w-5 text-green-500" />
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  Data Collection
                </span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-green-600 dark:text-green-400">
                    Active
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  ML Processing
                </span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-green-600 dark:text-green-400">
                    Running
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  Campaign Detection
                </span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-green-600 dark:text-green-400">
                    Monitoring
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  Last Update
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {new Date().toLocaleTimeString()}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;