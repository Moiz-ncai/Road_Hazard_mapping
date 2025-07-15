from flask import Blueprint, request, jsonify
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import db
from models.hazard import Hazard, HazardType, SeverityLevel

hazard_bp = Blueprint('hazards', __name__)

@hazard_bp.route('/hazards', methods=['POST'])
def create_hazard():
    """Create a new hazard detection"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['latitude', 'longitude', 'hazard_type', 'severity_level', 
                          'speed_limit', 'recommended_speed', 'road_name', 'area']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create hazard from data
        hazard = Hazard.from_dict(data)
        
        # Set location geometry
        hazard.location = func.ST_GeomFromText(f'POINT({data["longitude"]} {data["latitude"]})', 4326)
        
        db.session.add(hazard)
        db.session.commit()
        
        return jsonify({
            'message': 'Hazard created successfully',
            'hazard': hazard.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hazard_bp.route('/hazards', methods=['GET'])
def get_hazards():
    """Retrieve hazards by geographic bounds and filters"""
    try:
        # Get query parameters
        north = request.args.get('north', type=float)
        south = request.args.get('south', type=float)
        east = request.args.get('east', type=float)
        west = request.args.get('west', type=float)
        
        hazard_type = request.args.get('hazard_type')
        severity_level = request.args.get('severity_level')
        hours_back = request.args.get('hours_back', type=int, default=24)
        verified_only = request.args.get('verified_only', type=bool, default=False)
        
        # Build query
        query = Hazard.query
        
        # Apply geographic bounds filter
        if all([north, south, east, west]):
            query = query.filter(
                and_(
                    Hazard.latitude >= south,
                    Hazard.latitude <= north,
                    Hazard.longitude >= west,
                    Hazard.longitude <= east
                )
            )
        
        # Apply filters
        if hazard_type:
            query = query.filter(Hazard.hazard_type == HazardType(hazard_type))
        
        if severity_level:
            query = query.filter(Hazard.severity_level == SeverityLevel(severity_level))
        
        if verified_only:
            query = query.filter(Hazard.verified == True)
        
        # Apply time filter
        if hours_back > 0:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
            query = query.filter(Hazard.detection_timestamp >= cutoff_time)
        
        # Execute query
        hazards = query.all()
        
        return jsonify({
            'hazards': [hazard.to_dict() for hazard in hazards],
            'count': len(hazards)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hazard_bp.route('/hazards/<int:hazard_id>', methods=['GET'])
def get_hazard(hazard_id):
    """Get a specific hazard by ID"""
    try:
        hazard = Hazard.query.get_or_404(hazard_id)
        return jsonify(hazard.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hazard_bp.route('/hazards/<int:hazard_id>', methods=['PUT'])
def update_hazard(hazard_id):
    """Update a hazard (e.g., verify it)"""
    try:
        hazard = Hazard.query.get_or_404(hazard_id)
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['verified', 'severity_level', 'recommended_speed', 'weather_condition']
        
        for field in allowed_fields:
            if field in data:
                if field == 'severity_level':
                    setattr(hazard, field, SeverityLevel(data[field]))
                else:
                    setattr(hazard, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Hazard updated successfully',
            'hazard': hazard.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hazard_bp.route('/hazards/<int:hazard_id>', methods=['DELETE'])
def delete_hazard(hazard_id):
    """Delete a hazard"""
    try:
        hazard = Hazard.query.get_or_404(hazard_id)
        db.session.delete(hazard)
        db.session.commit()
        
        return jsonify({'message': 'Hazard deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@hazard_bp.route('/hazards/route', methods=['POST'])
def get_hazards_along_route():
    """Get hazards along a specific route"""
    try:
        data = request.get_json()
        
        # Expected data: {'waypoints': [{'lat': float, 'lng': float}, ...], 'buffer_km': float}
        waypoints = data.get('waypoints', [])
        buffer_km = data.get('buffer_km', 0.5)  # Default 500m buffer
        
        if not waypoints:
            return jsonify({'error': 'No waypoints provided'}), 400
        
        # For simplicity, we'll find hazards within a bounding box of all waypoints
        # In a production system, you'd use proper route geometry
        
        lats = [wp['lat'] for wp in waypoints]
        lngs = [wp['lng'] for wp in waypoints]
        
        # Add buffer
        buffer_deg = buffer_km / 111.0  # Rough conversion km to degrees
        
        min_lat = min(lats) - buffer_deg
        max_lat = max(lats) + buffer_deg
        min_lng = min(lngs) - buffer_deg
        max_lng = max(lngs) + buffer_deg
        
        hazards = Hazard.query.filter(
            and_(
                Hazard.latitude >= min_lat,
                Hazard.latitude <= max_lat,
                Hazard.longitude >= min_lng,
                Hazard.longitude <= max_lng
            )
        ).all()
        
        return jsonify({
            'hazards': [hazard.to_dict() for hazard in hazards],
            'route_info': {
                'waypoints_count': len(waypoints),
                'buffer_km': buffer_km,
                'hazards_found': len(hazards)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@hazard_bp.route('/hazards/nearby', methods=['GET'])
def get_nearby_hazards():
    """Get hazards near a specific location"""
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius_km = request.args.get('radius_km', type=float, default=1.0)
        
        if not lat or not lng:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        # Convert km to degrees (rough approximation)
        radius_deg = radius_km / 111.0
        
        hazards = Hazard.query.filter(
            and_(
                Hazard.latitude >= lat - radius_deg,
                Hazard.latitude <= lat + radius_deg,
                Hazard.longitude >= lng - radius_deg,
                Hazard.longitude <= lng + radius_deg
            )
        ).all()
        
        return jsonify({
            'hazards': [hazard.to_dict() for hazard in hazards],
            'center': {'lat': lat, 'lng': lng},
            'radius_km': radius_km,
            'count': len(hazards)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 