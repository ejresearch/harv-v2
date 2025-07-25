import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginPage } from './components/auth/LoginPage';

// Import your page components
import Dashboard from './pages/Dashboard';
import ModulePage from './pages/ModulePage';
import ChatPage from './pages/ChatPage';
import ProgressPage from './pages/ProgressPage';
import TeacherDashboard from './pages/TeacherDashboard';
import AdminDashboard from './pages/AdminDashboard';

// Modern Layout with Miranda-style design
const Layout = ({ children }) => {
  const { user, userRole, logout } = useAuth();
  const location = useLocation();

  const navigationItems = {
    student: [
      { icon: '🏠', label: 'Dashboard', path: '/dashboard' },
      { icon: '💬', label: 'AI Tutor', path: '/chat' },
      { icon: '📊', label: 'Progress', path: '/progress' }
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
      { icon: '⚙️', label: 'Settings', path: '/settings' }
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
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      {/* Miranda-style Header */}
      <header style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
        padding: '1rem 2rem',
        position: 'sticky',
        top: 0,
        zIndex: 1000,
        boxShadow: '0 1px 20px rgba(0, 0, 0, 0.1)'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          maxWidth: '1400px',
          margin: '0 auto'
        }}>
          {/* Logo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 'bold',
              fontSize: '1.2rem'
            }}>
              H
            </div>
            <div>
              <h1 style={{ 
                margin: 0, 
                fontSize: '1.5rem', 
                fontWeight: '700',
                background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                Harv v2.0
              </h1>
              <p style={{ 
                margin: 0, 
                fontSize: '0.85rem', 
                color: '#64748b',
                textTransform: 'capitalize'
              }}>
                {userRole} Portal
              </p>
            </div>
          </div>

          {/* User Info */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ 
                fontSize: '0.9rem', 
                fontWeight: '600', 
                color: '#1e293b'
              }}>
                {user?.name}
              </div>
              <div style={{ 
                fontSize: '0.75rem', 
                color: '#64748b'
              }}>
                {user?.email}
              </div>
            </div>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #f1f5f9, #e2e8f0)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.2rem'
            }}>
              {userRole === 'student' ? '🎓' : userRole === 'educator' ? '🧑‍🏫' : userRole === 'universal' ? '🔄' : '⚙️'}
            </div>
            <button
              onClick={logout}
              style={{
                background: 'none',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '8px',
                cursor: 'pointer',
                color: '#64748b',
                fontSize: '0.85rem',
                transition: 'all 0.2s',
                fontWeight: '500'
              }}
              onMouseEnter={(e) => {
                e.target.style.background = '#f1f5f9';
                e.target.style.color = '#1e293b';
              }}
              onMouseLeave={(e) => {
                e.target.style.background = 'none';
                e.target.style.color = '#64748b';
              }}
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Container */}
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '2rem',
        display: 'flex',
        gap: '2rem',
        minHeight: 'calc(100vh - 100px)'
      }}>
        
        {/* Miranda-style Sidebar */}
        <aside style={{
          width: '280px',
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          borderRadius: '20px',
          padding: '1.5rem',
          height: 'fit-content',
          position: 'sticky',
          top: '120px',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          {/* Navigation Tabs */}
          <nav style={{ marginBottom: '2rem' }}>
            <h3 style={{
              fontSize: '0.75rem',
              fontWeight: '600',
              color: '#64748b',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              marginBottom: '1rem',
              margin: '0 0 1rem 0'
            }}>
              Navigation
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {currentNavigation.map((item) => (
                <NavTab key={item.path} {...item} location={location} />
              ))}
            </div>
          </nav>

          {/* Course Modules (for students and universal) */}
          {(userRole === 'student' || userRole === 'universal') && (
            <div>
              <h3 style={{
                fontSize: '0.75rem',
                fontWeight: '600',
                color: '#64748b',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                marginBottom: '1rem',
                margin: '0 0 1rem 0'
              }}>
                Course Modules
              </h3>
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '2px',
                maxHeight: '400px',
                overflowY: 'auto',
                scrollbarWidth: 'thin'
              }}>
                {courseModules.map((module) => (
                  <ModuleTab key={module.id} {...module} location={location} />
                ))}
              </div>
            </div>
          )}
        </aside>

        {/* Main Content Area */}
        <main style={{
          flex: 1,
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          borderRadius: '20px',
          padding: '2rem',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          minHeight: '600px'
        }}>
          {children}
        </main>
      </div>
    </div>
  );
};

