import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function TeacherDashboard() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [classData, setClassData] = useState(null);

  useEffect(() => {
    // Simulate loading class data
    setTimeout(() => {
      setClassData({
        totalStudents: 24,
        activeStudents: 18,
        averageProgress: 62,
        completionRate: 75,
        recentActivity: [
          {
            student: 'Sarah Johnson',
            action: 'completed "Media Uses & Effects"',
            time: '2 hours ago',
            type: 'completion'
          },
          {
            student: 'Mike Chen',
            action: 'had a 15-minute AI tutor session',
            time: '4 hours ago',
            type: 'chat'
          },
          {
            student: 'Jessica Martinez',
            action: 'started "Communication Infrastructure"',
            time: '1 day ago',
            type: 'progress'
          },
          {
            student: 'David Kim',
            action: 'asked 5 questions in AI chat',
            time: '1 day ago',
            type: 'chat'
          }
        ],
        moduleStats: [
          { id: 1, title: 'Your Four Worlds', completed: 20, inProgress: 3, notStarted: 1 },
          { id: 2, title: 'Media Uses & Effects', completed: 15, inProgress: 6, notStarted: 3 },
          { id: 3, title: 'Shared Characteristics', completed: 8, inProgress: 10, notStarted: 6 },
          { id: 4, title: 'Communication Infrastructure', completed: 5, inProgress: 8, notStarted: 11 },
          { id: 5, title: 'Books', completed: 3, inProgress: 5, notStarted: 16 }
        ]
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <TeacherDashboardSkeleton />;
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">
              Welcome, {user?.name}! 🧑‍🏫
            </h1>
            <p className="text-gray-600">
              Here's an overview of your Mass Communication class performance.
            </p>
          </div>
          <div className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
            Teacher Portal
          </div>
        </div>
      </div>

      {/* Class Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <ClassStatCard
          title="Total Students"
          value={classData.totalStudents}
          icon="👥"
          color="blue"
          subtitle="enrolled"
        />
        <ClassStatCard
          title="Active Students"
          value={classData.activeStudents}
          icon="🟢"
          color="green"
          subtitle="this week"
        />
        <ClassStatCard
          title="Average Progress"
          value={`${classData.averageProgress}%`}
          icon="📈"
          color="purple"
          subtitle="across all modules"
        />
        <ClassStatCard
          title="Completion Rate"
          value={`${classData.completionRate}%`}
          icon="✅"
          color="orange"
          subtitle="on-time submissions"
        />
      </div>

      {/* Module Progress Overview */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Module Progress Overview</h2>
        <div className="space-y-4">
          {classData.moduleStats.map((module) => (
            <ModuleProgressBar key={module.id} module={module} />
          ))}
        </div>
      </div>

      {/* Recent Student Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Student Activity</h3>
          <div className="space-y-3">
            {classData.recentActivity.map((activity, index) => (
              <ActivityItem key={index} activity={activity} />
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <QuickActionButton
              title="View Student Progress"
              description="See detailed progress for each student"
              icon="📊"
              color="blue"
            />
            <QuickActionButton
              title="Course Management"
              description="Edit modules and course content"
              icon="📚"
              color="green"
            />
            <QuickActionButton
              title="Class Analytics"
              description="Deep dive into class performance"
              icon="📈"
              color="purple"
            />
            <QuickActionButton
              title="Message Students"
              description="Send announcements or feedback"
              icon="💬"
              color="orange"
            />
          </div>
        </div>
      </div>

      {/* Class Performance Insights */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Class Performance Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <InsightCard
            title="Most Engaging Module"
            value="Media Uses & Effects"
            description="Students spend 23% more time here"
            icon="🎯"
          />
          <InsightCard
            title="AI Chat Usage"
            value="156 sessions"
            description="Students actively using Socratic method"
            icon="🤖"
          />
          <InsightCard
            title="Completion Trend"
            value="+12% this week"
            description="Improvement over last week"
            icon="📈"
          />
        </div>
      </div>
    </div>
  );
}

// Supporting Components
const ClassStatCard = ({ title, value, icon, color, subtitle }) => {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200',
    green: 'bg-green-50 border-green-200',
    purple: 'bg-purple-50 border-purple-200',
    orange: 'bg-orange-50 border-orange-200'
  };

  return (
    <div className={`rounded-lg border p-6 ${colorClasses[color]}`}>
      <div className="flex items-center">
        <div className="p-2 bg-white rounded-lg shadow-sm">
          <span className="text-2xl">{icon}</span>
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {subtitle && <p className="text-xs text-gray-500">{subtitle}</p>}
        </div>
      </div>
    </div>
  );
};

const ModuleProgressBar = ({ module }) => {
  const total = module.completed + module.inProgress + module.notStarted;
  const completedPercent = (module.completed / total) * 100;
  const inProgressPercent = (module.inProgress / total) * 100;

  return (
    <div className="border rounded-lg p-4">
      <div className="flex justify-between items-center mb-2">
        <h4 className="font-medium text-gray-800">{module.title}</h4>
        <span className="text-sm text-gray-500">
          {module.completed}/{total} completed
        </span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
        <div className="h-3 rounded-full flex">
          <div 
            className="bg-green-500 rounded-l-full"
            style={{ width: `${completedPercent}%` }}
          ></div>
          <div 
            className="bg-blue-500"
            style={{ width: `${inProgressPercent}%` }}
          ></div>
        </div>
      </div>
      
      <div className="flex justify-between text-xs text-gray-600">
        <span>✅ {module.completed} completed</span>
        <span>🔄 {module.inProgress} in progress</span>
        <span>⏳ {module.notStarted} not started</span>
      </div>
    </div>
  );
};

const ActivityItem = ({ activity }) => {
  const typeIcons = {
    completion: '✅',
    chat: '💬',
    progress: '📈'
  };

  const typeColors = {
    completion: 'bg-green-50 text-green-700',
    chat: 'bg-blue-50 text-blue-700',
    progress: 'bg-purple-50 text-purple-700'
  };

  return (
    <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${typeColors[activity.type]}`}>
        <span className="text-sm">{typeIcons[activity.type]}</span>
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-800">
          <span className="font-semibold">{activity.student}</span> {activity.action}
        </p>
        <p className="text-xs text-gray-500">{activity.time}</p>
      </div>
    </div>
  );
};

const QuickActionButton = ({ title, description, icon, color }) => {
  const colorClasses = {
    blue: 'hover:bg-blue-50 border-blue-200',
    green: 'hover:bg-green-50 border-green-200',
    purple: 'hover:bg-purple-50 border-purple-200',
    orange: 'hover:bg-orange-50 border-orange-200'
  };

  return (
    <button className={`w-full p-4 border rounded-lg text-left transition-colors ${colorClasses[color]}`}>
      <div className="flex items-center space-x-3">
        <span className="text-2xl">{icon}</span>
        <div>
          <p className="font-medium text-gray-800">{title}</p>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
      </div>
    </button>
  );
};

const InsightCard = ({ title, value, description, icon }) => {
  return (
    <div className="border rounded-lg p-4 text-center">
      <div className="text-2xl mb-2">{icon}</div>
      <h4 className="font-medium text-gray-800 mb-1">{title}</h4>
      <p className="text-xl font-bold text-blue-600 mb-1">{value}</p>
      <p className="text-xs text-gray-600">{description}</p>
    </div>
  );
};

const TeacherDashboardSkeleton = () => {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-3/4"></div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="bg-white rounded-lg shadow p-6">
            <div className="h-16 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <div className="h-32 bg-gray-200 rounded"></div>
      </div>
    </div>
  );
};
