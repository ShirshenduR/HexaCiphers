import React from 'react';

const SentimentChart = ({ data }) => {
  const total = data.positive + data.negative + data.neutral;
  
  const chartData = [
    { name: 'Positive', value: data.positive, color: '#10B981', percentage: total > 0 ? (data.positive / total * 100).toFixed(1) : 0 },
    { name: 'Negative', value: data.negative, color: '#EF4444', percentage: total > 0 ? (data.negative / total * 100).toFixed(1) : 0 },
    { name: 'Neutral', value: data.neutral, color: '#6B7280', percentage: total > 0 ? (data.neutral / total * 100).toFixed(1) : 0 }
  ];

  // If no data, show sample data
  if (total === 0) {
    chartData[0] = { name: 'Positive', value: 45, color: '#10B981', percentage: '45.0' };
    chartData[1] = { name: 'Negative', value: 25, color: '#EF4444', percentage: '25.0' };
    chartData[2] = { name: 'Neutral', value: 30, color: '#6B7280', percentage: '30.0' };
  }

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
                  className="h-full rounded-full transition-all duration-500 ease-out"
                  style={{
                    backgroundColor: item.color,
                    width: `${item.percentage}%`
                  }}
                />
              </div>
            </div>
            <div className="w-12 text-sm font-medium text-gray-700 dark:text-gray-300 text-right">
              {item.percentage}%
            </div>
            <div className="w-16 text-sm text-gray-500 dark:text-gray-400 text-right">
              {item.value.toLocaleString()}
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="grid grid-cols-3 gap-4 text-center">
          {chartData.map((item, index) => (
            <div key={index} className="space-y-1">
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
      </div>
      
      {/* Overall Sentiment Indicator */}
      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Overall Sentiment
          </span>
          <div className="flex items-center space-x-2">
            {chartData[0].percentage > chartData[1].percentage ? (
              <>
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-green-600 dark:text-green-400 font-medium">
                  Positive Trend
                </span>
              </>
            ) : chartData[1].percentage > chartData[0].percentage ? (
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