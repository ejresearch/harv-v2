import React, { useState, useEffect } from 'react';
import { BookOpen, MessageCircle, TrendingUp, Clock, Brain, Users, Award, ChevronRight, Play, Pause, BarChart3, Target, Lightbulb } from 'lucide-react';

const EnhancedDashboard = () => {
  const [user] = useState({
    name: "Sarah Chen",
    role: "Student", 
    avatar: "SC",
    enrolled: "Introduction to Mass Communication",
    startDate: "January 15, 2024"
  });

  const [stats, setStats] = useState({
    modulesCompleted: 3,
    totalModules: 15,
    studyTime: 127,
    discussionMessages: 89,
    memoryConnections: 24,
    currentStreak: 7
  });

  const [recentActivity, setRecentActivity] = useState([
    {
      id: 1,
      type: 'completion',
      title: 'Completed "Communication Infrastructure"',
      time: '2 hours ago',
      icon: '✅',
      module: 4
    },
    {
      id: 2, 
      type: 'discussion',
      title: 'AI Discussion: Media Effects Theory',
      time: '1 day ago',
      icon: '💬',
      module: 2
    },
    {
      id: 3,
      type: 'memory',
      title: 'New cross-module connection discovered',
      time: '2 days ago', 
      icon: '🧠',
      module: 3
    }
  ]);

  const modules = [
    { id: 1, title: "Your Four Worlds", icon: "🌍", progress: 100, status: "completed", timeSpent: 45 },
    { id: 2, title: "Media Uses & Effects", icon: "📺", progress: 100, status: "completed", timeSpent: 52 },
    { id: 3, title: "Shared Characteristics", icon: "🔗", progress: 100, status: "completed", timeSpent: 38 },
    { id: 4, title: "Communication Infrastructure", icon: "🌐", progress: 85, status: "in-progress", timeSpent: 41 },
    { id: 5, title: "Books", icon: "📚", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 6, title: "Newspapers", icon: "📰", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 7, title: "Magazines", icon: "📖", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 8, title: "Comic Books", icon: "📝", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 9, title: "Photography", icon: "📷", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 10, title: "Recordings", icon: "🎵", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 11, title: "Motion Pictures", icon: "🎬", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 12, title: "Radio", icon: "📻", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 13, title: "Television", icon: "📺", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 14, title: "Video Games", icon: "🎮", progress: 0, status: "not-started", timeSpent: 0 },
    { id: 15, title: "Economic Influencers", icon: "💰", progress: 0, status: "not-started", timeSpent: 0 }
  ];

  const StatCard = ({ title, value, subtitle, icon: Icon, color, trend }) => (
    <div className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-all duration-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
      {trend && (
        <div className="mt-4 flex items-center gap-1">
          <TrendingUp className="w-4 h-4 text-green-500" />
          <span className="text-sm text-green-600 font-medium">{trend}</span>
        </div>
      )}
    </div>
  );

  const ModuleCard = ({ module }) => (
    <div className={`bg-white rounded-lg border border-gray-200 p-4 hover:border-blue-300 transition-all cursor-pointer ${
      module.status === 'completed' ? 'ring-1 ring-green-100' : 
      module.status === 'in-progress' ? 'ring-1 ring-blue-100' : ''
    }`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="text-2xl">{module.icon}</div>
          <div>
            <h4 className="font-medium text-gray-900">{module.title}</h4>
            <p className="text-xs text-gray-500">Module {module.id}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {module.status === 'completed' && (
            <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
              <span className="text-white text-xs">✓</span>
            </div>
          )}
          {module.status === 'in-progress' && (
            <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
              <Pause className="w-3 h-3 text-white" />
            </div>
          )}
          <ChevronRight className="w-4 h-4 text-gray-400" />
        </div>
      </div>
      
      <div className="mb-3">
        <div className="flex justify-between text-sm mb-1">
          <span className="text-gray-600">Progress</span>
          <span className="font-medium">{module.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full transition-all duration-300 ${
              module.status === 'completed' ? 'bg-green-500' :
              module.status === 'in-progress' ? 'bg-blue-500' : 'bg-gray-300'
            }`}
            style={{ width: `${module.progress}%` }}
          ></div>
        </div>
      </div>
      
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <Clock className="w-3 h-3" />
          {module.timeSpent} min
        </span>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          module.status === 'completed' ? 'bg-green-100 text-green-700' :
          module.status === 'in-progress' ? 'bg-blue-100 text-blue-700' :
          'bg-gray-100 text-gray-600'
        }`}>
          {module.status === 'completed' ? 'Complete' :
           module.status === 'in-progress' ? 'In Progress' : 'Not Started'}
        </span>
      </div>
    </div>
  );

  const ActivityItem = ({ activity }) => (
    <div className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
      <div className="text-lg">{activity.icon}</div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">{activity.title}</p>
        <p className="text-xs text-gray-500">{activity.time}</p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Welcome back, {user.name}! 👋
              </h1>
              <p className="text-gray-600 mt-1">Continue your journey through {user.enrolled}</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">Current Streak</p>
                <p className="text-xl font-bold text-orange-600">{stats.currentStreak} days 🔥</p>
              </div>
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                {user.avatar}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Modules Completed"
            value={`${stats.modulesCompleted}/${stats.totalModules}`}
            subtitle="3 more this week"
            icon={BookOpen}
            color="bg-blue-500"
            trend="+2 from last week"
          />
          <StatCard
            title="Study Time"
            value={`${stats.studyTime}m`}
            subtitle="This week"
            icon={Clock}
            color="bg-green-500"
            trend="+15% increase"
          />
          <StatCard
            title="AI Discussions"
            value={stats.discussionMessages}
            subtitle="Messages exchanged"
            icon={MessageCircle}
            color="bg-purple-500"
            trend="Very active"
          />
          <StatCard
            title="Memory Connections"
            value={stats.memoryConnections}
            subtitle="Cross-module links"
            icon={Brain}
            color="bg-orange-500"
            trend="+5 this week"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Course Progress */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Course Progress</h2>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <span>{Math.round((stats.modulesCompleted / stats.totalModules) * 100)}% Complete</span>
                  <div className="w-16 h-2 bg-gray-200 rounded-full">
                    <div 
                      className="h-2 bg-blue-500 rounded-full transition-all"
                      style={{ width: `${(stats.modulesCompleted / stats.totalModules) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {modules.slice(0, 8).map(module => (
                  <ModuleCard key={module.id} module={module} />
                ))}
              </div>
              
              <button className="w-full mt-6 py-3 text-blue-600 hover:text-blue-700 font-medium transition-colors">
                View All Modules ({modules.length})
              </button>
            </div>

            {/* Learning Analytics */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Learning Analytics</h2>
              
              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <BarChart3 className="w-6 h-6 text-blue-600 mx-auto mb-2" />
                  <p className="text-sm font-medium text-blue-900">Study Pattern</p>
                  <p className="text-xs text-blue-700">Consistent</p>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <Target className="w-6 h-6 text-green-600 mx-auto mb-2" />
                  <p className="text-sm font-medium text-green-900">Focus Areas</p>
                  <p className="text-xs text-green-700">Theory & Practice</p>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <Lightbulb className="w-6 h-6 text-purple-600 mx-auto mb-2" />
                  <p className="text-sm font-medium text-purple-900">Insights</p>
                  <p className="text-xs text-purple-700">High Discovery</p>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Questions Asked</span>
                  <span className="text-sm font-medium">47</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Concepts Mastered</span>
                  <span className="text-sm font-medium">12/18</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Discussion Quality</span>
                  <span className="text-sm font-medium text-green-600">Excellent</span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Continue Learning</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button className="p-4 border-2 border-dashed border-blue-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-all text-left">
                  <div className="flex items-center gap-3 mb-2">
                    <Play className="w-5 h-5 text-blue-600" />
                    <span className="font-medium text-blue-900">Resume Module 4</span>
                  </div>
                  <p className="text-sm text-blue-700">Communication Infrastructure</p>
                  <p className="text-xs text-blue-600 mt-1">15 minutes remaining</p>
                </button>
                
                <button className="p-4 border-2 border-dashed border-green-300 rounded-lg hover:border-green-400 hover:bg-green-50 transition-all text-left">
                  <div className="flex items-center gap-3 mb-2">
                    <MessageCircle className="w-5 h-5 text-green-600" />
                    <span className="font-medium text-green-900">AI Discussion</span>
                  </div>
                  <p className="text-sm text-green-700">Ask questions about any topic</p>
                  <p className="text-xs text-green-600 mt-1">Always available</p>
                </button>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Recent Activity */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Recent Activity</h3>
              <div className="space-y-1">
                {recentActivity.map(activity => (
                  <ActivityItem key={activity.id} activity={activity} />
                ))}
              </div>
              <button className="w-full mt-4 py-2 text-sm text-blue-600 hover:text-blue-700 font-medium">
                View All Activity
              </button>
            </div>

            {/* Memory System Status */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <Brain className="w-5 h-5 text-purple-600" />
                <h3 className="font-semibold text-gray-900">Enhanced Memory</h3>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Profile Completeness</span>
                  <span className="text-sm font-medium text-green-600">95%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Learning Patterns</span>
                  <span className="text-sm font-medium text-blue-600">Active</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Cross-Connections</span>
                  <span className="text-sm font-medium text-purple-600">{stats.memoryConnections}</span>
                </div>
              </div>
              
              <div className="mt-4 p-3 bg-purple-50 rounded-lg">
                <p className="text-sm text-purple-800 font-medium">Memory Insight</p>
                <p className="text-xs text-purple-700 mt-1">
                  Your learning style shows strong visual-conceptual preferences. 
                  The AI is adapting discussions accordingly.
                </p>
              </div>
            </div>

            {/* Achievements */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <Award className="w-5 h-5 text-yellow-600" />
                <h3 className="font-semibold text-gray-900">Achievements</h3>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                    <span className="text-lg">🏆</span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">First Module Master</p>
                    <p className="text-xs text-gray-600">Completed your first module</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-lg">💬</span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Discussion Expert</p>
                    <p className="text-xs text-gray-600">50+ meaningful exchanges</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                    <span className="text-lg">🧠</span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Connection Maker</p>
                    <p className="text-xs text-gray-600">Discovered 20+ links</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Study Schedule */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="font-semibold text-gray-900 mb-4">This Week's Plan</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">Today</span>
                  <span className="text-sm font-medium text-blue-600">Module 4 Discussion</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">Tomorrow</span>
                  <span className="text-sm font-medium">Complete Module 4</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">Friday</span>
                  <span className="text-sm font-medium">Start Module 5: Books</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedDashboard;
