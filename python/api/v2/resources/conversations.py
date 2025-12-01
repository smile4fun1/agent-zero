"""
Conversation management API endpoints
"""

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import ConversationCreate, ConversationUpdate
from ..services.conversation_service import ConversationService
from pydantic import ValidationError

class ConversationListResource(Resource):
    """List and create conversations"""
    
    @jwt_required()
    def get(self):
        """
        Get all conversations for current user
        
        Query params:
            - agent_id: Filter by agent (optional)
            - archived: Filter by archived status (optional)
            - limit: Number of results (default 50)
            - offset: Pagination offset (default 0)
        """
        user_id = get_jwt_identity()
        agent_id = request.args.get('agent_id')
        archived = request.args.get('archived')
        if archived is not None:
            archived = archived.lower() == 'true'
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        conversations = ConversationService.list_conversations(
            user_id=user_id,
            agent_id=agent_id,
            archived=archived,
            limit=limit,
            offset=offset
        )
        
        return {
            'conversations': [c.dict() for c in conversations],
            'total': len(conversations),
            'limit': limit,
            'offset': offset
        }, 200
    
    @jwt_required()
    def post(self):
        """
        Create a new conversation
        
        Request body: ConversationCreate model
        """
        user_id = get_jwt_identity()
        
        try:
            data = ConversationCreate(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        try:
            conversation = ConversationService.create_conversation(user_id, data)
            return conversation.dict(), 201
        except Exception as e:
            return {'error': 'creation_failed', 'message': str(e)}, 500

class ConversationResource(Resource):
    """Individual conversation operations"""
    
    @jwt_required()
    def get(self, conversation_id):
        """Get conversation by ID with all messages"""
        user_id = get_jwt_identity()
        
        conversation = ConversationService.get_conversation(conversation_id, user_id)
        if not conversation:
            return {'error': 'not_found', 'message': 'Conversation not found'}, 404
        
        return conversation.dict(), 200
    
    @jwt_required()
    def put(self, conversation_id):
        """Update conversation (e.g., title, archive status)"""
        user_id = get_jwt_identity()
        
        try:
            data = ConversationUpdate(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        conversation = ConversationService.update_conversation(conversation_id, user_id, data)
        if not conversation:
            return {'error': 'not_found', 'message': 'Conversation not found'}, 404
        
        return conversation.dict(), 200
    
    @jwt_required()
    def delete(self, conversation_id):
        """Delete conversation"""
        user_id = get_jwt_identity()
        
        success = ConversationService.delete_conversation(conversation_id, user_id)
        if not success:
            return {'error': 'not_found', 'message': 'Conversation not found'}, 404
        
        return {'message': 'Conversation deleted successfully'}, 200
