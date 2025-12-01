/**
 * API client for Agent Zero backend
 */

import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v2`,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Try to refresh token
          const refreshed = await this.refreshToken();
          if (refreshed) {
            // Retry the original request
            return this.client(error.config);
          } else {
            // Redirect to login
            this.clearTokens();
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Token management
  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  private getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('refresh_token');
  }

  private setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  private clearTokens(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  private async refreshToken(): Promise<boolean> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) return false;

    try {
      const response = await axios.post(`${API_URL}/api/v2/auth/refresh`, {}, {
        headers: { Authorization: `Bearer ${refreshToken}` }
      });
      
      const { access_token } = response.data;
      this.setTokens(access_token, refreshToken);
      return true;
    } catch (error) {
      return false;
    }
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', { email, password });
    const { tokens, user } = response.data;
    this.setTokens(tokens.access_token, tokens.refresh_token);
    return { user, tokens };
  }

  async register(email: string, password: string, name: string) {
    const response = await this.client.post('/auth/register', { email, password, name });
    const { tokens, user } = response.data;
    this.setTokens(tokens.access_token, tokens.refresh_token);
    return { user, tokens };
  }

  async logout() {
    this.clearTokens();
  }

  // Persona endpoints
  async listPersonas(params?: { domain?: string; limit?: number; offset?: number }) {
    const response = await this.client.get('/personas', { params });
    return response.data;
  }

  async getPersona(id: string) {
    const response = await this.client.get(`/personas/${id}`);
    return response.data;
  }

  async createPersona(data: any) {
    const response = await this.client.post('/personas', data);
    return response.data;
  }

  async updatePersona(id: string, data: any) {
    const response = await this.client.put(`/personas/${id}`, data);
    return response.data;
  }

  async deletePersona(id: string) {
    await this.client.delete(`/personas/${id}`);
  }

  // Agent endpoints
  async listAgents(params?: { status?: string; persona_id?: string; limit?: number; offset?: number }) {
    const response = await this.client.get('/agents', { params });
    return response.data;
  }

  async getAgent(id: string) {
    const response = await this.client.get(`/agents/${id}`);
    return response.data;
  }

  async createAgent(data: any) {
    const response = await this.client.post('/agents', data);
    return response.data;
  }

  async updateAgent(id: string, data: any) {
    const response = await this.client.put(`/agents/${id}`, data);
    return response.data;
  }

  async deleteAgent(id: string) {
    await this.client.delete(`/agents/${id}`);
  }

  async executeAgent(id: string, data: any) {
    const response = await this.client.post(`/agents/${id}/execute`, data);
    return response.data;
  }

  // Conversation endpoints
  async listConversations(params?: { agent_id?: string; archived?: boolean; limit?: number; offset?: number }) {
    const response = await this.client.get('/conversations', { params });
    return response.data;
  }

  async getConversation(id: string) {
    const response = await this.client.get(`/conversations/${id}`);
    return response.data;
  }

  async createConversation(data: any) {
    const response = await this.client.post('/conversations', data);
    return response.data;
  }

  async updateConversation(id: string, data: any) {
    const response = await this.client.put(`/conversations/${id}`, data);
    return response.data;
  }

  async deleteConversation(id: string) {
    await this.client.delete(`/conversations/${id}`);
  }

  // Memory endpoints
  async searchMemory(query: string, params?: { limit?: number; agent_id?: string; type?: string }) {
    const response = await this.client.post('/memory/search', { query, ...params });
    return response.data;
  }

  async createMemory(data: any) {
    const response = await this.client.put('/memory/search', data);
    return response.data;
  }

  async deleteMemory(id: string) {
    await this.client.delete(`/memory/${id}`);
  }

  // Analytics endpoints
  async getAnalytics(params?: { period?: string; agent_id?: string }) {
    const response = await this.client.get('/analytics', { params });
    return response.data;
  }
}

export const api = new ApiClient();
