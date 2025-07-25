import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Dashboard() {
  const { user, userRole } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
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
        }
      });
      setLoading(false);
    }, 800);
  }, []);

  if (loading) {
    return <DashboardSkeleton />;
  }

  return <StudentDashboardContent data={dashboardData.student} user={user} userRole={userRole} navigate={navigate} />;
}

const StudentDashboardContent = ({ data, user, userRole, navigate }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Welcome Header */}
      <div className="miranda-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h1 className="miranda-title">
              Welcome back, {user?.name}! 👋
            </h1>
            <p className="miranda-subtitle">
              Ready to continue your Mass Communication journey?
            </p>
          </div>
          {userRole === 'universal' && (
            <div style={{
              background: 'linear-gradient(135deg, #8b5cf6, #ec4899)',
              color: 'white',
              padding: '0.5rem 1rem',
              borderRadius: '20px',
              fontSize: '0.85rem',
              fontWeight: '600'
            }}>
              🔄 Universal Access
            </div>
          )}
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '1.5rem'
      }}>
        <div 
          className="miranda-stat-card"
          onClick={() => navigate('/progress')}
        >
          <div className="miranda-stat-value">{data.overallProgress}%</div>
          <div className="miranda-stat-label">Overall Progress</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            {data.completedModules}/{data.totalModules} modules
          </div>
        </div>

        <div 
          className="miranda-stat-card"
          onClick={() => navigate('/chat')}
        >
          <div className="miranda-stat-value">{data.chatSessions}</div>
          <div className="miranda-stat-label">Chat Sessions</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            with AI tutor
          </div>
        </div>

        <div className="miranda-stat-card">
          <div className="miranda-stat-value">{data.insightsGained}</div>
          <div className="miranda-stat-label">Insights Gained</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            learning moments
          </div>
        </div>

        <div 
          className="miranda-stat-card"
          onClick={() => navigate(`/modules/${data.currentModule.id}`)}
        >
          <div className="miranda-stat-value">{data.currentModule.progress}%</div>
          <div className="miranda-stat-label">Current Module</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            {data.currentModule.title}
          </div>
        </div>
      </div>

      {/* Current Module Progress */}
      <div className="miranda-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1e293b' }}>
            Continue Learning
          </h2>
          <button
            onClick={() => navigate(`/modules/${data.currentModule.id}`)}
            className="miranda-button secondary"
          >
            View Module →
          </button>
        </div>
        
        <div style={{
          background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.05))',
          borderRadius: '16px',
          padding: '1.5rem',
          border: '1px solid rgba(59, 130, 246, 0.1)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
              width: '60px',
              height: '60px',
              background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
              borderRadius: '16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem'
            }}>
              📡
            </div>
            <div style={{ flex: 1 }}>
              <h3 style={{ fontSize: '1.2rem', fontWeight: '600', color: '#1e293b', marginBottom: '0.5rem' }}>
                {data.currentModule.title}
              </h3>
              <p style={{ color: '#64748b', marginBottom: '1rem', fontSize: '0.95rem' }}>
                Understanding how communication systems work
              </p>
              <div className="miranda-progress-bar">
                <div 
                  className="miranda-progress-fill"
                  style={{ width: `${data.currentModule.progress}%` }}
                ></div>
              </div>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.5rem' }}>
                {data.currentModule.progress}% complete
              </p>
            </div>
            <button
              onClick={() => navigate(`/modules/${data.currentModule.id}`)}
              className="miranda-button"
            >
              Continue
            </button>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1.5rem'
      }}>
        <QuickActionCard
          title="Chat with AI Tutor"
          description="Ask questions about communication theory and get Socratic guidance"
          icon="🤖"
          action={() => navigate('/chat')}
          gradient="linear-gradient(135deg, #10b981, #059669)"
        />
        <QuickActionCard
          title="View All Modules"
          description="Browse through all 15 Mass Communication modules"
          icon="📚"
          action={() => navigate('/modules/1')}
          gradient="linear-gradient(135deg, #8b5cf6, #ec4899)"
        />
      </div>

      {/* Recent Activity */}
      <div className="miranda-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1e293b' }}>
            Recent Activity
          </h2>
          <button
            onClick={() => navigate('/progress')}
            className="miranda-button secondary"
          >
            View Full Progress →
          </button>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {data.recentActivity.map((activity, index) => (
            <ActivityItem key={index} {...activity} />
          ))}
        </div>
      </div>
    </div>
  );
};

const QuickActionCard = ({ title, description, icon, action, gradient }) => {
  return (
    <div
      onClick={action}
      style={{
        background: gradient,
        borderRadius: '16px',
        padding: '1.5rem',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        display: 'flex',
        alignItems: 'center',
        gap: '1rem'
      }}
      onMouseEnter={(e) => {
        e.target.style.transform = 'translateY(-4px)';
        e.target.style.boxShadow = '0 12px 32px rgba(0, 0, 0, 0.2)';
      }}
      onMouseLeave={(e) => {
        e.target.style.transform = 'translateY(0)';
        e.target.style.boxShadow = 'none';
      }}
    >
      <span style={{ fontSize: '2rem' }}>{icon}</span>
      <div>
        <h3 style={{ fontSize: '1.2rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          {title}
        </h3>
        <p style={{ opacity: 0.9, fontSize: '0.9rem' }}>
          {description}
        </p>
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
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '1rem',
      padding: '1rem',
      background: 'rgba(248, 250, 252, 0.8)',
      borderRadius: '12px',
      border: '1px solid rgba(226, 232, 240, 0.8)'
    }}>
      <div style={{
        width: '40px',
        height: '40px',
        borderRadius: '10px',
        background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1))',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '1.2rem'
      }}>
        {icons[type] || '📝'}
      </div>
      <div style={{ flex: 1 }}>
        <p style={{ fontWeight: '500', color: '#1e293b', marginBottom: '0.25rem' }}>
          {description}
        </p>
        <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
          {time}
        </p>
      </div>
    </div>
  );
};

const DashboardSkeleton = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {[1, 2, 3].map(i => (
        <div key={i} className="miranda-card" style={{ opacity: 0.6 }}>
          <div style={{
            height: '120px',
            background: 'linear-gradient(90deg, rgba(226, 232, 240, 0.8) 25%, rgba(255, 255, 255, 0.8) 50%, rgba(226, 232, 240, 0.8) 75%)',
            borderRadius: '12px',
            backgroundSize: '200% 100%',
            animation: 'shimmer 2s infinite'
          }}></div>
        </div>
      ))}
    </div>
  );
};

// Add shimmer animation
const shimmerStyle = document.createElement('style');
shimmerStyle.textContent = `
  @keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
  }
`;
document.head.appendChild(shimmerStyle);
