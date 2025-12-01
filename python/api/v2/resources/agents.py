"""
Agent management API endpoints
"""

from flask import request, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import AgentCreate, AgentUpdate, AgentExecuteRequest
from ..services.agent_service import AgentService
from pydantic import ValidationError
import json

class AgentListResource(Resource):
    """List and create agents"""
    
    @jwt_required()
    def get(self):
        """
        Get all agents for current user
        
        Query params:
            - status: Filter by status (optional)
            - persona_id: Filter by persona (optional)
            - limit: Number of results (default 50)
            - offset: Pagination offset (default 0)
        """
        user_id = get_jwt_identity()
        status = request.args.get('status')
        persona_id = request.args.get('persona_id')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        agents = AgentService.list_agents(
            user_id=user_id,
            status=status,
            persona_id=persona_id,
            limit=limit,
            offset=offset
        )
        
        return {
            'agents': [a.dict() for a in agents],
            'total': len(agents),
            'limit': limit,
            'offset': offset
        }, 200
    
    @jwt_required()
    def post(self):
        """
        Create a new agent
        
        Request body: AgentCreate model
        """
        user_id = get_jwt_identity()
        
        try:
            data = AgentCreate(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        try:
            agent = AgentService.create_agent(user_id, data)
            return agent.dict(), 201
        except Exception as e:
            return {'error': 'creation_failed', 'message': str(e)}, 500

class AgentResource(Resource):
    """Individual agent operations"""
    
    @jwt_required()
    def get(self, agent_id):
        """Get agent by ID"""
        user_id = get_jwt_identity()
        
        agent = AgentService.get_agent(agent_id, user_id)
        if not agent:
            return {'error': 'not_found', 'message': 'Agent not found'}, 404
        
        return agent.dict(), 200
    
    @jwt_required()
    def put(self, agent_id):
        """Update agent"""
        user_id = get_jwt_identity()
        
        try:
            data = AgentUpdate(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        agent = AgentService.update_agent(agent_id, user_id, data)
        if not agent:
            return {'error': 'not_found', 'message': 'Agent not found'}, 404
        
        return agent.dict(), 200
    
    @jwt_required()
    def delete(self, agent_id):
        """Delete agent"""
        user_id = get_jwt_identity()
        
        success = AgentService.delete_agent(agent_id, user_id)
        if not success:
            return {'error': 'not_found', 'message': 'Agent not found'}, 404
        
        return {'message': 'Agent deleted successfully'}, 200

class AgentExecuteResource(Resource):
    """Execute agent tasks"""
    
    @jwt_required()
    def post(self, agent_id):
        """
        Execute a task with the agent
        
        Request body: AgentExecuteRequest model
        Returns: Streaming response or JSON response
        """
        user_id = get_jwt_identity()
        
        try:
            data = AgentExecuteRequest(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        # Check if agent exists and user has access
        agent = AgentService.get_agent(agent_id, user_id)
        if not agent:
            return {'error': 'not_found', 'message': 'Agent not found'}, 404
        
        # Execute the task
        if data.stream:
            # Return streaming response
            def generate():
                try:
                    for chunk in AgentService.execute_streaming(
                        agent_id=agent_id,
                        user_id=user_id,
                        message=data.message,
                        conversation_id=data.conversation_id,
                        context=data.context
                    ):
                        # Send Server-Sent Events format
                        yield f"data: {json.dumps(chunk)}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            return Response(
                generate(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        else:
            # Return full response
            result = AgentService.execute(
                agent_id=agent_id,
                user_id=user_id,
                message=data.message,
                conversation_id=data.conversation_id,
                context=data.context
            )
            return result, 200
