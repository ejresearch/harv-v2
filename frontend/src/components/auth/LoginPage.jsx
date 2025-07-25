import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';

export const LoginPage = () => {
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(credentials);
    } catch (error) {
      setError('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoClick = (email, password) => {
    setCredentials({ email, password });
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      {/* Split Layout for Desktop */}
      <div style={{ 
        display: 'flex',
        background: 'white',
        borderRadius: '20px',
        boxShadow: '0 25px 50px rgba(0,0,0,0.15)',
        overflow: 'hidden',
        maxWidth: '1200px',
        width: '100%',
        minHeight: '700px'
      }}>
        
        {/* Left Side - Branding */}
        <div style={{ 
          flex: '1',
          background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
          padding: '4rem',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          color: 'white',
          textAlign: 'center'
        }}>
          <div style={{ 
            width: '120px',
            height: '120px',
            background: 'rgba(255,255,255,0.2)',
            borderRadius: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '2rem',
            backdropFilter: 'blur(10px)'
          }}>
            <span style={{ fontSize: '3rem', fontWeight: 'bold' }}>H</span>
          </div>
          <h1 style={{ fontSize: '3.5rem', fontWeight: 'bold', margin: '0 0 1rem', letterSpacing: '-0.02em' }}>
            Harv v2.0
          </h1>
          <p style={{ fontSize: '1.25rem', margin: '0 0 3rem', opacity: 0.9, lineHeight: 1.6 }}>
            Introduction to Mass Communication
          </p>
          <div style={{ fontSize: '1rem', opacity: 0.8, lineHeight: 1.6 }}>
            <p style={{ margin: '0 0 1rem' }}>🎓 15 comprehensive modules</p>
            <p style={{ margin: '0 0 1rem' }}>🤖 Socratic AI methodology</p>
            <p style={{ margin: '0' }}>📊 Advanced learning analytics</p>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div style={{ 
          flex: '1',
          padding: '4rem',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center'
        }}>
          <div style={{ maxWidth: '400px', width: '100%', margin: '0 auto' }}>
            
            <div style={{ marginBottom: '3rem', textAlign: 'center' }}>
              <h2 style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1f2937', margin: '0 0 0.5rem' }}>
                Welcome Back
              </h2>
              <p style={{ color: '#6b7280', margin: 0, fontSize: '1.1rem' }}>
                Sign in to continue your learning journey
              </p>
            </div>

            {/* Login Form */}
            <form onSubmit={handleLogin} style={{ marginBottom: '2rem' }}>
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ 
                  display: 'block', 
                  fontSize: '1rem', 
                  fontWeight: '600', 
                  color: '#374151', 
                  marginBottom: '0.75rem' 
                }}>
                  Email Address
                </label>
                <input
                  type="email"
                  value={credentials.email}
                  onChange={(e) => setCredentials({...credentials, email: e.target.value})}
                  style={{ 
                    width: '100%',
                    padding: '1rem 1.25rem',
                    border: '2px solid #e5e7eb',
                    borderRadius: '12px',
                    fontSize: '1.1rem',
                    transition: 'border-color 0.2s',
                    outline: 'none'
                  }}
                  placeholder="Enter your email address"
                  required
                  onFocus={(e) => e.target.style.borderColor = '#3b82f6'}
                  onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                />
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ 
                  display: 'block', 
                  fontSize: '1rem', 
                  fontWeight: '600', 
                  color: '#374151', 
                  marginBottom: '0.75rem' 
                }}>
                  Password
                </label>
                <input
                  type="password"
                  value={credentials.password}
                  onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                  style={{ 
                    width: '100%',
                    padding: '1rem 1.25rem',
                    border: '2px solid #e5e7eb',
                    borderRadius: '12px',
                    fontSize: '1.1rem',
                    transition: 'border-color 0.2s',
                    outline: 'none'
                  }}
                  placeholder="Enter your password"
                  required
                  onFocus={(e) => e.target.style.borderColor = '#3b82f6'}
                  onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                />
              </div>

              {error && (
                <div style={{ 
                  background: '#fef2f2',
                  border: '2px solid #fecaca',
                  color: '#dc2626',
                  padding: '1rem',
                  borderRadius: '12px',
                  marginBottom: '1.5rem',
                  fontSize: '1rem'
                }}>
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                style={{ 
                  width: '100%',
                  background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
                  color: 'white',
                  padding: '1rem 1.25rem',
                  borderRadius: '12px',
                  fontWeight: '600',
                  border: 'none',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.7 : 1,
                  fontSize: '1.1rem',
                  transition: 'transform 0.2s, opacity 0.2s',
                  transform: loading ? 'scale(1)' : 'scale(1)',
                }}
                onMouseEnter={(e) => !loading && (e.target.style.transform = 'translateY(-1px)')}
                onMouseLeave={(e) => !loading && (e.target.style.transform = 'translateY(0)')}
              >
                {loading ? 'Signing in...' : 'Sign In'}
              </button>
            </form>

            {/* Demo Accounts */}
            <div style={{ paddingTop: '2rem', borderTop: '1px solid #e5e7eb' }}>
              <p style={{ 
                fontSize: '1rem', 
                color: '#6b7280', 
                textAlign: 'center', 
                marginBottom: '1.5rem',
                fontWeight: '500'
              }}>
                Demo Accounts - Click to auto-fill:
              </p>
              
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: '1fr 1fr', 
                gap: '1rem',
                marginBottom: '1rem'
              }}>
                <button
                  type="button"
                  onClick={() => handleDemoClick('student@demo.com', 'student123')}
                  style={{ 
                    padding: '1rem',
                    background: '#f8fafc',
                    border: '2px solid #e2e8f0',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    textAlign: 'center',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = '#f1f5f9';
                    e.target.style.borderColor = '#cbd5e1';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = '#f8fafc';
                    e.target.style.borderColor = '#e2e8f0';
                  }}
                >
                  <div style={{ fontWeight: '600', color: '#1e293b', marginBottom: '0.25rem' }}>
                    🎓 Student
                  </div>
                  <div style={{ color: '#64748b', fontSize: '0.9rem' }}>
                    student@demo.com
                  </div>
                </button>
                
                <button
                  type="button"
                  onClick={() => handleDemoClick('teacher@demo.com', 'teacher123')}
                  style={{ 
                    padding: '1rem',
                    background: '#f8fafc',
                    border: '2px solid #e2e8f0',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    textAlign: 'center',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = '#f1f5f9';
                    e.target.style.borderColor = '#cbd5e1';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = '#f8fafc';
                    e.target.style.borderColor = '#e2e8f0';
                  }}
                >
                  <div style={{ fontWeight: '600', color: '#1e293b', marginBottom: '0.25rem' }}>
                    👨‍🏫 Teacher
                  </div>
                  <div style={{ color: '#64748b', fontSize: '0.9rem' }}>
                    teacher@demo.com
                  </div>
                </button>
              </div>
              
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: '1fr 1fr', 
                gap: '1rem'
              }}>
                <button
                  type="button"
                  onClick={() => handleDemoClick('admin@demo.com', 'admin123')}
                  style={{ 
                    padding: '1rem',
                    background: '#f8fafc',
                    border: '2px solid #e2e8f0',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    textAlign: 'center',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = '#f1f5f9';
                    e.target.style.borderColor = '#cbd5e1';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = '#f8fafc';
                    e.target.style.borderColor = '#e2e8f0';
                  }}
                >
                  <div style={{ fontWeight: '600', color: '#1e293b', marginBottom: '0.25rem' }}>
                    ⚙️ Admin
                  </div>
                  <div style={{ color: '#64748b', fontSize: '0.9rem' }}>
                    admin@demo.com
                  </div>
                </button>
                
                <button
                  type="button"
                  onClick={() => handleDemoClick('demo@harv.com', 'demo123')}
                  style={{ 
                    padding: '1rem',
                    background: '#f8fafc',
                    border: '2px solid #e2e8f0',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    textAlign: 'center',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = '#f1f5f9';
                    e.target.style.borderColor = '#cbd5e1';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = '#f8fafc';
                    e.target.style.borderColor = '#e2e8f0';
                  }}
                >
                  <div style={{ fontWeight: '600', color: '#1e293b', marginBottom: '0.25rem' }}>
                    🌟 Universal
                  </div>
                  <div style={{ color: '#64748b', fontSize: '0.9rem' }}>
                    demo@harv.com
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
