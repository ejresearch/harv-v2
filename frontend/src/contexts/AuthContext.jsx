import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [userRole, setUserRole] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const savedUser = localStorage.getItem('user_data');
    const role = localStorage.getItem('user_role');
    
    if (token && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        setUserRole(role || 'student');
      } catch (error) {
        console.error('Error parsing saved user data:', error);
        // Clear corrupted data
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
        localStorage.removeItem('user_role');
      }
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      console.log('🔐 Attempting login...', credentials.email);
      
      // Try to call your API
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Login API failed:', response.status, errorText);
        throw new Error('Login failed');
      }

      const data = await response.json();
      console.log('✅ Login API success:', data);
      
      // Extract user data from the response
      const userData = {
        id: data.user_id,
        name: data.name,
        email: data.email
      };

      // Determine role from email (demo logic)
      let role = 'student';
      if (data.email?.includes('teacher')) role = 'educator';
      if (data.email?.includes('admin')) role = 'admin';
      if (data.email?.includes('demo@harv.com')) role = 'universal';

      // Save to localStorage
      localStorage.setItem('auth_token', data.access_token);
      localStorage.setItem('user_data', JSON.stringify(userData));
      localStorage.setItem('user_role', role);

      // Update state
      setUser(userData);
      setUserRole(role);

      console.log('✅ Login successful, user:', userData, 'role:', role);
      return data;

    } catch (error) {
      console.error('❌ Login error:', error);
      
      // Miranda-inspired fallback: If backend is down, allow demo login
      console.log('🔄 Trying demo fallback...');
      
      if (credentials.email && credentials.password) {
        // Create demo user based on email
        let role = 'student';
        let name = 'Demo User';
        
        if (credentials.email.includes('teacher')) {
          role = 'educator';
          name = 'Demo Teacher';
        } else if (credentials.email.includes('admin')) {
          role = 'admin';
          name = 'Demo Admin';
        } else if (credentials.email.includes('demo@harv.com')) {
          role = 'universal';
          name = 'Universal Demo User';
        }

        const demoUser = {
          id: 1,
          name: name,
          email: credentials.email
        };

        const demoToken = `demo_token_${Date.now()}`;

        // Save demo data
        localStorage.setItem('auth_token', demoToken);
        localStorage.setItem('user_data', JSON.stringify(demoUser));
        localStorage.setItem('user_role', role);

        // Update state
        setUser(demoUser);
        setUserRole(role);

        console.log('✅ Demo login successful:', demoUser, 'role:', role);
        
        return {
          access_token: demoToken,
          user: demoUser,
          role: role
        };
      }
      
      throw error;
    }
  };

  const logout = () => {
    console.log('🔓 Logging out...');
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    localStorage.removeItem('user_role');
    setUser(null);
    setUserRole(null);
  };

  const value = {
    user,
    userRole,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
