import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function ProgressPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [progressData, setProgressData] = useState(null);

  useEffect(() => {
    // Simulate loading progress data
    setTimeout(() => {
      setProgressData({
        overall: 45,
        completedModules: 3,
        totalModules: 15,
        chatSessions: 12,
        insightsGained: 28,
        moduleProgress: [
          { id: 1, title: 'Your Four Worlds', progress: 100, status: 'completed', timeSpent: '2.5 hours' },
          { id: 2, title: 'Media Uses & Effects', progress: 85, status: 'in-progress', timeSpent: '1.8 hours' },
          { id: 3, title: 'Shared Characteristics', progress: 60, status: 'in-progress', timeSpent: '1.2 hours' },
          { id: 4, title: 'Communication Infrastructure', progress: 30, status: 'in-progress', timeSpent: '0.5 hours' },
          { id: 5, title: 'Books', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 6, title: 'Newspapers', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 7, title: 'Magazines', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 8, title: 'Comic Books', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 9, title: 'Photography', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 10, title: 'Recordings', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 11, title: 'Motion Pictures', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 12, title: 'Radio', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 13, title: 'Television', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 14, title: 'Video Games', progress: 0, status: 'not-started', timeSpent: '0 hours' },
          { id: 15, title: 'Economic Influencers', progress: 0, status: 'not-started', timeSpent: '0 hours' }
        ]
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-gray-800">Your Learning Progress</h1>
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-blue-100 text-blue-700 px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors"
          >
            ← Back to Dashboard
          </button>
        </div>
        <p className="text-gray-600">
          Track your journey through the Mass Communication course, {user?.name}!
        </p>
      </div>

      {/* Progress Overview */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Overall Progress</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-3xl font-bold text-blue-600">{progressData.overall}%</div>
            <div className="text-sm text-gray-600">Course Completion</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600">{progressData.completedModules}</div>
            <div className="text-sm text-gray-600">Modules Completed</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-3xl font-bold text-purple-600">{progressData.chatSessions}</div>
            <div className="text-sm text-gray-600">AI Chat Sessions</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-3xl font-bold text-orange-600">{progressData.insightsGained}</div>
            <div className="text-sm text-gray-600">Insights Gained</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div 
            className="bg-gradient-to-r from-blue-500 to-purple-500 h-4 rounded-full transition-all duration-500"
            style={{ width: `${progressData.overall}%` }}
          ></div>
        </div>
        <p className="text-center text-gray-600">
          {progressData.completedModules} of {progressData.totalModules} modules complete
        </p>
      </div>

      {/* Module Progress */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Module Progress</h3>
          <button
            onClick={() => navigate('/chat')}
            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            💬 Get Help from AI Tutor
          </button>
        </div>
        
        <div className="space-y-3">
          {progressData.moduleProgress.map((module) => (
            <div 
              key={module.id} 
              className="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => navigate(`/modules/${module.id}`)}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
                  <span className="text-xl">
                    {module.status === 'completed' ? '✅' : 
                     module.status === 'in-progress' ? '🔄' : '⏳'}
                  </span>
                  <div>
                    <h4 className="font-medium text-gray-800">{module.title}</h4>
                    <p className="text-sm text-gray-500">Time spent: {module.timeSpent}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-sm text-gray-500">{module.progress}%</span>
                  <div className={`px-2 py-1 rounded text-xs font-medium ${
                    module.status === 'completed' ? 'bg-green-100 text-green-800' :
                    module.status === 'in-progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-600'
                  }`}>
                    {module.status.replace('-', ' ')}
                  </div>
                </div>
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
          ))}
        </div>
      </div>

      {/* Learning Insights */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Learning Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
            <h4 className="font-semibold text-gray-800 mb-2">🎯 Strongest Area</h4>
            <p className="text-gray-600">Media Theory & Effects</p>
            <p className="text-sm text-gray-500 mt-1">You excel at understanding theoretical concepts</p>
          </div>
          <div className="p-4 bg-gradient-to-r from-green-50 to-teal-50 rounded-lg">
            <h4 className="font-semibold text-gray-800 mb-2">📈 Growth Area</h4>
            <p className="text-gray-600">Practical Applications</p>
            <p className="text-sm text-gray-500 mt-1">Try connecting theory to real-world examples</p>
          </div>
        </div>
        
        <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
          <h4 className="font-semibold text-gray-800 mb-2">💡 Recommendation</h4>
          <p className="text-gray-600 mb-2">
            You're making great progress! Consider spending more time with the AI tutor to deepen your understanding.
          </p>
          <button
            onClick={() => navigate('/chat')}
            className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors"
          >
            Start AI Chat Session
          </button>
        </div>
      </div>
    </div>
  );
}
