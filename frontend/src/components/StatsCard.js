import React from 'react';

const StatsCard = ({ title, value, icon: Icon, trend, trendUp, color = 'blue', darkMode }) => {
  const colorClasses = {
    blue: 'metric-card-blue',
    red: 'metric-card-red',
    green: 'metric-card-green',
    orange: 'metric-card-orange',
    purple: 'metric-card-purple',
  };

  return (
    <div className={`${colorClasses[color]} text-white scale-in`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <Icon className="h-6 w-6 text-white/90" />
            <h3 className="text-sm font-semibold text-white/80 uppercase tracking-wider">
              {title}
            </h3>
          </div>
          <div className="text-3xl font-bold text-white mb-1">
            {value}
          </div>
          {trend && (
            <div className="flex items-center space-x-1">
              <div className={`text-sm font-medium ${
                trendUp ? 'text-green-200' : 'text-red-200'
              }`}>
                {trend}
              </div>
              <div className={`h-1.5 w-1.5 rounded-full ${
                trendUp ? 'bg-green-300' : 'bg-red-300'
              } animate-pulse`}></div>
            </div>
          )}
        </div>
        <div className="flex-shrink-0">
          <div className="h-16 w-16 bg-white/10 rounded-2xl flex items-center justify-center backdrop-blur-sm border border-white/20">
            <Icon className="h-8 w-8 text-white drop-shadow-sm" />
          </div>
        </div>
      </div>
      
      {/* Progress bar */}
      <div className="mt-4">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{
              width: `${Math.min(100, (parseInt(value.replace(/,/g, '')) / 10000) * 100)}%`,
              background: 'rgba(255, 255, 255, 0.3)'
            }}
          ></div>
        </div>
      </div>

      {/* Floating decoration */}
      <div className="absolute top-2 right-2 h-8 w-8 bg-white/5 rounded-full blur-xl"></div>
      <div className="absolute bottom-2 left-2 h-6 w-6 bg-white/5 rounded-full blur-lg"></div>
    </div>
  );
};

export default StatsCard;