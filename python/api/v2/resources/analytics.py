"""
Analytics API endpoints
"""

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.analytics_service import AnalyticsService
from datetime import datetime, timedelta

class AnalyticsResource(Resource):
    """Analytics and usage statistics"""
    
    @jwt_required()
    def get(self):
        """
        Get analytics for current user
        
        Query params:
            - period: Time period (day, week, month, year) default: month
            - start_date: Start date (ISO format) optional
            - end_date: End date (ISO format) optional
            - agent_id: Filter by specific agent (optional)
        """
        user_id = get_jwt_identity()
        period = request.args.get('period', 'month')
        agent_id = request.args.get('agent_id')
        
        # Parse dates
        end_date = datetime.now()
        if request.args.get('end_date'):
            end_date = datetime.fromisoformat(request.args.get('end_date'))
        
        start_date = None
        if request.args.get('start_date'):
            start_date = datetime.fromisoformat(request.args.get('start_date'))
        else:
            # Calculate start date based on period
            if period == 'day':
                start_date = end_date - timedelta(days=1)
            elif period == 'week':
                start_date = end_date - timedelta(weeks=1)
            elif period == 'month':
                start_date = end_date - timedelta(days=30)
            elif period == 'year':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)
        
        # Get analytics
        analytics = AnalyticsService.get_analytics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            agent_id=agent_id
        )
        
        return analytics.dict(), 200
