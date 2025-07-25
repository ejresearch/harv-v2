import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginPage } from './components/auth/LoginPage';

// Import your page components
import Dashboard from './pages/Dashboard';
import ModulePage from './pages/ModulePage';
import ChatPage from './pages/ChatPage';
import ProgressPage from './pages/ProgressPage';
import TeacherDashboard from './pages/TeacherDashboard';
import AdminDashboard from './pages/AdminDashboard';

// Layout Components
const Layout = ({ children }) => {
  const { user, userRole, logout } = useAuth();

  const navigationItems = {
    student: [
      { icon: '🏠', label: 'Dashboard', path: '/dashboard' },
      { icon: '💬', label: 'AI Tutor', path: '/chat' },
      { icon: '📊', label: 'Progress', path: '/progress' },
      { icon: '📚', label: 'Modules', path: '/modules' }
    ],
    educator: [
      { icon: '🏠', label: 'Dashboard', path: '/teacher' },
      { icon: '👥', label: 'Students', path: '/students' },
      { icon: '📚', label: 'Course Management', path: '/course' },
      { icon: '📊', label: 'Analytics', path: '/analytics' }
    ],
    admin: [
      { icon: '🏠', label: 'Dashboard', path: '/admin' },
      { icon: '👥', label: 'Users', path: '/users' },
      { icon: '⚙️', label: 'Settings', path: '/settings' },
      { icon: '📊', label: 'System Analytics', path: '/system-analytics' }
    ],
    universal: [
      { icon: '🏠', label: 'Dashboard', path: '/dashboard' },
      { icon: '💬', label: 'AI Tutor', path: '/chat' },
      { icon: '📊', label: 'Progress', path: '/progress' },
      { icon: '🧑‍🏫', label: 'Teacher View', path: '/teacher' },
      { icon: '⚙️', label: 'Admin View', path: '/admin' }
    ]
  };

  const courseModules = [
    { id: 1, title: 'Your Four Worlds', icon: '🌍', path: '/modules/1' },
    { id: 2, title: 'Media Uses & Effects', icon: '📺', path: '/modules/2' },
    { id: 3, title: 'Shared Characteristics', icon: '🔗', path: '/modules/3' },
    { id: 4, title: 'Communication Infrastructure', icon: '📡', path: '/modules/4' },
    { id: 5, title: 'Books', icon: '📚', path: '/modules/5' },
    { id: 6, title: 'Newspapers', icon: '📰', path: '/modules/6' },
    { id: 7, title: 'Magazines', icon: '📖', path: '/modules/7' },
    { id: 8, title: 'Comic Books', icon: '💭', path: '/modules/8' },
    { id: 9, title: 'Photography', icon: '📷', path: '/modules/9' },
    { id: 10, title: 'Recordings', icon: '🎵', path: '/modules/10' },
    { id: 11, title: 'Motion Pictures', icon: '🎬', path: '/modules/11' },
    { id: 12, title: 'Radio', icon: '📻', path: '/modules/12' },
    { id: 13, title: 'Television', icon: '📺', path: '/modules/13' },
    { id: 14, title: 'Video Games', icon: '🎮', path: '/modules/14' },
    { id: 15, title: 'Economic Influencers', icon: '💰', path: '/modules/15' }
  ];

  const currentNavigation = navigationItems[userRole] || navigationItems.student;

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg flex flex-col">
        {/* Header */}
        <div className="p-6 border-b">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">H</span>
            </div>
            <div>
              <h1 className="font-bold text-gray-800">Harv v2.0</h1>
              <p className="text-sm text-gray-600 capitalize">{userRole} Portal</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {currentNavigation.map((item) => (
            <NavItem key={item.path} {...item} />
          ))}

          {/* Course Modules (for students and universal) */}
          {(userRole === 'student' || userRole === 'universal') && (
            <div className="pt-6 mt-6 border-t">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Course Modules
              </h3>
              <div className="space-y-1 max-h-96 overflow-y-auto">
                {courseModules.map((module) => (
                  <ModuleNavItem key={module.id} {...module} />
                ))}
              </div>
            </div>
          )}
        </nav>

        {/* User Menu */}
        <div className="p-4 border-t">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              <span className="text-gray-600 text-sm font-medium">
                {user?.name?.charAt(0) || 'U'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-700 truncate">
                {user?.name || 'User'}
              </p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <span>🔓</span>
            <span>Sign Out</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header Bar */}
        <header className="bg-white shadow-sm border-b p-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold text-gray-800">
              Mass Communication Course
            </h1>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                Welcome back, {user?.name}!
              </div>
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-blue-600 text-sm">
                  {userRole === 'student' ? '🎓' : userRole === 'educator' ? '🧑‍🏫' : userRole === 'universal' ? '🔄' : '⚙️'}
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

// Navigation Components
const NavItem = ({ icon, label, path }) => {
  const isActive = window.location.pathname === path;
  
  return (
    <Link
      to={path}
      className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
        isActive 
          ? 'bg-blue-100 text-blue-700' 
          : 'text-gray-600 hover:bg-gray-100'
      }`}
    >
      <span className="text-lg">{icon}</span>
      <span className="font-medium">{label}</span>
    </Link>
  );
};

const ModuleNavItem = ({ id, title, icon, path }) => {
  const isActive = window.location.pathname === path;
  
  return (
    <Link
      to={path}
      className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors text-sm ${
        isActive 
          ? 'bg-blue-50 text-blue-700' 
          : 'text-gray-600 hover:bg-gray-50'
      }`}
    >
      <span>{icon}</span>
      <span className="font-medium truncate">{title}</span>
    </Link>
  );
};

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-500 rounded-xl mx-auto mb-4 flex items-center justify-center animate-pulse">
            <span className="text-white text-2xl font-bold">H</span>
          </div>
          <p className="text-gray-600">Loading Harv v2.0...</p>
          <div className="mt-2">
            <div className="inline-flex space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <Layout>{children}</Layout>;
};

// Role-based Route Component
const RoleRoute = ({ children, allowedRoles }) => {
  const { userRole } = useAuth();

  if (!allowedRoles.includes(userRole)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// Main App Content
const AppContent = () => {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Routes */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/modules/:moduleId" 
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={['student', 'universal']}>
                <ModulePage />
              </RoleRoute>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/chat" 
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={['student', 'universal']}>
                <ChatPage />
              </RoleRoute>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/progress" 
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={['student', 'universal']}>
                <ProgressPage />
              </RoleRoute>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/teacher" 
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={['educator', 'universal']}>
                <TeacherDashboard />
              </RoleRoute>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/admin" 
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={['admin', 'universal']}>
                <AdminDashboard />
              </RoleRoute>
            </ProtectedRoute>
          } 
        />

        {/* Catch all - redirect to dashboard */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
};

// Main App Component
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
