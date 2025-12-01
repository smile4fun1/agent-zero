"""
WebSocket event handlers for real-time communication
"""

from flask_socketio import emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
from functools import wraps
import json

def authenticated_only(f):
    """Decorator to require authentication for WebSocket events"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        # Get token from query string or handshake
        token = kwargs.get('token')
        if not token:
            emit('error', {'message': 'Authentication required'})
            disconnect()
            return
        
        try:
            # Decode JWT token
            decoded = decode_token(token)
            user_id = decoded['sub']
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)
        except Exception as e:
            emit('error', {'message': 'Invalid token'})
            disconnect()
            return
    
    return wrapped

def register_websocket_events(socketio):
    """Register all WebSocket event handlers"""
    
    @socketio.on('connect')
    def handle_connect(auth):
        """Handle client connection"""
        print(f"Client connected")
        emit('connected', {'status': 'connected'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        print("Client disconnected")
    
    @socketio.on('join_session')
    @authenticated_only
    def handle_join_session(data, user_id=None):
        """
        Join a session room for receiving updates
        
        Data:
            - session_id: Session/conversation ID to join
        """
        session_id = data.get('session_id')
        if not session_id:
            emit('error', {'message': 'session_id required'})
            return
        
        # TODO: Verify user has access to this session
        
        join_room(session_id)
        emit('joined_session', {
            'session_id': session_id,
            'message': 'Successfully joined session'
        })
    
    @socketio.on('leave_session')
    def handle_leave_session(data):
        """
        Leave a session room
        
        Data:
            - session_id: Session ID to leave
        """
        session_id = data.get('session_id')
        if not session_id:
            emit('error', {'message': 'session_id required'})
            return
        
        leave_room(session_id)
        emit('left_session', {
            'session_id': session_id,
            'message': 'Successfully left session'
        })
    
    @socketio.on('agent_message')
    @authenticated_only
    def handle_agent_message(data, user_id=None):
        """
        Send message to agent
        
        Data:
            - session_id: Session ID
            - agent_id: Agent ID
            - message: Message content
            - context: Optional context
        """
        from .services.agent_service import AgentService
        
        session_id = data.get('session_id')
        agent_id = data.get('agent_id')
        message = data.get('message')
        context = data.get('context', {})
        
        if not all([session_id, agent_id, message]):
            emit('error', {'message': 'session_id, agent_id, and message required'})
            return
        
        # Join session room if not already joined
        join_room(session_id)
        
        # Emit typing indicator
        emit('agent_typing', {
            'session_id': session_id,
            'agent_id': agent_id,
            'typing': True
        }, room=session_id)
        
        try:
            # Stream agent response
            for chunk in AgentService.execute_streaming(
                agent_id=agent_id,
                user_id=user_id,
                message=message,
                conversation_id=session_id,
                context=context
            ):
                # Emit chunk to room
                emit('agent_response_chunk', {
                    'session_id': session_id,
                    'agent_id': agent_id,
                    'chunk': chunk
                }, room=session_id)
            
            # Emit completion
            emit('agent_response_complete', {
                'session_id': session_id,
                'agent_id': agent_id
            }, room=session_id)
            
        except Exception as e:
            emit('agent_error', {
                'session_id': session_id,
                'agent_id': agent_id,
                'error': str(e)
            }, room=session_id)
        
        finally:
            # Stop typing indicator
            emit('agent_typing', {
                'session_id': session_id,
                'agent_id': agent_id,
                'typing': False
            }, room=session_id)
    
    @socketio.on('agent_interrupt')
    @authenticated_only
    def handle_agent_interrupt(data, user_id=None):
        """
        Interrupt agent execution
        
        Data:
            - session_id: Session ID
            - agent_id: Agent ID
        """
        from .services.agent_service import AgentService
        
        session_id = data.get('session_id')
        agent_id = data.get('agent_id')
        
        if not all([session_id, agent_id]):
            emit('error', {'message': 'session_id and agent_id required'})
            return
        
        # Interrupt agent
        AgentService.interrupt(session_id, agent_id, user_id)
        
        # Emit interruption confirmation
        emit('agent_interrupted', {
            'session_id': session_id,
            'agent_id': agent_id
        }, room=session_id)
    
    @socketio.on('typing')
    def handle_typing(data):
        """
        Broadcast user typing status
        
        Data:
            - session_id: Session ID
            - typing: Boolean
        """
        session_id = data.get('session_id')
        typing = data.get('typing', False)
        
        if not session_id:
            return
        
        emit('user_typing', {
            'session_id': session_id,
            'typing': typing
        }, room=session_id, include_self=False)
    
    @socketio.on('ping')
    def handle_ping():
        """Simple ping/pong for connection health check"""
        emit('pong', {'timestamp': datetime.now().isoformat()})
    
    print("✓ WebSocket events registered")
