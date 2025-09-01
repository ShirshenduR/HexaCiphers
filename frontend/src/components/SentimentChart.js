import React from 'react';

const SentimentChart = ({ data }) => {
  // Add null/undefined check for data
  if (!data || typeof data !== 'object') {
    return (
      <div className="text-center py-8">
        <div className="mx-auto h-12 w-12 text-gray-400 mb-4">📊</div>
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
          No sentiment data
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Data will appear when Twitter posts are analyzed.
        </p>
      </div>
    );
  }

  const positive = data.positive || 0;
  const negative = data.negative || 0;
  const neutral = data.neutral || 0;
  const total = positive + negative + neutral;

  if (total === 0) {
    return (
      <div className="text-center py-8">
        <div className="mx-auto h-12 w-12 text-gray-400 mb-4">📊</div>
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
          No sentiment data
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Data will appear when Twitter posts are analyzed.
        </p>
      </div>
    );
  }

  const chartData = [
    { 
      name: 'Positive', 
      value: positive, 
      color: '#10B981', 
      percentage: total > 0 ? ((positive / total) * 100).toFixed(1) : '0.0'
    },
    { 
      name: 'Negative', 
      value: negative, 
      color: '#EF4444', 
      percentage: total > 0 ? ((negative / total) * 100).toFixed(1) : '0.0'
    },
    { 
      name: 'Neutral', 
      value: neutral, 
      color: '#6B7280', 
      percentage: total > 0 ? ((neutral / total) * 100).toFixed(1) : '0.0'
    }
  ];

  return (
    <div className="space-y-4">
      {/* Bar Chart */}
      <div className="space-y-3">
        {chartData.map((item, index) => (
          <div key={index} className="flex items-center space-x-3">
            <div className="w-16 text-sm font-medium text-gray-700 dark:text-gray-300">
              {item.name}
            </div>
            <div className="flex-1 relative">
              <div className="bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-300"
                  style={{
                    width: `${item.percentage}%`,
                    backgroundColor: item.color
                  }}
                />
              </div>
            </div>
            <div className="w-12 text-sm font-medium text-gray-700 dark:text-gray-300 text-right">
              {item.percentage}%
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        {chartData.map((item, index) => (
          <div key={index} className="text-center">
            <div
              className="w-3 h-3 rounded-full mx-auto"
              style={{ backgroundColor: item.color }}
            />
            <div className="text-xs font-medium text-gray-700 dark:text-gray-300">
              {item.name}
            </div>
            <div className="text-lg font-bold text-gray-900 dark:text-white">
              {item.value.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
      
      {/* Overall Sentiment Indicator */}
      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Overall Sentiment
          </span>
          <div className="flex items-center space-x-2">
            {positive > negative ? (
              <>
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-green-600 dark:text-green-400 font-medium">
                  Positive Trend
                </span>
              </>
            ) : negative > positive ? (
              <>
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <span className="text-sm text-red-600 dark:text-red-400 font-medium">
                  Negative Trend
                </span>
              </>
            ) : (
              <>
                <div className="w-2 h-2 bg-gray-500 rounded-full"></div>
                <span className="text-sm text-gray-600 dark:text-gray-400 font-medium">
                  Neutral Trend
                </span>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SentimentChart;