"""
Memory management API endpoints
"""

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import MemoryCreate, MemorySearch
from ..services.memory_service import MemoryService
from pydantic import ValidationError

class MemoryResource(Resource):
    """Individual memory operations"""
    
    @jwt_required()
    def get(self, memory_id):
        """Get memory by ID"""
        user_id = get_jwt_identity()
        
        memory = MemoryService.get_memory(memory_id, user_id)
        if not memory:
            return {'error': 'not_found', 'message': 'Memory not found'}, 404
        
        return memory.dict(), 200
    
    @jwt_required()
    def delete(self, memory_id):
        """Delete memory"""
        user_id = get_jwt_identity()
        
        success = MemoryService.delete_memory(memory_id, user_id)
        if not success:
            return {'error': 'not_found', 'message': 'Memory not found'}, 404
        
        return {'message': 'Memory deleted successfully'}, 200

class MemorySearchResource(Resource):
    """Memory search and creation"""
    
    @jwt_required()
    def post(self):
        """
        Search memories using semantic search
        
        Request body: MemorySearch model
        """
        user_id = get_jwt_identity()
        
        try:
            data = MemorySearch(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        memories = MemoryService.search_memories(
            user_id=user_id,
            query=data.query,
            limit=data.limit,
            agent_id=data.agent_id,
            memory_type=data.type
        )
        
        return {
            'memories': [m.dict() for m in memories],
            'total': len(memories)
        }, 200
    
    @jwt_required()
    def put(self):
        """
        Create a new memory
        
        Request body: MemoryCreate model
        """
        user_id = get_jwt_identity()
        
        try:
            data = MemoryCreate(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        try:
            memory = MemoryService.create_memory(user_id, data)
            return memory.dict(), 201
        except Exception as e:
            return {'error': 'creation_failed', 'message': str(e)}, 500
