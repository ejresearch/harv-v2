/**
 * Harv v2.0 API Service - Phase 2.5
 * Complete API integration for enhanced memory + OpenAI features
 */

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class HarvAPI {
  constructor() {
    this.baseURL = API_BASE;
    this.token = localStorage.getItem('harv_token');
  }

  // Authentication headers
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  // Enhanced Memory System APIs
  async getMemoryContext(moduleId, currentMessage) {
    const response = await fetch(
      `${this.baseURL}/memory/context/${moduleId}?current_message=${encodeURIComponent(currentMessage)}`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  async getMemoryLayers(moduleId) {
    const response = await fetch(
      `${this.baseURL}/memory/layers/${moduleId}`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  // Enhanced Chat APIs
  async sendChatMessage(moduleId, message, conversationId = null) {
    const response = await fetch(`${this.baseURL}/chat/enhanced`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({
        message,
        module_id: moduleId,
        conversation_id: conversationId
      })
    });
    return response.json();
  }

  // WebSocket Chat Connection
  createWebSocketConnection(moduleId, userId = null) {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = window.location.host.replace(':3000', ':8000'); // Dev adjustment
    const wsUrl = `${wsProtocol}//${wsHost}/api/v1/chat/ws/${moduleId}${userId ? `?user_id=${userId}` : ''}`;
    
    return new WebSocket(wsUrl);
  }

  // Analytics Dashboard APIs
  async getAnalyticsOverview(timeRange = '7d', moduleId = null) {
    const params = new URLSearchParams({ time_range: timeRange });
    if (moduleId) params.append('module_id', moduleId);
    
    const response = await fetch(
      `${this.baseURL}/analytics/overview?${params}`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  async getSocraticEffectiveness(timeRange = '7d') {
    const response = await fetch(
      `${this.baseURL}/analytics/socratic-effectiveness?time_range=${timeRange}`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  async getMemoryPerformance(timeRange = '7d') {
    const response = await fetch(
      `${this.baseURL}/analytics/memory-performance?time_range=${timeRange}`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  async getLearningVelocity(timeRange = '30d', moduleId = null) {
    const params = new URLSearchParams({ time_range: timeRange });
    if (moduleId) params.append('module_id', moduleId);
    
    const response = await fetch(
      `${this.baseURL}/analytics/learning-velocity?${params}`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  // System Status APIs
  async getSystemHealth() {
    const response = await fetch(`${this.baseURL}/health/system`);
    return response.json();
  }

  async getOpenAIStatus() {
    const response = await fetch(
      `${this.baseURL}/chat/openai/status`,
      { headers: this.getHeaders() }
    );
    return response.json();
  }

  // Authentication APIs
  async login(email, password) {
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    if (data.access_token) {
      this.token = data.access_token;
      localStorage.setItem('harv_token', this.token);
    }
    
    return data;
  }

  async register(name, email, password) {
    const response = await fetch(`${this.baseURL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });
    return response.json();
  }

  // Demo APIs
  async runEnhancedChatDemo(moduleId) {
    const response = await fetch(
      `${this.baseURL}/chat/demo/${moduleId}`,
      { 
        method: 'POST',
        headers: this.getHeaders() 
      }
    );
    return response.json();
  }

  async runMemoryDemo(moduleId) {
    const response = await fetch(
      `${this.baseURL}/memory/demo/${moduleId}`,
      { 
        method: 'POST',
        headers: this.getHeaders() 
      }
    );
    return response.json();
  }
}

export const harvAPI = new HarvAPI();
export default HarvAPI;
