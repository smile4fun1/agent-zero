/**
 * WebSocket client for real-time communication
 */

import { io, Socket } from 'socket.io-client';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:5000';

type EventCallback = (data: any) => void;

class WebSocketClient {
  private socket: Socket | null = null;
  private connected: boolean = false;
  private eventCallbacks: Map<string, Set<EventCallback>> = new Map();

  connect(token: string): void {
    if (this.connected) return;

    this.socket = io(WS_URL, {
      auth: { token },
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.connected = true;
      this.emit('connection_status', { connected: true });
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      this.connected = false;
      this.emit('connection_status', { connected: false });
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    });

    // Register event listeners
    this.setupEventListeners();
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
    }
  }

  isConnected(): boolean {
    return this.connected;
  }

  private setupEventListeners(): void {
    if (!this.socket) return;

    // Agent events
    this.socket.on('agent_typing', (data) => this.emit('agent_typing', data));
    this.socket.on('agent_response_chunk', (data) => this.emit('agent_response_chunk', data));
    this.socket.on('agent_response_complete', (data) => this.emit('agent_response_complete', data));
    this.socket.on('agent_error', (data) => this.emit('agent_error', data));
    this.socket.on('agent_interrupted', (data) => this.emit('agent_interrupted', data));

    // User events
    this.socket.on('user_typing', (data) => this.emit('user_typing', data));

    // Session events
    this.socket.on('joined_session', (data) => this.emit('joined_session', data));
    this.socket.on('left_session', (data) => this.emit('left_session', data));

    // Ping/pong
    this.socket.on('pong', (data) => this.emit('pong', data));
  }

  // Session management
  joinSession(sessionId: string, token: string): void {
    if (!this.socket) return;
    this.socket.emit('join_session', { session_id: sessionId, token });
  }

  leaveSession(sessionId: string): void {
    if (!this.socket) return;
    this.socket.emit('leave_session', { session_id: sessionId });
  }

  // Send message to agent
  sendMessage(
    sessionId: string,
    agentId: string,
    message: string,
    context?: any,
    token?: string
  ): void {
    if (!this.socket) return;
    this.socket.emit('agent_message', {
      session_id: sessionId,
      agent_id: agentId,
      message,
      context,
      token,
    });
  }

  // Interrupt agent
  interruptAgent(sessionId: string, agentId: string, token?: string): void {
    if (!this.socket) return;
    this.socket.emit('agent_interrupt', {
      session_id: sessionId,
      agent_id: agentId,
      token,
    });
  }

  // Typing indicator
  setTyping(sessionId: string, typing: boolean): void {
    if (!this.socket) return;
    this.socket.emit('typing', {
      session_id: sessionId,
      typing,
    });
  }

  // Ping
  ping(): void {
    if (!this.socket) return;
    this.socket.emit('ping');
  }

  // Event subscription
  on(event: string, callback: EventCallback): () => void {
    if (!this.eventCallbacks.has(event)) {
      this.eventCallbacks.set(event, new Set());
    }
    this.eventCallbacks.get(event)!.add(callback);

    // Return unsubscribe function
    return () => {
      this.eventCallbacks.get(event)?.delete(callback);
    };
  }

  // Emit event to all subscribers
  private emit(event: string, data: any): void {
    const callbacks = this.eventCallbacks.get(event);
    if (callbacks) {
      callbacks.forEach((callback) => callback(data));
    }
  }
}

// Singleton instance
export const ws = new WebSocketClient();
