import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';

const StudentDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [courseProgress, setCourseProgress] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [currentModule, setCurrentModule] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [progress, modules] = await Promise.all([
        api.getUserOverview(user.id),
        api.getModules()
      ]);
      
      setCourseProgress(progress);
      setCurrentModule(findCurrentModule(modules, progress));
      setRecentActivity(progress.recent_activity || []);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
      // Set demo data if API fails
      const demoProgress = {
        completed_modules: 2,
        overall_progress: 35,
        chat_sessions: 5,
        insights_gained: 12,
        module_progress: {
          1: { completion_percentage: 100 },
          2: { completion_percentage: 75 },
          3: { completion_percentage: 30 }
        }
      };
      setCourseProgress(demoProgress);
      setCurrentModule({ id: 2, title: 'Media Uses & Effects', description: 'Explore how media functions in society' });
      setRecentActivity([
        { type: 'chat', description: 'Discussed media effects theory', timestamp: new Date().toISOString() },
        { type: 'module_complete', description: 'Completed "Your Four Worlds"', timestamp: new Date().toISOString() }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const findCurrentModule = (modules, progress) => {
    // Find the first incomplete module or default to module 1
    const incomplete = modules?.find(m => (progress.module_progress?.[m.id]?.completion_percentage || 0) < 100);
    return incomplete || { id: 1, title: 'Your Four Worlds', description: 'Communication models and the four worlds we live in' };
  };

  if (loading) {
    return <DashboardLoading />;
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          Welcome back, {user?.name}!
        </h1>
        <p className="text-gray-600 mb-4">
          Continue your journey through the evolution of mass communication
        </p>
        
        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard 
            title="Modules Completed" 
            value={`${courseProgress?.completed_modules || 0}/15`}
            icon="📚" 
            color="blue"
          />
          <StatCard 
            title="Overall Progress" 
            value={`${Math.round(courseProgress?.overall_progress || 0)}%`}
            icon="📊" 
            color="green"
          />
          <StatCard 
            title="AI Conversations" 
            value={courseProgress?.chat_sessions || 0}
            icon="💬" 
            color="purple"
          />
          <StatCard 
            title="Learning Insights" 
            value={courseProgress?.insights_gained || 0}
            icon="💡" 
            color="orange"
          />
        </div>
      </div>

      {/* Current Module Progress */}
      {currentModule && (
        <CurrentModuleCard 
          module={currentModule}
          progress={courseProgress?.module_progress?.[currentModule.id]}
          onContinue={() => navigate(`/modules/${currentModule.id}`)}
        />
      )}

      {/* Course Timeline - Media Evolution */}
      <MediaEvolutionTimeline 
        progress={courseProgress}
        onModuleClick={(moduleId) => navigate(`/modules/${moduleId}`)}
      />

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <QuickActionCard 
          title="Continue Learning"
          description="Pick up where you left off in your current module"
          action={() => navigate(`/modules/${currentModule?.id || 1}`)}
          icon="🎓"
          gradient="from-blue-500 to-purple-600"
        />
        <QuickActionCard 
          title="Chat with AI Tutor"
          description="Ask questions about communication theory"
          action={() => navigate('/chat')}
          icon="🤖"
          gradient="from-green-500 to-teal-600"
        />
      </div>

      {/* Recent Activity */}
      <RecentActivityFeed activities={recentActivity} />
    </div>
  );
};

// Supporting Components
const StatCard = ({ title, value, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    purple: 'bg-purple-50 text-purple-600 border-purple-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200'
  };

  return (
    <div className={`rounded-lg border p-4 ${colorClasses[color]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium opacity-80">{title}</p>
          <p className="text-2xl font-bold">{value}</p>
        </div>
        <span className="text-2xl">{icon}</span>
      </div>
    </div>
  );
};

const CurrentModuleCard = ({ module, progress, onContinue }) => (
  <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl shadow-lg text-white p-6">
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <h2 className="text-xl font-bold mb-2">
          Continue Learning: {module.title}
        </h2>
        <p className="text-indigo-100 mb-4">{module.description}</p>
        
        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-sm mb-1">
            <span>Progress</span>
            <span>{Math.round(progress?.completion_percentage || 0)}%</span>
          </div>
          <div className="bg-indigo-400 bg-opacity-30 rounded-full h-2">
            <div 
              className="bg-white rounded-full h-2 transition-all duration-300"
              style={{ width: `${progress?.completion_percentage || 0}%` }}
            />
          </div>
        </div>
        
        <button
          onClick={onContinue}
          className="bg-white text-indigo-600 px-6 py-2 rounded-lg font-semibold hover:bg-indigo-50 transition-colors"
        >
          Continue Learning →
        </button>
      </div>
      <div className="text-6xl opacity-20 ml-6">
        {getModuleIcon(module.id)}
      </div>
    </div>
  </div>
);

const MediaEvolutionTimeline = ({ progress, onModuleClick }) => {
  const courseModules = [
    { id: 1, title: 'Your Four Worlds', icon: '🌍', era: 'Foundation' },
    { id: 2, title: 'Media Uses & Effects', icon: '📺', era: 'Theory' },
    { id: 3, title: 'Shared Characteristics', icon: '🔗', era: 'Theory' },
    { id: 4, title: 'Communication Infrastructure', icon: '📡', era: 'Infrastructure' },
    { id: 5, title: 'Books', icon: '📚', era: 'Print Era' },
    { id: 6, title: 'Newspapers', icon: '📰', era: 'Print Era' },
    { id: 7, title: 'Magazines', icon: '📖', era: 'Print Era' },
    { id: 8, title: 'Comic Books', icon: '💭', era: 'Visual Media' },
    { id: 9, title: 'Photography', icon: '📷', era: 'Visual Media' },
    { id: 10, title: 'Recordings', icon: '🎵', era: 'Audio Era' },
    { id: 11, title: 'Motion Pictures', icon: '🎬', era: 'Visual Media' },
    { id: 12, title: 'Radio', icon: '📻', era: 'Broadcast Era' },
    { id: 13, title: 'Television', icon: '📺', era: 'Broadcast Era' },
    { id: 14, title: 'Video Games', icon: '🎮', era: 'Digital Era' },
    { id: 15, title: 'Economic Influencers', icon: '💰', era: 'Modern' }
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6">
        Media Evolution Timeline
      </h2>
      
      <div className="space-y-4">
        {courseModules.map((module, index) => {
          const moduleProgress = progress?.module_progress?.[module.id];
          const isCompleted = (moduleProgress?.completion_percentage || 0) >= 100;
          const isInProgress = (moduleProgress?.completion_percentage || 0) > 0;
          const isLocked = index > 0 && (progress?.module_progress?.[courseModules[index-1].id]?.completion_percentage || 0) < 80;
          
          return (
            <TimelineModule
              key={module.id}
              module={module}
              progress={moduleProgress}
              isCompleted={isCompleted}
              isInProgress={isInProgress}
              isLocked={isLocked}
              onClick={() => !isLocked && onModuleClick(module.id)}
            />
          );
        })}
      </div>
    </div>
  );
};

const TimelineModule = ({ module, progress, isCompleted, isInProgress, isLocked, onClick }) => {
  const getStatusColor = () => {
    if (isLocked) return 'bg-gray-100 text-gray-400';
    if (isCompleted) return 'bg-green-100 text-green-600 border-green-200';
    if (isInProgress) return 'bg-blue-100 text-blue-600 border-blue-200';
    return 'bg-gray-50 text-gray-600 hover:bg-gray-100';
  };

  return (
    <div 
      className={`flex items-center p-4 rounded-lg border cursor-pointer transition-colors ${getStatusColor()}`}
      onClick={onClick}
    >
      <div className="flex items-center flex-1">
        <span className="text-2xl mr-4">{module.icon}</span>
        <div className="flex-1">
          <h3 className="font-semibold">{module.title}</h3>
          <p className="text-sm opacity-75">{module.era}</p>
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        {progress && (
          <div className="text-right">
            <div className="text-sm font-medium">
              {Math.round(progress.completion_percentage || 0)}%
            </div>
            <div className="w-16 bg-gray-200 rounded-full h-1 mt-1">
              <div 
                className="bg-current rounded-full h-1 transition-all duration-300"
                style={{ width: `${progress.completion_percentage || 0}%` }}
              />
            </div>
          </div>
        )}
        
        <div className="text-lg">
          {isLocked ? '🔒' : isCompleted ? '✅' : isInProgress ? '⏳' : '○'}
        </div>
      </div>
    </div>
  );
};

const QuickActionCard = ({ title, description, action, icon, gradient }) => (
  <div className={`bg-gradient-to-r ${gradient} rounded-xl shadow-lg text-white p-6 cursor-pointer transform hover:scale-105 transition-transform`}
       onClick={action}>
    <div className="flex items-center justify-between">
      <div>
        <h3 className="text-lg font-bold mb-2">{title}</h3>
        <p className="text-white text-opacity-90 text-sm">{description}</p>
      </div>
      <span className="text-3xl opacity-80">{icon}</span>
    </div>
  </div>
);

const RecentActivityFeed = ({ activities }) => (
  <div className="bg-white rounded-xl shadow-sm p-6">
    <h2 className="text-xl font-bold text-gray-800 mb-4">Recent Activity</h2>
    
    {activities.length === 0 ? (
      <div className="text-center py-8 text-gray-500">
        <span className="text-4xl mb-4 block">📚</span>
        <p>Start learning to see your activity here!</p>
      </div>
    ) : (
      <div className="space-y-3">
        {activities.map((activity, index) => (
          <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
            <span className="text-lg mr-3">{getActivityIcon(activity.type)}</span>
            <div className="flex-1">
              <p className="text-sm font-medium">{activity.description}</p>
              <p className="text-xs text-gray-500">{formatTimeAgo(activity.timestamp)}</p>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);

const DashboardLoading = () => (
  <div className="space-y-6">
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3 mb-6"></div>
        <div className="grid grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

// Helper Functions
const getModuleIcon = (moduleId) => {
  const icons = {
    1: '🌍', 2: '📺', 3: '🔗', 4: '📡', 5: '📚',
    6: '📰', 7: '📖', 8: '💭', 9: '📷', 10: '🎵',
    11: '🎬', 12: '📻', 13: '📺', 14: '🎮', 15: '💰'
  };
  return icons[moduleId] || '📚';
};

const getActivityIcon = (type) => {
  const icons = {
    chat: '💬',
    module_complete: '✅',
    insight_gained: '💡',
    progress: '📊'
  };
  return icons[type] || '📚';
};

const formatTimeAgo = (timestamp) => {
  const now = new Date();
  const time = new Date(timestamp);
  const diffInHours = Math.floor((now - time) / (1000 * 60 * 60));
  
  if (diffInHours < 1) return 'Just now';
  if (diffInHours < 24) return `${diffInHours} hours ago`;
  return `${Math.floor(diffInHours / 24)} days ago`;
};

export default StudentDashboard;
