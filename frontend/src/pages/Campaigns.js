import React, { useState, useEffect } from 'react';
import { AlertTriangle, Clock, Users, TrendingUp } from 'lucide-react';
import { fetchCampaigns, detectCampaigns, getRiskLevel, getRiskColor, formatDate } from '../utils/api';

const Campaigns = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [detecting, setDetecting] = useState(false);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const response = await fetchCampaigns();
      setCampaigns(response.data || []);
    } catch (error) {
      console.error('Error loading campaigns:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDetectCampaigns = async () => {
    setDetecting(true);
    try {
      await detectCampaigns();
      await loadCampaigns(); // Reload data
    } catch (error) {
      console.error('Error detecting campaigns:', error);
    } finally {
      setDetecting(false);
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
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Campaign Detection
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Coordinated campaigns and suspicious activities
          </p>
        </div>
        <button
          onClick={handleDetectCampaigns}
          disabled={detecting}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          {detecting ? 'Detecting...' : 'Run Detection'}
        </button>
      </div>

      {/* Campaign Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 border border-red-200 dark:border-red-800">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <div className="text-2xl font-bold text-red-900 dark:text-red-100">
                {campaigns.filter(c => c.risk_score >= 0.7).length}
              </div>
              <div className="text-sm text-red-600">High Risk</div>
            </div>
          </div>
        </div>

        <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6 border border-yellow-200 dark:border-yellow-800">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-yellow-600" />
            <div className="ml-4">
              <div className="text-2xl font-bold text-yellow-900 dark:text-yellow-100">
                {campaigns.filter(c => c.risk_score >= 0.4 && c.risk_score < 0.7).length}
              </div>
              <div className="text-sm text-yellow-600">Medium Risk</div>
            </div>
          </div>
        </div>

        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 border border-green-200 dark:border-green-800">
          <div className="flex items-center">
            <Users className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <div className="text-2xl font-bold text-green-900 dark:text-green-100">
                {campaigns.filter(c => c.risk_score < 0.4).length}
              </div>
              <div className="text-sm text-green-600">Low Risk</div>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 border border-blue-200 dark:border-blue-800">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <div className="text-2xl font-bold text-blue-900 dark:text-blue-100">
                {campaigns.reduce((sum, c) => sum + (c.volume || 0), 0)}
              </div>
              <div className="text-sm text-blue-600">Total Volume</div>
            </div>
          </div>
        </div>
      </div>

      {/* Campaigns List */}
      <div className="dashboard-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          Detected Campaigns
        </h3>
        
        {campaigns.length > 0 ? (
          <div className="space-y-4">
            {campaigns.map((campaign, index) => {
              const riskLevel = getRiskLevel(campaign.risk_score);
              const riskColor = getRiskColor(riskLevel);
              
              return (
                <div key={campaign.id || index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h4 className="text-lg font-medium text-gray-900 dark:text-white">
                          {campaign.hashtag || `Campaign ${index + 1}`}
                        </h4>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${riskColor}`}>
                          {riskLevel.toUpperCase()} RISK
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                        <div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">Volume</div>
                          <div className="text-lg font-semibold text-gray-900 dark:text-white">
                            {(campaign.volume || 0).toLocaleString()}
                          </div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">Risk Score</div>
                          <div className="text-lg font-semibold text-gray-900 dark:text-white">
                            {((campaign.risk_score || 0) * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">First Detected</div>
                          <div className="text-sm text-gray-900 dark:text-white">
                            {campaign.first_detected ? formatDate(campaign.first_detected) : 'N/A'}
                          </div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">Last Activity</div>
                          <div className="text-sm text-gray-900 dark:text-white">
                            {campaign.last_detected ? formatDate(campaign.last_detected) : 'N/A'}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="ml-4">
                      <button className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium">
                        View Details →
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12">
            <AlertTriangle className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
              No campaigns detected
            </h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Run detection to analyze current data for campaign patterns.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Campaigns;