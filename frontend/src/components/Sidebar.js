import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  BarChart3, 
  Shield, 
  TrendingUp, 
  Settings, 
  AlertTriangle,
  X,
  Link as LinkIcon,
  Activity
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
  { name: 'URL Analysis', href: '/url-analysis', icon: LinkIcon },
  { name: 'Analytics', href: '/analytics', icon: TrendingUp },
  { name: 'Campaigns', href: '/campaigns', icon: AlertTriangle },
  { name: 'Settings', href: '/settings', icon: Settings },
];

const Sidebar = ({ sidebarOpen, setSidebarOpen, darkMode }) => {
  const location = useLocation();

  return (
    <>
      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 ${darkMode ? 'glass-dark' : 'glass-card'} shadow-xl transform transition-all duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 border-r border-white/20
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center justify-between px-4 border-b border-white/20">
            <div className="flex items-center space-x-2">
              <div className="relative">
                <Shield className="h-6 w-6 text-white drop-shadow-lg" />
                <div className="absolute inset-0 h-6 w-6 bg-white/20 rounded-full blur-lg"></div>
              </div>
              <span className="text-lg font-bold text-white drop-shadow-sm">
                HexaCiphers
              </span>
            </div>
            <button
              type="button"
              className="lg:hidden text-white/80 hover:text-white transition-colors duration-200"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-2 px-4 py-6">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    group flex items-center px-4 py-3 text-sm font-semibold rounded-xl transition-all duration-200 relative overflow-hidden
                    ${isActive
                      ? 'bg-white/20 text-white shadow-lg backdrop-blur-sm border border-white/30'
                      : 'text-white/80 hover:bg-white/10 hover:text-white'
                    }
                  `}
                  onClick={() => setSidebarOpen(false)}
                >
                  {isActive && (
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-400/20 to-purple-500/20 rounded-xl"></div>
                  )}
                  <item.icon
                    className={`
                      mr-3 h-5 w-5 transition-all duration-200 relative z-10
                      ${isActive
                        ? 'text-white drop-shadow-sm'
                        : 'text-white/60 group-hover:text-white/90'
                      }
                    `}
                  />
                  <span className="relative z-10">{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Quick Stats */}
          <div className="px-4 py-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-semibold text-white">
                  Live Monitoring
                </span>
                <Activity className="h-4 w-4 text-green-400 pulse-status" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-white/80">Active Campaigns</span>
                  <span className="text-red-400 font-semibold">23</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-white/80">Posts Analyzed</span>
                  <span className="text-green-400 font-semibold">1.2k</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-white/80">Risk Level</span>
                  <span className="text-yellow-400 font-semibold">Medium</span>
                </div>
              </div>
            </div>
          </div>

          {/* Status Panel */}
          <div className="border-t border-white/20 p-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-3 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-white">
                  System Status
                </span>
                <div className="h-2 w-2 bg-green-400 rounded-full pulse-status"></div>
              </div>
              <div className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-white/80">API</span>
                  <span className="text-green-400 font-medium">Online</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-white/80">ML Models</span>
                  <span className="text-green-400 font-medium">Ready</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-white/80">Database</span>
                  <span className="text-green-400 font-medium">Connected</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;