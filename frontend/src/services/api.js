class HarvCourseAPI {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    this.token = localStorage.getItem('auth_token');
  }

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...(this.token && { Authorization: `Bearer ${this.token}` }),
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // ========================================================================
  // AUTHENTICATION
  // ========================================================================
  async login(credentials) {
    try {
      const response = await this.request('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials)
      });
      
      // Update token for future requests
      this.token = response.access_token;
      localStorage.setItem('auth_token', response.access_token);
      
      return response;
    } catch (error) {
      // Demo fallback for development
      if (credentials.email === 'student@harv.com' && credentials.password === 'student123') {
        const mockResponse = {
          access_token: 'demo_token_student',
          token_type: 'bearer',
          user: {
            id: 1,
            name: 'Demo Student',
            email: 'student@harv.com',
            role: 'student'
          },
          role: 'student'
        };
        this.token = mockResponse.access_token;
        localStorage.setItem('auth_token', mockResponse.access_token);
        return mockResponse;
      }
      throw error;
    }
  }

  async getCurrentUser() {
    try {
      return await this.request('/api/v1/auth/me');
    } catch (error) {
      // Demo fallback
      return {
        id: 1,
        name: 'Demo Student',
        email: 'student@harv.com',
        role: 'student',
        is_active: true
      };
    }
  }

  async logout() {
    this.token = null;
    localStorage.removeItem('auth_token');
    return { success: true };
  }

  // ========================================================================
  // COURSE MODULES (15 Mass Communication Topics)
  // ========================================================================
  async getModules() {
    try {
      return await this.request('/api/v1/modules/');
    } catch (error) {
      console.warn('API unavailable, using demo data');
      return this.getDemoModules();
    }
  }

  async getModule(moduleId) {
    try {
      return await this.request(`/api/v1/modules/${moduleId}`);
    } catch (error) {
      console.warn('API unavailable, using demo data');
      return this.getDemoModule(moduleId);
    }
  }

  // ========================================================================
  // USER PROGRESS & ANALYTICS
  // ========================================================================
  async getUserProgress(userId, moduleId) {
    try {
      return await this.request(`/api/v1/progress/user/${userId}/module/${moduleId}`);
    } catch (error) {
      console.warn('API unavailable, using demo data');
      return this.getDemoModuleProgress(moduleId);
    }
  }

  async getUserOverview(userId) {
    try {
      return await this.request(`/api/v1/progress/user/${userId}/overview`);
    } catch (error) {
      console.warn('API unavailable, using demo data');
      return this.getDemoUserOverview();
    }
  }

  // ========================================================================
  // AI CHAT & SOCRATIC TUTORING
  // ========================================================================
  async sendChatMessage(messageData) {
    try {
      return await this.request('/api/v1/chat/enhanced', {
        method: 'POST',
        body: JSON.stringify(messageData)
      });
    } catch (error) {
      console.warn('API unavailable, using demo response');
      return this.getDemoChat(messageData);
    }
  }

  // ========================================================================
  // ENHANCED MEMORY SYSTEM
  // ========================================================================
  async getEnhancedMemory(moduleId, currentMessage = '') {
    try {
      const params = new URLSearchParams({
        ...(currentMessage && { current_message: currentMessage })
      });
      return await this.request(`/api/v1/memory/enhanced/${moduleId}?${params}`);
    } catch (error) {
      console.warn('API unavailable, using demo memory');
      return this.getDemoMemory(moduleId);
    }
  }

  // ========================================================================
  // DEMO DATA FOR DEVELOPMENT
  // ========================================================================
  getDemoModules() {
    return [
      { id: 1, title: 'Your Four Worlds', icon: '🌍', description: 'Understanding communication models and personal perception', completion_percentage: 100 },
      { id: 2, title: 'Media Uses & Effects', icon: '📺', description: 'How media functions in society and personal lives', completion_percentage: 75 },
      { id: 3, title: 'Shared Characteristics', icon: '🔗', description: 'Common elements across all media types', completion_percentage: 30 },
      { id: 4, title: 'Communication Infrastructure', icon: '📡', description: 'From telegraph to internet evolution', completion_percentage: 0 },
      { id: 5, title: 'Books', icon: '📚', description: 'The birth of mass communication', completion_percentage: 0 },
      { id: 6, title: 'Newspapers', icon: '📰', description: 'News values and gatekeeping principles', completion_percentage: 0 },
      { id: 7, title: 'Magazines', icon: '📖', description: 'Special interest targeting and niche markets', completion_percentage: 0 },
      { id: 8, title: 'Comic Books', icon: '💭', description: 'Visual storytelling and cultural impact', completion_percentage: 0 },
      { id: 9, title: 'Photography', icon: '📷', description: 'Fixing shadows and capturing reality', completion_percentage: 0 },
      { id: 10, title: 'Recordings', icon: '🎵', description: 'From Bach to rap - cultural mirror', completion_percentage: 0 },
      { id: 11, title: 'Motion Pictures', icon: '🎬', description: 'Mass entertainment revolution begins', completion_percentage: 0 },
      { id: 12, title: 'Radio', icon: '📻', description: 'The household utility that changed everything', completion_percentage: 0 },
      { id: 13, title: 'Television', icon: '📺', description: 'Center of attention - the dominant medium', completion_percentage: 0 },
      { id: 14, title: 'Video Games', icon: '🎮', description: 'The newest and most interactive mass medium', completion_percentage: 0 },
      { id: 15, title: 'Economic Influencers', icon: '💰', description: 'Advertising and media ownership impact', completion_percentage: 0 }
    ];
  }

  getDemoModule(moduleId) {
    const modules = this.getDemoModules();
    const module = modules.find(m => m.id === parseInt(moduleId));
    
    if (!module) return null;

    return {
      ...module,
      learning_objectives: [
        `Understand key concepts in ${module.title}`,
        `Analyze the impact of ${module.title} on society`,
        `Apply critical thinking to ${module.title} examples`,
        `Connect ${module.title} to personal experience`
      ],
      key_concepts: [
        `Historical development of ${module.title}`,
        `Technical aspects and limitations`,
        `Social and cultural influence`,
        `Economic factors and business models`,
        `Future trends and evolution`
      ],
      estimated_time: '45-60 minutes',
      prerequisites: moduleId > 1 ? [`Module ${moduleId - 1}`] : ['None'],
      content_sections: [
        { title: 'Introduction', type: 'text', duration: 10 },
        { title: 'Core Concepts', type: 'interactive', duration: 20 },
        { title: 'Case Studies', type: 'discussion', duration: 15 },
        { title: 'Practical Application', type: 'exercise', duration: 15 }
      ]
    };
  }

  getDemoUserOverview() {
    return {
      user_id: 1,
      course_progress: 35, // Overall percentage
      modules_completed: 2,
      total_modules: 15,
      current_streak: 5,
      total_study_time: 187, // minutes
      last_activity: new Date().toISOString(),
      module_progress: {
        1: { completion_percentage: 100, last_accessed: new Date(Date.now() - 86400000).toISOString() },
        2: { completion_percentage: 75, last_accessed: new Date(Date.now() - 43200000).toISOString() },
        3: { completion_percentage: 30, last_accessed: new Date().toISOString() }
      },
      recent_activity: [
        {
          id: 1,
          type: 'module_progress',
          title: 'Continued Module 3: Shared Characteristics',
          description: 'Made progress on understanding common media elements',
          timestamp: new Date(Date.now() - 1800000).toISOString(),
          icon: '🔗'
        },
        {
          id: 2,
          type: 'ai_chat',
          title: 'AI Tutor Session',
          description: 'Discussed the differences between books and digital media',
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          icon: '💬'
        },
        {
          id: 3,
          type: 'module_complete',
          title: 'Completed Module 2: Media Uses & Effects',
          description: 'Successfully finished all learning objectives',
          timestamp: new Date(Date.now() - 86400000).toISOString(),
          icon: '✅'
        }
      ],
      achievements: [
        { id: 1, title: 'First Steps', description: 'Completed your first module', earned_date: new Date(Date.now() - 172800000).toISOString() },
        { id: 2, title: 'Quick Learner', description: 'Completed 2 modules in one week', earned_date: new Date(Date.now() - 86400000).toISOString() }
      ],
      learning_insights: {
        preferred_time: 'afternoon',
        average_session_length: 23,
        strongest_areas: ['Books', 'Media Theory'],
        areas_for_improvement: ['Technical Infrastructure', 'Economics']
      }
    };
  }

  getDemoModuleProgress(moduleId) {
    const progressMap = {
      1: 100,
      2: 75,
      3: 30,
      4: 0
    };
    
    return {
      module_id: parseInt(moduleId),
      completion_percentage: progressMap[moduleId] || 0,
      last_accessed: new Date().toISOString(),
      time_spent: Math.floor(Math.random() * 60) + 15,
      sections_completed: Math.floor((progressMap[moduleId] || 0) / 25),
      quiz_scores: progressMap[moduleId] > 50 ? [85, 92, 78] : [],
      notes_count: Math.floor(Math.random() * 5),
      next_section: progressMap[moduleId] < 100 ? 'Core Concepts' : null
    };
  }

  getDemoChat(messageData) {
    return {
      response: "That's a fascinating question about mass communication! Instead of giving you the answer directly, let me ask you this: What do you think are the key differences between how books and television deliver their messages to audiences? Consider the pace, interactivity, and how much control the audience has over the experience.",
      conversation_id: 'demo_conversation_' + Date.now(),
      memory_context: {
        recent_topics: ['books', 'television', 'audience control'],
        learning_progress: 'Module 3 - exploring media characteristics',
        socratic_approach: 'encouraging comparison and analysis'
      },
      suggested_followups: [
        "What role does the audience play in each medium?",
        "How does timing affect message delivery?",
        "Can you think of examples where these differences matter?"
      ]
    };
  }

  getDemoMemory(moduleId) {
    return {
      module_id: parseInt(moduleId),
      memory_layers: {
        immediate: {
          recent_concepts: ['mass communication', 'media effects', 'audience'],
          current_focus: 'Understanding how different media types work'
        },
        short_term: {
          session_progress: 'Exploring characteristics of traditional vs digital media',
          key_questions: ['What makes media "mass"?', 'How do audiences interact with different media?']
        },
        long_term: {
          mastered_concepts: ['Basic communication models', 'Historical development of mass media'],
          learning_patterns: 'Student prefers concrete examples over abstract theory'
        },
        contextual: {
          related_modules: [1, 2, 4],
          real_world_connections: ['Social media usage', 'News consumption habits'],
          personal_relevance: 'Student is interested in digital media careers'
        }
      },
      confidence_scores: {
        'communication models': 0.85,
        'media history': 0.72,
        'audience analysis': 0.45,
        'technical aspects': 0.23
      }
    };
  }

  // ========================================================================
  // TEACHER/ADMIN TOOLS (Phase 3)
  // ========================================================================
  async updateModuleContent(moduleId, content) {
    try {
      return await this.request(`/api/v1/modules/${moduleId}/content`, {
        method: 'PUT',
        body: JSON.stringify(content)
      });
    } catch (error) {
      console.warn('API unavailable, simulating update');
      return { success: true, message: 'Content updated (demo mode)' };
    }
  }

  async getAdminDashboard() {
    try {
      return await this.request('/api/v1/admin/analytics/dashboard');
    } catch (error) {
      console.warn('API unavailable, using demo admin data');
      return {
        total_students: 127,
        active_students: 89,
        completion_rate: 73,
        average_progress: 45,
        popular_modules: [1, 2, 5, 11, 13],
        recent_activity: []
      };
    }
  }

  async switchRole(targetRole) {
    try {
      return await this.request('/api/v1/demo/switch-role', {
        method: 'POST',
        body: JSON.stringify({ target_role: targetRole })
      });
    } catch (error) {
      console.warn('API unavailable, simulating role switch');
      return { 
        success: true, 
        new_role: targetRole,
        message: `Switched to ${targetRole} role (demo mode)` 
      };
    }
  }
}

export const api = new HarvCourseAPI();
