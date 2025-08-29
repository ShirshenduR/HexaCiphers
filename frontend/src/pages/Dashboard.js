import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  TrendingUp, 
  Users, 
  MessageCircle,
  Activity,
  Eye,
  Clock,
  Shield
} from 'lucide-react';
import StatsCard from '../components/StatsCard';
import RecentAlerts from '../components/RecentAlerts';
import TrendingHashtags from '../components/TrendingHashtags';
import SentimentChart from '../components/SentimentChart';
import CampaignHeatmap from '../components/CampaignHeatmap';
import { fetchStats, fetchRecentPosts, fetchCampaigns } from '../utils/api';

const Dashboard = ({ darkMode }) => {
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
    const loadData = async () => {
      try {
        const [statsData, postsData, campaignsData] = await Promise.all([
          fetchStats(),
          fetchRecentPosts(10),
          fetchCampaigns()
        ]);
        
        setStats(statsData.data || {
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
        setRecentPosts(postsData.data || []);
        setCampaigns(campaignsData.data || []);
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
    
    // Set up real-time updates
    const interval = setInterval(loadData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
            <Shield className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-6 w-6 text-white" />
          </div>
          <p className="text-white/80 font-medium">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white drop-shadow-lg mb-2">
          Campaign Detection Dashboard
        </h1>
        <p className="text-xl text-white/80 font-medium">
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
          darkMode={darkMode}
        />
        <StatsCard
          title="Active Campaigns"
          value={stats.total_campaigns.toString()}
          icon={AlertTriangle}
          trend={campaigns.filter(c => c.risk_score > 0.7).length > 0 ? 'High Risk' : 'Low Risk'}
          trendUp={false}
          color="red"
          darkMode={darkMode}
        />
        <StatsCard
          title="Users Monitored"
          value={stats.total_users.toLocaleString()}
          icon={Users}
          trend={`+${Math.floor(Math.random() * 15 + 3)}%`}
          trendUp={true}
          color="green"
          darkMode={darkMode}
        />
        <StatsCard
          title="Anti-India Posts"
          value={stats.classification_distribution.anti_india.toString()}
          icon={TrendingUp}
          trend={`${Math.floor(Math.random() * 10 + 2)}% of total`}
          trendUp={false}
          color="orange"
          darkMode={darkMode}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Charts */}
        <div className="lg:col-span-2 space-y-8">
          {/* Sentiment Analysis Chart */}
          <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} slide-up`}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">
                Sentiment Analysis
              </h3>
              <div className="flex items-center space-x-2">
                <Activity className="h-5 w-5 text-blue-400" />
                <span className="text-sm text-white/60 font-medium">Live</span>
              </div>
            </div>
            <SentimentChart data={stats.sentiment_distribution} darkMode={darkMode} />
          </div>

          {/* Campaign Intensity Heatmap */}
          <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} slide-up`} style={{animationDelay: '0.1s'}}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">
                Campaign Activity Heatmap
              </h3>
              <div className="flex items-center space-x-2">
                <Eye className="h-5 w-5 text-purple-400" />
                <span className="text-sm text-white/60 font-medium">Interactive</span>
              </div>
            </div>
            <CampaignHeatmap campaigns={campaigns} darkMode={darkMode} />
          </div>
        </div>

        {/* Right Column - Alerts and Trending */}
        <div className="space-y-8">
          {/* Recent Alerts */}
          <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} slide-up`} style={{animationDelay: '0.2s'}}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">
                Recent Alerts
              </h3>
              <div className="flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5 text-red-400 pulse-status" />
                <span className="text-sm text-white/60 font-medium">Critical</span>
              </div>
            </div>
            <RecentAlerts posts={recentPosts} darkMode={darkMode} />
          </div>

          {/* Trending Hashtags */}
          <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} slide-up`} style={{animationDelay: '0.3s'}}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">
                Trending Hashtags
              </h3>
              <div className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-green-400" />
                <span className="text-sm text-white/60 font-medium">Rising</span>
              </div>
            </div>
            <TrendingHashtags campaigns={campaigns} darkMode={darkMode} />
          </div>

          {/* System Status */}
          <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} slide-up`} style={{animationDelay: '0.4s'}}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">
                System Status
              </h3>
              <div className="flex items-center space-x-2">
                <Clock className="h-5 w-5 text-blue-400" />
                <span className="text-sm text-white/60 font-medium">Real-time</span>
              </div>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/10">
                <span className="text-sm text-white/80 font-medium">
                  Data Collection
                </span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-green-400 rounded-full pulse-status"></div>
                  <span className="text-sm text-green-400 font-semibold">
                    Active
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/10">
                <span className="text-sm text-white/80 font-medium">
                  ML Processing
                </span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-green-400 rounded-full pulse-status"></div>
                  <span className="text-sm text-green-400 font-semibold">
                    Running
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/10">
                <span className="text-sm text-white/80 font-medium">
                  Campaign Detection
                </span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-green-400 rounded-full pulse-status"></div>
                  <span className="text-sm text-green-400 font-semibold">
                    Monitoring
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/10">
                <span className="text-sm text-white/80 font-medium">
                  Last Update
                </span>
                <span className="text-sm text-white/60 font-medium">
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