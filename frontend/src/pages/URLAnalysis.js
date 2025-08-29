import React, { useState } from 'react';
import { 
  Link as LinkIcon, 
  Search, 
  AlertTriangle, 
  MessageCircle,
  Users,
  Hash,
  BarChart3,
  Shield,
  Clock,
  Globe,
  Heart,
  Share,
  MessageSquare
} from 'lucide-react';

const URLAnalysis = ({ darkMode }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!url.trim()) {
      setError('Please enter a valid URL');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/analyze-url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setAnalysisResult(data.data);
      } else {
        setError(data.message || 'Failed to analyze URL');
      }
    } catch (err) {
      setError('Network error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskScore) => {
    if (riskScore >= 70) return 'text-red-400';
    if (riskScore >= 40) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getRiskLabel = (riskScore) => {
    if (riskScore >= 70) return 'High Risk';
    if (riskScore >= 40) return 'Medium Risk';
    return 'Low Risk';
  };

  const getPlatformIcon = (platform) => {
    if (platform === 'Twitter') {
      return '🐦';
    }
    return '🌐'; // fallback icon
  };

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white drop-shadow-lg mb-2">
          URL Analysis
        </h1>
        <p className="text-xl text-white/80 font-medium">
          Analyze individual posts from social media platforms for anti-India sentiment
        </p>
      </div>

      {/* URL Input Section */}
      <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} slide-up`}>
        <div className="flex items-center space-x-3 mb-6">
          <LinkIcon className="h-6 w-6 text-blue-400" />
          <h2 className="text-xl font-bold text-white">
            Enter Post URL
          </h2>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-white/80 mb-2">
              Social Media Post URL
            </label>
            <div className="flex space-x-3">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://twitter.com/user/status/123... or https://x.com/user/status/..."
                className={`flex-1 ${darkMode ? 'input-modern-dark' : 'input-modern'}`}
                disabled={loading}
              />
              <button
                onClick={handleAnalyze}
                disabled={loading || !url.trim()}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="loading-spinner h-4 w-4"></div>
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4" />
                    <span>Analyze</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {error && (
            <div className="alert-high">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="h-4 w-4" />
                <span className="text-sm font-medium">{error}</span>
              </div>
            </div>
          )}

          {/* Supported Platforms */}
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <h3 className="text-sm font-semibold text-white/80 mb-2">Supported Platform:</h3>
            <div className="flex flex-wrap gap-2">
              <span className="inline-flex items-center space-x-1 px-3 py-1 rounded-lg bg-white/10 text-white/80 text-xs font-medium">
                <span>{getPlatformIcon('Twitter')}</span>
                <span>Twitter / X</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Results */}
      {analysisResult && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Analysis Results */}
          <div className="lg:col-span-2 space-y-6">
            {/* Post Details */}
            <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} scale-in`}>
              <div className="flex items-center space-x-3 mb-6">
                <Globe className="h-6 w-6 text-blue-400" />
                <h3 className="text-xl font-bold text-white">Post Details</h3>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getPlatformIcon(analysisResult.platform)}</span>
                  <div>
                    <h4 className="text-lg font-semibold text-white">{analysisResult.platform}</h4>
                    <p className="text-white/60">Platform detected from URL</p>
                  </div>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                  <h5 className="text-sm font-semibold text-white/80 mb-2">Content Preview:</h5>
                  <p className="text-white/70 text-sm leading-relaxed">
                    {analysisResult.content || "Content preview will appear here after successful URL analysis."}
                  </p>
                </div>

                {analysisResult.hashtags && analysisResult.hashtags.length > 0 && (
                  <div>
                    <h5 className="text-sm font-semibold text-white/80 mb-2 flex items-center space-x-1">
                      <Hash className="h-4 w-4" />
                      <span>Hashtags:</span>
                    </h5>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.hashtags.map((hashtag, index) => (
                        <span key={index} className="px-2 py-1 bg-blue-500/20 text-blue-300 rounded-lg text-xs font-medium">
                          {hashtag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Engagement Metrics */}
            {analysisResult.engagement && (
              <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} scale-in`} style={{animationDelay: '0.1s'}}>
                <div className="flex items-center space-x-3 mb-6">
                  <BarChart3 className="h-6 w-6 text-green-400" />
                  <h3 className="text-xl font-bold text-white">Engagement Metrics</h3>
                </div>
                
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-white/5 rounded-xl border border-white/10">
                    <Heart className="h-6 w-6 text-red-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">{analysisResult.engagement.likes || 0}</div>
                    <div className="text-sm text-white/60">Likes</div>
                  </div>
                  <div className="text-center p-4 bg-white/5 rounded-xl border border-white/10">
                    <Share className="h-6 w-6 text-blue-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">{analysisResult.engagement.shares || 0}</div>
                    <div className="text-sm text-white/60">Shares</div>
                  </div>
                  <div className="text-center p-4 bg-white/5 rounded-xl border border-white/10">
                    <MessageSquare className="h-6 w-6 text-green-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">{analysisResult.engagement.comments || 0}</div>
                    <div className="text-sm text-white/60">Comments</div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Analysis Metrics */}
          <div className="space-y-6">
            {/* Risk Assessment */}
            <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} scale-in`} style={{animationDelay: '0.2s'}}>
              <div className="flex items-center space-x-3 mb-6">
                <Shield className="h-6 w-6 text-yellow-400" />
                <h3 className="text-xl font-bold text-white">Risk Assessment</h3>
              </div>
              
              <div className="space-y-4">
                <div className="text-center">
                  <div className={`text-4xl font-bold ${getRiskColor(analysisResult.riskScore || 0)} mb-2`}>
                    {analysisResult.riskScore || 0}%
                  </div>
                  <div className={`text-sm font-semibold ${getRiskColor(analysisResult.riskScore || 0)}`}>
                    {getRiskLabel(analysisResult.riskScore || 0)}
                  </div>
                </div>
                
                <div className="progress-bar">
                  <div 
                    className="h-2 rounded-full transition-all duration-500"
                    style={{
                      width: `${analysisResult.riskScore || 0}%`,
                      background: analysisResult.riskScore >= 70 ? 'linear-gradient(90deg, #ef4444, #dc2626)' :
                                 analysisResult.riskScore >= 40 ? 'linear-gradient(90deg, #f59e0b, #d97706)' :
                                 'linear-gradient(90deg, #10b981, #059669)'
                    }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Sentiment Analysis */}
            <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} scale-in`} style={{animationDelay: '0.3s'}}>
              <div className="flex items-center space-x-3 mb-6">
                <MessageCircle className="h-6 w-6 text-purple-400" />
                <h3 className="text-xl font-bold text-white">Sentiment Analysis</h3>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/10">
                  <span className="text-white/80 font-medium">Sentiment</span>
                  <span className={`font-semibold ${
                    analysisResult.sentiment === 'positive' ? 'text-green-400' :
                    analysisResult.sentiment === 'negative' ? 'text-red-400' :
                    'text-yellow-400'
                  }`}>
                    {analysisResult.sentiment === 'positive' ? '😊 Positive' :
                     analysisResult.sentiment === 'negative' ? '😞 Negative' :
                     '😐 Neutral'}
                  </span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/10">
                  <span className="text-white/80 font-medium">Classification</span>
                  <span className={`font-semibold ${
                    analysisResult.classification === 'Pro-India' ? 'text-green-400' :
                    analysisResult.classification === 'Anti-India' ? 'text-red-400' :
                    'text-yellow-400'
                  }`}>
                    {analysisResult.classification || 'Neutral'}
                  </span>
                </div>
              </div>
            </div>

            {/* Bot Analysis */}
            {analysisResult.botProbability !== undefined && (
              <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} scale-in`} style={{animationDelay: '0.4s'}}>
                <div className="flex items-center space-x-3 mb-6">
                  <Users className="h-6 w-6 text-orange-400" />
                  <h3 className="text-xl font-bold text-white">Bot Analysis</h3>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-400 mb-2">
                    {analysisResult.botProbability}%
                  </div>
                  <div className="text-sm text-white/60 mb-3">
                    Bot Probability
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${analysisResult.botProbability}%`,
                        background: 'linear-gradient(90deg, #f59e0b, #d97706)'
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            )}

            {/* Analysis Timestamp */}
            <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} scale-in`} style={{animationDelay: '0.5s'}}>
              <div className="flex items-center space-x-3 mb-4">
                <Clock className="h-5 w-5 text-blue-400" />
                <h4 className="text-lg font-semibold text-white">Analysis Info</h4>
              </div>
              
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-white/60">Analyzed at:</span>
                  <span className="text-white/80">{new Date().toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/60">Processing time:</span>
                  <span className="text-white/80">2.3s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/60">Model version:</span>
                  <span className="text-white/80">v2.1.0</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* No Results State */}
      {!analysisResult && !loading && (
        <div className={`${darkMode ? 'dashboard-card-dark' : 'dashboard-card'} text-center py-12`}>
          <LinkIcon className="h-16 w-16 text-white/40 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white/80 mb-2">
            No Analysis Yet
          </h3>
          <p className="text-white/60">
            Enter a social media post URL above to start the analysis
          </p>
        </div>
      )}
    </div>
  );
};

export default URLAnalysis;