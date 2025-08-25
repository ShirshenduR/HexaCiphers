import React from 'react';

const CampaignHeatmap = ({ campaigns }) => {
  // Generate heatmap data for the last 7 days and 24 hours
  const generateHeatmapData = () => {
    const data = [];
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    
    for (let day = 0; day < 7; day++) {
      for (let hour = 0; hour < 24; hour++) {
        // Simulate campaign activity data
        const intensity = Math.random();
        const campaignCount = Math.floor(intensity * 10);
        
        data.push({
          day: days[day],
          hour,
          intensity,
          campaignCount,
          date: new Date(Date.now() - (6 - day) * 24 * 60 * 60 * 1000)
        });
      }
    }
    
    return data;
  };

  const heatmapData = generateHeatmapData();
  const hours = Array.from({ length: 24 }, (_, i) => i);
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const getIntensityColor = (intensity) => {
    if (intensity > 0.8) return 'bg-red-600';
    if (intensity > 0.6) return 'bg-red-400';
    if (intensity > 0.4) return 'bg-yellow-400';
    if (intensity > 0.2) return 'bg-green-400';
    if (intensity > 0) return 'bg-green-200';
    return 'bg-gray-100 dark:bg-gray-800';
  };

  const getDataForDayHour = (day, hour) => {
    return heatmapData.find(d => d.day === day && d.hour === hour) || { intensity: 0, campaignCount: 0 };
  };

  return (
    <div className="space-y-4">
      {/* Legend */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600 dark:text-gray-400">
          Campaign activity intensity over the last 7 days
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs text-gray-500 dark:text-gray-400">Less</span>
          <div className="flex space-x-1">
            <div className="w-3 h-3 bg-gray-100 dark:bg-gray-800 rounded-sm"></div>
            <div className="w-3 h-3 bg-green-200 rounded-sm"></div>
            <div className="w-3 h-3 bg-green-400 rounded-sm"></div>
            <div className="w-3 h-3 bg-yellow-400 rounded-sm"></div>
            <div className="w-3 h-3 bg-red-400 rounded-sm"></div>
            <div className="w-3 h-3 bg-red-600 rounded-sm"></div>
          </div>
          <span className="text-xs text-gray-500 dark:text-gray-400">More</span>
        </div>
      </div>

      {/* Heatmap Grid */}
      <div className="overflow-x-auto">
        <div className="inline-block min-w-full">
          {/* Hour labels */}
          <div className="flex mb-2">
            <div className="w-12"></div> {/* Space for day labels */}
            {hours.map(hour => (
              <div key={hour} className="w-4 text-xs text-center text-gray-500 dark:text-gray-400">
                {hour % 6 === 0 ? hour : ''}
              </div>
            ))}
          </div>
          
          {/* Days and data */}
          {days.map(day => (
            <div key={day} className="flex items-center mb-1">
              <div className="w-12 text-xs text-gray-600 dark:text-gray-400 pr-2">
                {day}
              </div>
              {hours.map(hour => {
                const data = getDataForDayHour(day, hour);
                return (
                  <div
                    key={`${day}-${hour}`}
                    className={`w-4 h-4 mr-1 rounded-sm cursor-pointer transition-all duration-200 hover:scale-110 ${getIntensityColor(data.intensity)}`}
                    title={`${day} ${hour}:00 - ${data.campaignCount} campaigns`}
                  />
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            {Math.max(...heatmapData.map(d => d.campaignCount))}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Peak Activity
          </div>
        </div>
        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            {Math.floor(heatmapData.reduce((sum, d) => sum + d.campaignCount, 0) / heatmapData.length)}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Avg. Hourly
          </div>
        </div>
        <div className="text-center">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            {heatmapData.reduce((sum, d) => sum + d.campaignCount, 0)}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Total Events
          </div>
        </div>
      </div>
    </div>
  );
};

export default CampaignHeatmap;