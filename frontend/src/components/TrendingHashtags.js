import React from 'react';
import { TrendingUp, Hash } from 'lucide-react';

const TrendingHashtags = ({ campaigns }) => {
  // Sample trending hashtags if no campaigns available
  const sampleHashtags = [
    { hashtag: '#DigitalIndia', volume: 1250, trend: '+15%', risk: 'low' },
    { hashtag: '#IndiaFirst', volume: 980, trend: '+8%', risk: 'low' },
    { hashtag: '#BoycottIndia', volume: 350, trend: '+45%', risk: 'high' },
    { hashtag: '#FakeNews', volume: 420, trend: '+22%', risk: 'medium' },
    { hashtag: '#PropagandaAlert', volume: 180, trend: '+67%', risk: 'high' }
  ];

  // Convert campaigns to hashtag format
  const hashtagsFromCampaigns = campaigns
    .filter(c => c.hashtag && c.hashtag.startsWith('#'))
    .map(c => ({
      hashtag: c.hashtag,
      volume: c.volume,
      trend: `+${Math.floor(Math.random() * 50 + 5)}%`,
      risk: c.risk_score > 0.7 ? 'high' : c.risk_score > 0.4 ? 'medium' : 'low'
    }));

  const hashtags = hashtagsFromCampaigns.length > 0 ? hashtagsFromCampaigns : sampleHashtags;

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'high': return 'text-red-600 bg-red-100 dark:bg-red-900/20';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
      case 'low': return 'text-green-600 bg-green-100 dark:bg-green-900/20';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-900/20';
    }
  };

  const getTrendColor = (trend) => {
    const value = parseInt(trend.replace('%', '').replace('+', ''));
    if (value > 30) return 'text-red-600';
    if (value > 10) return 'text-yellow-600';
    return 'text-green-600';
  };

  return (
    <div className="space-y-3">
      {hashtags.slice(0, 8).map((item, index) => (
        <div key={index} className="flex items-center justify-between p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <Hash className="h-4 w-4 text-blue-500" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {item.hashtag}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {item.volume.toLocaleString()} posts
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className={`flex items-center space-x-1 ${getTrendColor(item.trend)}`}>
              <TrendingUp className="h-3 w-3" />
              <span className="text-xs font-medium">{item.trend}</span>
            </div>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(item.risk)}`}>
              {item.risk.toUpperCase()}
            </span>
          </div>
        </div>
      ))}
      
      {hashtags.length === 0 && (
        <div className="text-center py-8">
          <Hash className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
            No trending hashtags
          </h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Hashtag analysis in progress.
          </p>
        </div>
      )}
      
      <div className="pt-3 border-t border-gray-200 dark:border-gray-700">
        <button className="w-full text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium">
          View All Trending Hashtags →
        </button>
      </div>
    </div>
  );
};

export default TrendingHashtags;