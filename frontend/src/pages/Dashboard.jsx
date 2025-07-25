import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Dashboard() {
  const { user, userRole } = useAuth();
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    // Simulate loading dashboard data
    setTimeout(() => {
      setDashboardData({
        student: {
          completedModules: 3,
          totalModules: 15,
          overallProgress: 45,
          chatSessions: 12,
          insightsGained: 28,
          currentModule: {
            id: 4,
            title: 'Communication Infrastructure',
            progress: 30
          },
          recentActivity: [
            { type: 'module_complete', description: 'Completed "Media Uses & Effects"', time: '2 hours ago' },
            { type: 'chat', description: 'Had a discussion about media theory', time: '1 day ago' },
            { type: 'progress', description: 'Made progress in "Shared Characteristics"', time: '2 days ago' }
          ]
        },
        teacher: {
          totalStudents: 24,
          activeStudents: 18,
          averageProgress: 62,
          completionRate: 75
        },
        admin: {
          totalUsers: 156,
          systemUptime: '99.9%',
          apiCalls: 2847,
          activeCoursesCount: 1
        }
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <DashboardSkeleton />;
  }

  // Route to appropriate dashboard based on role
  if (userRole === 'educator') {
    return <TeacherDashboardContent data={dashboardData.teacher} user={user} />;
  }

  if (userRole === 'admin') {
    return <AdminDashboardContent data={dashboardData.admin} user={user} />;
  }

  // Default to student dashboard for 'student' and 'universal' roles
  return <StudentDashboardContent data={dashboardData.student} user={user} userRole={userRole} />;
}

// Student Dashboard Component
const StudentDashboardContent = ({ data, user, userRole }) => {
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">
              Welcome back, {user?.name}! 👋
            </h1>
            <p className="text-gray-600">
              Ready to continue your Mass Communication journey?
            </p>
          </div>
          {userRole === 'universal' && (
            <div className="text-sm bg-purple-100 text-purple-700 px-3 py-1 rounded-full">
              🔄 Universal Access
            </div>
          )}
        </div>
      </div>

      {/* Progress Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Overall Progress"
          value={`${data.overallProgress}%`}
          icon="📊"
          color="blue"
          subtitle={`${data.completedModules}/${data.totalModules} modules`}
        />
        <StatCard
          title="Chat Sessions"
          value={data.chatSessions}
          icon="💬"
          color="green"
          subtitle="with AI tutor"
        />
        <StatCard
          title="Insights Gained"
          value={data.insightsGained}
          icon="💡"
          color="purple"
          subtitle="learning moments"
        />
        <StatCard
          title="Current Module"
          value={data.currentModule.progress + '%'}
          icon="📚"
          color="orange"
          subtitle={data.currentModule.title}
        />
      </div>

      {/* Current Module Progress */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-800">Continue Learning</h2>
          <Link
            to={`/modules/${data.currentModule.id}`}
            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            View Module →
          </Link>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📡</span>
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-gray-800">{data.currentModule.title}</h3>
              <p className="text-sm text-gray-600 mb-2">
                Understanding how communication systems work
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${data.currentModule.progress}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">{data.currentModule.progress}% complete</p>
            </div>
            <Link
              to={`/modules/${data.currentModule.id}`}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Continue
            </Link>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <QuickActionCard
          title="Chat with AI Tutor"
          description="Ask questions about communication theory and get Socratic guidance"
          icon="🤖"
          action={() => window.location.href = '/chat'}
          gradient="from-green-500 to-teal-600"
        />
        <QuickActionCard
          title="View All Modules"
          description="Browse through all 15 Mass Communication modules"
          icon="📚"
          action={() => window.location.href = '/modules/1'}
          gradient="from-purple-500 to-pink-600"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          {data.recentActivity.map((activity, index) => (
            <ActivityItem key={index} {...activity} />
          ))}
        </div>
      </div>
    </div>
  );
};

// Teacher Dashboard Content
const TeacherDashboardContent = ({ data, user }) => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          Teacher Dashboard
        </h1>
        <p className="text-gray-600">
          Welcome, {user?.name}! Here's your class overview.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Total Students"
          value={data.totalStudents}
          icon="👥"
          color="blue"
        />
        <StatCard
          title="Active Students"
          value={data.activeStudents}
          icon="🟢"
          color="green"
        />
        <StatCard
          title="Average Progress"
          value={`${data.averageProgress}%`}
          icon="📈"
          color="purple"
        />
        <StatCard
          title="Completion Rate"
          value={`${data.completionRate}%`}
          icon="✅"
          color="orange"
        />
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Class Management</h3>
        <p className="text-gray-600">Full teacher features coming soon...</p>
      </div>
    </div>
  );
};

// Admin Dashboard Content
const AdminDashboardContent = ({ data, user }) => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          System Administration
        </h1>
        <p className="text-gray-600">
          Welcome, {user?.name}! System status overview.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Total Users"
          value={data.totalUsers}
          icon="👤"
          color="blue"
        />
        <StatCard
          title="System Uptime"
          value={data.systemUptime}
          icon="⚡"
          color="green"
        />
        <StatCard
          title="API Calls"
          value={data.apiCalls.toLocaleString()}
          icon="🔗"
          color="purple"
        />
        <StatCard
          title="Active Courses"
          value={data.activeCoursesCount}
          icon="📚"
          color="orange"
        />
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">System Health</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
            <span className="text-sm font-medium">Database</span>
            <span className="flex items-center text-sm text-green-600">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Healthy
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
            <span className="text-sm font-medium">API Services</span>
            <span className="flex items-center text-sm text-green-600">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Online
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
            <span className="text-sm font-medium">AI Services</span>
            <span className="flex items-center text-sm text-green-600">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Active
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Reusable Components
const StatCard = ({ title, value, icon, color, subtitle }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    purple: 'bg-purple-50 text-purple-600 border-purple-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200'
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
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

const QuickActionCard = ({ title, description, icon, action, gradient }) => {
  return (
    <div className={`bg-gradient-to-r ${gradient} rounded-lg p-6 text-white cursor-pointer transform hover:scale-105 transition-transform`}
         onClick={action}>
      <div className="flex items-center space-x-4">
        <span className="text-3xl">{icon}</span>
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          <p className="text-sm opacity-90">{description}</p>
        </div>
      </div>
    </div>
  );
};

const ActivityItem = ({ type, description, time }) => {
  const icons = {
    module_complete: '✅',
    chat: '💬',
    progress: '📈'
  };

  return (
    <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
      <span className="text-lg">{icons[type] || '📝'}</span>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-800">{description}</p>
        <p className="text-xs text-gray-500">{time}</p>
      </div>
    </div>
  );
};

const DashboardSkeleton = () => {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
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
