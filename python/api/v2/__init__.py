"""
Enhanced API v2 for Agent Zero Enterprise
Provides RESTful endpoints, WebSocket support, and GraphQL capabilities
"""

from flask import Blueprint, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Create API blueprint
api_v2_blueprint = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(api_v2_blueprint)

# JWT Manager (will be initialized with app)
jwt = JWTManager()

# Enable CORS
def init_cors(app):
    """Initialize CORS with appropriate settings"""
    CORS(app, resources={
        r"/api/v2/*": {
            "origins": ["http://localhost:3000", "https://*.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

# Health check endpoint
@api_v2_blueprint.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'service': 'agent-zero-enterprise'
    }), 200

# Import and register resources
def register_resources():
    """Register all API resources"""
    from .resources.agents import AgentResource, AgentListResource, AgentExecuteResource
    from .resources.conversations import ConversationResource, ConversationListResource
    from .resources.personas import PersonaResource, PersonaListResource
    from .resources.memory import MemoryResource, MemorySearchResource
    from .resources.analytics import AnalyticsResource
    from .resources.auth import LoginResource, RefreshResource, RegisterResource
    
    # Auth endpoints
    api.add_resource(RegisterResource, '/auth/register')
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(RefreshResource, '/auth/refresh')
    
    # Agent endpoints
    api.add_resource(AgentListResource, '/agents')
    api.add_resource(AgentResource, '/agents/<string:agent_id>')
    api.add_resource(AgentExecuteResource, '/agents/<string:agent_id>/execute')
    
    # Conversation endpoints
    api.add_resource(ConversationListResource, '/conversations')
    api.add_resource(ConversationResource, '/conversations/<string:conversation_id>')
    
    # Persona endpoints
    api.add_resource(PersonaListResource, '/personas')
    api.add_resource(PersonaResource, '/personas/<string:persona_id>')
    
    # Memory endpoints
    api.add_resource(MemoryResource, '/memory/<string:memory_id>')
    api.add_resource(MemorySearchResource, '/memory/search')
    
    # Analytics endpoints
    api.add_resource(AnalyticsResource, '/analytics')

def init_api_v2(app, socketio=None):
    """
    Initialize API v2 with Flask app
    
    Args:
        app: Flask application instance
        socketio: SocketIO instance for real-time features
    """
    # Initialize JWT
    jwt.init_app(app)
    
    # Register resources
    register_resources()
    
    # Register blueprint
    app.register_blueprint(api_v2_blueprint)
    
    # Initialize CORS
    init_cors(app)
    
    # Initialize WebSocket events if socketio provided
    if socketio:
        from .websocket import register_websocket_events
        register_websocket_events(socketio)
    
    print("✓ API v2 initialized successfully")

# JWT callbacks
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'token_expired',
        'message': 'The token has expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Token verification failed'
    }), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        'error': 'unauthorized',
        'message': 'Authorization required'
    }), 401
