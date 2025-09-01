import React from 'react';

const Analytics = () => {
  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Analytics & Insights
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Deep dive into campaign patterns and platform analytics
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="dashboard-card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Twitter Content Analysis
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Original Tweets</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{width: '65%'}}></div>
                </div>
                <span className="text-sm font-medium">65%</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Retweets</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-600 h-2 rounded-full" style={{width: '25%'}}></div>
                </div>
                <span className="text-sm font-medium">25%</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Replies</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div className="bg-purple-600 h-2 rounded-full" style={{width: '10%'}}></div>
                </div>
                <span className="text-sm font-medium">10%</span>
              </div>
            </div>
          </div>
        </div>

        <div className="dashboard-card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Content Classification
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Pro-India</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-600 h-2 rounded-full" style={{width: '45%'}}></div>
                </div>
                <span className="text-sm font-medium">45%</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Neutral</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div className="bg-gray-600 h-2 rounded-full" style={{width: '47%'}}></div>
                </div>
                <span className="text-sm font-medium">47%</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Anti-India</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div className="bg-red-600 h-2 rounded-full" style={{width: '8%'}}></div>
                </div>
                <span className="text-sm font-medium">8%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="dashboard-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Coming Soon: Advanced Analytics
        </h3>
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center mb-4">
            <span className="text-2xl">📊</span>
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            Advanced Analytics Dashboard
          </h3>
          <p className="mt-2 text-gray-500 dark:text-gray-400 max-w-md mx-auto">
            Time series analysis, network graphs, and predictive modeling coming soon.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Analytics;