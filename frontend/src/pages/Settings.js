import React from 'react';
import { Settings as SettingsIcon, Database, Shield, Bell } from 'lucide-react';

const Settings = () => {
  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Settings
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Configure system parameters and monitoring settings
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Data Collection Settings */}
        <div className="dashboard-card">
          <div className="flex items-center space-x-2 mb-4">
            <Database className="h-5 w-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Data Collection
            </h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Collection Interval (minutes)
              </label>
              <input
                type="number"
                defaultValue="5"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Platforms to Monitor
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input type="checkbox" defaultChecked className="mr-2" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Twitter</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" defaultChecked className="mr-2" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Reddit</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" className="mr-2" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">YouTube</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Detection Settings */}
        <div className="dashboard-card">
          <div className="flex items-center space-x-2 mb-4">
            <Shield className="h-5 w-5 text-red-600" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Detection Settings
            </h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Risk Threshold
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                defaultValue="0.7"
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                <span>Low</span>
                <span>High</span>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Minimum Campaign Volume
              </label>
              <input
                type="number"
                defaultValue="5"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>
          </div>
        </div>

        {/* Alert Settings */}
        <div className="dashboard-card">
          <div className="flex items-center space-x-2 mb-4">
            <Bell className="h-5 w-5 text-yellow-600" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Alert Settings
            </h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="flex items-center">
                <input type="checkbox" defaultChecked className="mr-2" />
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  High risk campaign alerts
                </span>
              </label>
            </div>
            
            <div>
              <label className="flex items-center">
                <input type="checkbox" defaultChecked className="mr-2" />
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  Bot detection alerts
                </span>
              </label>
            </div>
            
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" />
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  Daily summary reports
                </span>
              </label>
            </div>
          </div>
        </div>

        {/* System Information */}
        <div className="dashboard-card">
          <div className="flex items-center space-x-2 mb-4">
            <SettingsIcon className="h-5 w-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              System Information
            </h3>
          </div>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Version</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">1.0.0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Database</span>
              <span className="text-sm font-medium text-green-600">Connected</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">ML Models</span>
              <span className="text-sm font-medium text-green-600">Loaded</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Last Update</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                {new Date().toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors">
          Save Settings
        </button>
      </div>
    </div>
  );
};

export default Settings;