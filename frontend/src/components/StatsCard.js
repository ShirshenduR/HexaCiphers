import React from 'react';

const StatsCard = ({ title, value, icon: Icon, trend, trendUp, color = 'blue' }) => {
  const colorClasses = {
    blue: 'bg-blue-500 text-blue-600',
    red: 'bg-red-500 text-red-600',
    green: 'bg-green-500 text-green-600',
    orange: 'bg-orange-500 text-orange-600',
    purple: 'bg-purple-500 text-purple-600',
  };

  const bgColorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900/20',
    red: 'bg-red-50 dark:bg-red-900/20',
    green: 'bg-green-50 dark:bg-green-900/20',
    orange: 'bg-orange-50 dark:bg-orange-900/20',
    purple: 'bg-purple-50 dark:bg-purple-900/20',
  };

  return (
    <div className={`${bgColorClasses[color]} rounded-lg p-6 border border-gray-200 dark:border-gray-700`}>
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <div className={`p-2 rounded-md ${colorClasses[color].split(' ')[0]}`}>
            <Icon className="h-6 w-6 text-white" />
          </div>
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
              {title}
            </dt>
            <dd className="flex items-baseline">
              <div className="text-2xl font-semibold text-gray-900 dark:text-white">
                {value}
              </div>
              {trend && (
                <div className={`ml-2 flex items-baseline text-sm ${
                  trendUp ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                }`}>
                  <span className="sr-only">
                    {trendUp ? 'Increased' : 'Decreased'} by
                  </span>
                  {trend}
                </div>
              )}
            </dd>
          </dl>
        </div>
      </div>
    </div>
  );
};

export default StatsCard;