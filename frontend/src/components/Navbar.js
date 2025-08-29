import React from 'react';
import { Menu, X, Shield, Moon, Sun, Bell, Search } from 'lucide-react';

const Navbar = ({ sidebarOpen, setSidebarOpen, darkMode, toggleDarkMode }) => {
  return (
    <nav className={`${darkMode ? 'glass-dark' : 'glass-card'} border-b border-white/20 backdrop-blur-md relative z-20`}>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Left side */}
          <div className="flex items-center">
            <button
              type="button"
              className="lg:hidden -ml-2 mr-2 flex h-10 w-10 items-center justify-center rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              {sidebarOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
            
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Shield className="h-10 w-10 text-white drop-shadow-lg" />
                <div className="absolute inset-0 h-10 w-10 bg-white/20 rounded-full blur-xl"></div>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-2xl font-bold text-white drop-shadow-sm">
                  HexaCiphers
                </h1>
                <p className="text-sm text-white/80 font-medium">
                  Anti-India Campaign Detection
                </p>
              </div>
            </div>
          </div>

          {/* Center - Search bar */}
          <div className="hidden md:flex flex-1 max-w-lg mx-8">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-white/60" />
              <input
                type="text"
                placeholder="Search campaigns, posts, users..."
                className="w-full pl-10 pr-4 py-2 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-white/30 backdrop-blur-sm transition-all duration-200"
              />
            </div>
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-3">
            {/* Notifications */}
            <button className="relative flex h-10 w-10 items-center justify-center rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200">
              <Bell className="h-5 w-5" />
              <div className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full pulse-status"></div>
            </button>

            {/* Dark mode toggle */}
            <button
              onClick={toggleDarkMode}
              className="flex h-10 w-10 items-center justify-center rounded-xl text-white/80 hover:text-white hover:bg-white/10 transition-all duration-200"
            >
              {darkMode ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </button>

            {/* Status indicator */}
            <div className="hidden sm:flex items-center space-x-2 px-3 py-2 rounded-xl bg-white/10 backdrop-blur-sm">
              <div className="h-2 w-2 bg-green-400 rounded-full pulse-status"></div>
              <span className="text-sm text-white/90 font-medium">
                System Active
              </span>
            </div>

            {/* User profile */}
            <div className="flex items-center space-x-2 cursor-pointer hover:bg-white/10 rounded-xl px-3 py-2 transition-all duration-200">
              <div className="h-8 w-8 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full flex items-center justify-center shadow-lg">
                <span className="text-xs font-bold text-white">A</span>
              </div>
              <span className="hidden sm:block text-sm font-semibold text-white">
                Admin
              </span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;