// Miranda-style Navigation Tab
const NavTab = ({ icon, label, path, location }) => {
  const isActive = location.pathname === path;
  
  return (
    <Link
      to={path}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '12px 16px',
        borderRadius: '12px',
        textDecoration: 'none',
        fontSize: '0.9rem',
        fontWeight: '500',
        transition: 'all 0.2s',
        background: isActive ? 'linear-gradient(135deg, #3b82f6, #8b5cf6)' : 'transparent',
        color: isActive ? 'white' : '#64748b',
        transform: isActive ? 'translateY(-1px)' : 'none',
        boxShadow: isActive ? '0 4px 12px rgba(59, 130, 246, 0.3)' : 'none'
      }}
      onMouseEnter={(e) => {
        if (!isActive) {
          e.target.style.background = '#f8fafc';
          e.target.style.color = '#1e293b';
          e.target.style.transform = 'translateY(-1px)';
        }
      }}
      onMouseLeave={(e) => {
        if (!isActive) {
          e.target.style.background = 'transparent';
          e.target.style.color = '#64748b';
          e.target.style.transform = 'none';
        }
      }}
    >
      <span style={{ fontSize: '1.1rem' }}>{icon}</span>
      <span>{label}</span>
    </Link>
  );
};

// Miranda-style Module Tab
const ModuleTab = ({ id, title, icon, path, location }) => {
  const isActive = location.pathname === path;
  
  return (
    <Link
      to={path}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        padding: '8px 12px',
        borderRadius: '8px',
        textDecoration: 'none',
        fontSize: '0.85rem',
        fontWeight: '500',
        transition: 'all 0.2s',
        background: isActive ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
        color: isActive ? '#3b82f6' : '#64748b',
        border: isActive ? '1px solid rgba(59, 130, 246, 0.2)' : '1px solid transparent'
      }}
      onMouseEnter={(e) => {
        if (!isActive) {
          e.target.style.background = '#f8fafc';
          e.target.style.color = '#1e293b';
        }
      }}
      onMouseLeave={(e) => {
        if (!isActive) {
          e.target.style.background = 'transparent';
          e.target.style.color = '#64748b';
        }
      }}
    >
      <span style={{ fontSize: '0.9rem' }}>{icon}</span>
      <span style={{ 
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap'
      }}>
        {title}
      </span>
    </Link>
  );
};

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          borderRadius: '20px',
          padding: '3rem',
          textAlign: 'center',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{
            width: '60px',
            height: '60px',
            background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
            borderRadius: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1.5rem',
            animation: 'pulse 2s infinite'
          }}>
            <span style={{ color: 'white', fontSize: '1.5rem', fontWeight: 'bold' }}>H</span>
          </div>
          <p style={{ 
            color: '#64748b', 
            fontSize: '1.1rem',
            margin: 0
          }}>
            Loading Harv v2.0...
          </p>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '4px',
            marginTop: '1rem'
          }}>
            {[0, 1, 2].map(i => (
              <div
                key={i}
                style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#3b82f6',
                  animation: `bounce 1.4s ease-in-out ${i * 0.16}s infinite both`
                }}
              />
            ))}
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

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  
  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
  
  /* Custom scrollbar */
  ::-webkit-scrollbar {
    width: 6px;
  }
  
  ::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
  }
  
  ::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }
`;
document.head.appendChild(style);

// Main App Component
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
