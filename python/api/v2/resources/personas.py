"""
Persona management API endpoints
"""

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import PersonaCreate, PersonaUpdate, PersonaResponse
from ..services.persona_service import PersonaService
from pydantic import ValidationError

class PersonaListResource(Resource):
    """List and create personas"""
    
    @jwt_required()
    def get(self):
        """
        Get all personas for current user
        
        Query params:
            - domain: Filter by domain (optional)
            - limit: Number of results (default 50)
            - offset: Pagination offset (default 0)
        """
        user_id = get_jwt_identity()
        domain = request.args.get('domain')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        personas = PersonaService.list_personas(
            user_id=user_id,
            domain=domain,
            limit=limit,
            offset=offset
        )
        
        return {
            'personas': [p.dict() for p in personas],
            'total': len(personas),
            'limit': limit,
            'offset': offset
        }, 200
    
    @jwt_required()
    def post(self):
        """
        Create a new persona
        
        Request body: PersonaCreate model
        """
        user_id = get_jwt_identity()
        
        try:
            data = PersonaCreate(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        try:
            persona = PersonaService.create_persona(user_id, data)
            return persona.dict(), 201
        except Exception as e:
            return {'error': 'creation_failed', 'message': str(e)}, 500

class PersonaResource(Resource):
    """Individual persona operations"""
    
    @jwt_required()
    def get(self, persona_id):
        """Get persona by ID"""
        user_id = get_jwt_identity()
        
        persona = PersonaService.get_persona(persona_id, user_id)
        if not persona:
            return {'error': 'not_found', 'message': 'Persona not found'}, 404
        
        return persona.dict(), 200
    
    @jwt_required()
    def put(self, persona_id):
        """Update persona"""
        user_id = get_jwt_identity()
        
        try:
            data = PersonaUpdate(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        persona = PersonaService.update_persona(persona_id, user_id, data)
        if not persona:
            return {'error': 'not_found', 'message': 'Persona not found'}, 404
        
        return persona.dict(), 200
    
    @jwt_required()
    def delete(self, persona_id):
        """Delete persona"""
        user_id = get_jwt_identity()
        
        success = PersonaService.delete_persona(persona_id, user_id)
        if not success:
            return {'error': 'not_found', 'message': 'Persona not found'}, 404
        
        return {'message': 'Persona deleted successfully'}, 200
