"""
Authentication API endpoints
"""

from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from ..models import UserRegister, UserLogin, TokenResponse
from ..services.auth_service import AuthService
from pydantic import ValidationError
from datetime import timedelta

class RegisterResource(Resource):
    """User registration"""
    
    def post(self):
        """
        Register a new user
        
        Request body: UserRegister model
        """
        try:
            data = UserRegister(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        # Check if user already exists
        if AuthService.user_exists(data.email):
            return {'error': 'user_exists', 'message': 'User with this email already exists'}, 409
        
        # Create user
        try:
            user = AuthService.create_user(data)
            
            # Generate tokens
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(hours=1)
            )
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=timedelta(days=30)
            )
            
            return {
                'user': user.dict(),
                'tokens': TokenResponse(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expires_in=3600
                ).dict()
            }, 201
        except Exception as e:
            return {'error': 'registration_failed', 'message': str(e)}, 500

class LoginResource(Resource):
    """User login"""
    
    def post(self):
        """
        Login user
        
        Request body: UserLogin model
        """
        try:
            data = UserLogin(**request.json)
        except ValidationError as e:
            return {'error': 'validation_error', 'details': e.errors()}, 400
        
        # Authenticate user
        user = AuthService.authenticate(data.email, data.password)
        if not user:
            return {'error': 'invalid_credentials', 'message': 'Invalid email or password'}, 401
        
        # Generate tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return {
            'user': user.dict(),
            'tokens': TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=3600
            ).dict()
        }, 200

class RefreshResource(Resource):
    """Token refresh"""
    
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh access token
        
        Requires: Refresh token in Authorization header
        """
        user_id = get_jwt_identity()
        
        # Generate new access token
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(hours=1)
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token="",  # Don't issue new refresh token
            expires_in=3600
        ).dict(), 200
