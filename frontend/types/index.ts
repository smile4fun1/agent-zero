/**
 * TypeScript type definitions for Agent Zero Enterprise
 */

// Enums
export enum PersonaDomain {
  GENERAL = 'general',
  ROBOTICS = 'robotics',
  FINANCE = 'finance',
  ENGINEERING = 'engineering',
  MARKETING = 'marketing',
  RESEARCH = 'research',
}

export enum MemoryStrategy {
  FULL = 'full',
  SUMMARIZED = 'summarized',
  SELECTIVE = 'selective',
}

export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system',
}

// Persona types
export interface PersonaTraits {
  formality: number;
  verbosity: number;
  creativity: number;
  empathy: number;
  humor: number;
}

export interface PersonaBehavior {
  greeting: string;
  style: string;
  constraints: string[];
  preferences: string[];
}

export interface PersonaConfig {
  temperature: number;
  max_tokens: number;
  tools_enabled: string[];
  memory_strategy: MemoryStrategy;
}

export interface Persona {
  id: string;
  name: string;
  role: string;
  expertise: string[];
  avatar?: string;
  traits: PersonaTraits;
  behavior: PersonaBehavior;
  config: PersonaConfig;
  domain: PersonaDomain;
  custom_instructions?: string;
  created_at: string;
  updated_at: string;
  user_id: string;
}

// Agent types
export interface Agent {
  id: string;
  name: string;
  persona_id: string;
  project_id?: string;
  status: string;
  config: Record<string, any>;
  created_at: string;
  updated_at: string;
  user_id: string;
}

// Conversation types
export interface Message {
  role: MessageRole;
  content: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface Conversation {
  id: string;
  agent_id: string;
  title: string;
  messages: Message[];
  context: Record<string, any>;
  created_at: string;
  updated_at: string;
  archived: boolean;
  user_id: string;
}

// Memory types
export interface Memory {
  id: string;
  content: string;
  type: 'fragment' | 'solution' | 'fact';
  metadata: Record<string, any>;
  agent_id?: string;
  relevance_score?: number;
  created_at: string;
  user_id: string;
}

// Analytics types
export interface UsageStats {
  total_messages: number;
  total_tokens: number;
  total_cost: number;
  avg_response_time: number;
  success_rate: number;
}

export interface Analytics {
  period: string;
  usage: UsageStats;
  top_agents: Array<{ name: string; usage: number }>;
  top_tools: Array<{ name: string; usage: number }>;
  cost_breakdown: Record<string, number>;
}

// Auth types
export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  subscription_tier: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// API response types
export interface ApiResponse<T> {
  data: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}
