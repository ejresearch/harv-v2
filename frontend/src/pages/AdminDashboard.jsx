import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function AdminDashboard() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [systemData, setSystemData] = useState(null);

  useEffect(() => {
    // Simulate loading system data
    setTimeout(() => {
      setSystemData({
        totalUsers: 156,
        totalCourses: 1,
        systemUptime: '99.9%',
        apiCalls: 2847,
        activeUsers: 42,
        systemHealth: {
          database: { status: 'healthy', response: '12ms' },
          api: { status: 'healthy', response: '45ms' },
          ai: { status: 'healthy', response: '230ms' },
          storage: { status: 'healthy', usage: '68%' }
        },
        recentEvents: [
          {
            type: 'user',
            description: 'New user registered: sarah.johnson@university.edu',
            time: '5 minutes ago',
            severity: 'info'
          },
          {
            type: 'system',
            description: 'Database backup completed successfully',
            time: '2 hours ago',
            severity: 'success'
          },
          {
            type: 'performance',
            description: 'API response time improved by 15%',
            time: '1 day ago',
            severity: 'success'
          },
          {
            type: 'maintenance',
            description: 'Scheduled maintenance window completed',
            time: '2 days ago',
            severity: 'info'
          }
        ],
        userStats: {
          students: 124,
          teachers: 28,
          admins: 4
        },
        usage: {
          dailyLogins: 87,
          chatSessions: 156,
          modulesCompleted: 45,
          averageSessionTime: '23 minutes'
        }
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <AdminDashboardSkeleton />;
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">
              System Administration ⚙️
            </h1>
            <p className="text-gray-600">
              Welcome, {user?.name}! Monitor and manage your Harv v2.0 system.
            </p>
          </div>
          <div className="text-sm bg-red-100 text-red-700 px-3 py-1 rounded-full">
            Admin Portal
          </div>
        </div>
      </div>

      {/* System Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <SystemStatCard
          title="Total Users"
          value={systemData.totalUsers}
          icon="👤"
          color="blue"
          subtitle="registered accounts"
        />
        <SystemStatCard
          title="System Uptime"
          value={systemData.systemUptime}
          icon="⚡"
          color="green"
          subtitle="last 30 days"
        />
        <SystemStatCard
          title="API Calls"
          value={systemData.apiCalls.toLocaleString()}
          icon="🔗"
          color="purple"
          subtitle="today"
        />
        <SystemStatCard
          title="Active Users"
          value={systemData.activeUsers}
          icon="🟢"
          color="orange"
          subtitle="online now"
        />
      </div>

      {/* System Health Dashboard */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">System Health</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(systemData.systemHealth).map(([service, data]) => (
            <SystemHealthCard key={service} service={service} data={data} />
          ))}
        </div>

        {/* Performance Graphs Placeholder */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Performance Metrics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricCard
              title="Response Time"
              value="125ms"
              trend="-12%"
              trendType="positive"
            />
            <MetricCard
              title="Error Rate"
              value="0.02%"
              trend="-45%"
              trendType="positive"
            />
            <MetricCard
              title="Throughput"
              value="1.2k req/min"
              trend="+8%"
              trendType="positive"
            />
          </div>
        </div>
      </div>

      {/* User Management & Usage Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* User Management */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">User Management</h3>
          
          <div className="space-y-4">
            <UserTypeCard
              type="Students"
              count={systemData.userStats.students}
              icon="🎓"
              color="blue"
            />
            <UserTypeCard
              type="Teachers"
              count={systemData.userStats.teachers}
              icon="🧑‍🏫"
              color="green"
            />
            <UserTypeCard
              type="Administrators"
              count={systemData.userStats.admins}
              icon="⚙️"
              color="red"
            />
          </div>

          <div className="mt-4 pt-4 border-t">
            <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
              Manage Users
            </button>
          </div>
        </div>

        {/* Usage Analytics */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Usage Analytics</h3>
          
          <div className="space-y-4">
            <UsageMetric
              label="Daily Logins"
              value={systemData.usage.dailyLogins}
              icon="🔐"
            />
            <UsageMetric
              label="Chat Sessions"
              value={systemData.usage.chatSessions}
              icon="💬"
            />
            <UsageMetric
              label="Modules Completed"
              value={systemData.usage.modulesCompleted}
              icon="✅"
            />
            <UsageMetric
              label="Avg Session Time"
              value={systemData.usage.averageSessionTime}
              icon="⏱️"
            />
          </div>
        </div>
      </div>

      {/* Recent System Events */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent System Events</h3>
        <div className="space-y-3">
          {systemData.recentEvents.map((event, index) => (
            <SystemEventItem key={index} event={event} />
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <AdminQuickAction
            title="Backup System"
            icon="💾"
            color="blue"
          />
          <AdminQuickAction
            title="View Logs"
            icon="📋"
            color="gray"
          />
          <AdminQuickAction
            title="System Settings"
            icon="⚙️"
            color="purple"
          />
          <AdminQuickAction
            title="Security Audit"
            icon="🔒"
            color="red"
          />
        </div>
      </div>
    </div>
  );
}

// Supporting Components
const SystemStatCard = ({ title, value, icon, color, subtitle }) => {
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

const SystemHealthCard = ({ service, data }) => {
  const isHealthy = data.status === 'healthy';
  const statusColor = isHealthy ? 'text-green-600' : 'text-red-600';
  const bgColor = isHealthy ? 'bg-green-50' : 'bg-red-50';
  const borderColor = isHealthy ? 'border-green-200' : 'border-red-200';

  return (
    <div className={`rounded-lg border p-4 ${bgColor} ${borderColor}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700 capitalize">{service}</span>
        <div className={`w-3 h-3 rounded-full ${isHealthy ? 'bg-green-500' : 'bg-red-500'}`}></div>
      </div>
      <p className={`text-sm font-semibold ${statusColor} capitalize`}>
        {data.status}
      </p>
      {data.response && (
        <p className="text-xs text-gray-600">Response: {data.response}</p>
      )}
      {data.usage && (
        <p className="text-xs text-gray-600">Usage: {data.usage}</p>
      )}
    </div>
  );
};

const MetricCard = ({ title, value, trend, trendType }) => {
  const trendColor = trendType === 'positive' ? 'text-green-600' : 'text-red-600';
  const trendIcon = trendType === 'positive' ? '↗️' : '↘️';

  return (
    <div className="text-center">
      <p className="text-sm text-gray-600">{title}</p>
      <p className="text-xl font-bold text-gray-900">{value}</p>
      <p className={`text-sm ${trendColor}`}>
        {trendIcon} {trend}
      </p>
    </div>
  );
};

const UserTypeCard = ({ type, count, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-700',
    green: 'bg-green-100 text-green-700',
    red: 'bg-red-100 text-red-700'
  };

  return (
    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
      <div className="flex items-center space-x-3">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${colorClasses[color]}`}>
          <span className="text-sm">{icon}</span>
        </div>
        <span className="font-medium text-gray-700">{type}</span>
      </div>
      <span className="text-lg font-bold text-gray-900">{count}</span>
    </div>
  );
};

const UsageMetric = ({ label, value, icon }) => {
  return (
    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
      <div className="flex items-center space-x-3">
        <span className="text-lg">{icon}</span>
        <span className="font-medium text-gray-700">{label}</span>
      </div>
      <span className="text-lg font-bold text-gray-900">{value}</span>
    </div>
  );
};

const SystemEventItem = ({ event }) => {
  const severityColors = {
    info: 'bg-blue-50 text-blue-700 border-blue-200',
    success: 'bg-green-50 text-green-700 border-green-200',
    warning: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    error: 'bg-red-50 text-red-700 border-red-200'
  };

  const typeIcons = {
    user: '👤',
    system: '⚙️',
    performance: '📊',
    maintenance: '🔧',
    security: '🔒'
  };

  return (
    <div className={`border rounded-lg p-3 ${severityColors[event.severity]}`}>
      <div className="flex items-center space-x-3">
        <span className="text-lg">{typeIcons[event.type] || '📝'}</span>
        <div className="flex-1">
          <p className="text-sm font-medium">{event.description}</p>
          <p className="text-xs opacity-75">{event.time}</p>
        </div>
      </div>
    </div>
  );
};

const AdminQuickAction = ({ title, icon, color }) => {
  const colorClasses = {
    blue: 'hover:bg-blue-50 border-blue-200',
    gray: 'hover:bg-gray-50 border-gray-200',
    purple: 'hover:bg-purple-50 border-purple-200',
    red: 'hover:bg-red-50 border-red-200'
  };

  return (
    <button className={`p-4 border rounded-lg text-center transition-colors ${colorClasses[color]}`}>
      <div className="text-2xl mb-2">{icon}</div>
      <p className="text-sm font-medium text-gray-700">{title}</p>
    </button>
  );
};

const AdminDashboardSkeleton = () => {
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
