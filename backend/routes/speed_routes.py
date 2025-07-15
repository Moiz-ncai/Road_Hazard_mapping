from flask import Blueprint, request, jsonify
from sqlalchemy import and_
import math
import sys
import os

# Add parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import db
from models.hazard import Hazard, SeverityLevel

speed_bp = Blueprint('speed', __name__)

class SpeedRecommendationEngine:
    """Engine for calculating speed recommendations based on hazards"""
    
    # Speed reduction factors based on severity
    SPEED_FACTORS = {
        SeverityLevel.HIGH: 0.5,      # 40-60% of speed limit
        SeverityLevel.MEDIUM: 0.75,   # 70-80% of speed limit
        SeverityLevel.LOW: 0.90       # 85-95% of speed limit
    }
    
    # Distance-based impact factors (in km)
    DISTANCE_FACTORS = {
        0.1: 1.0,   # Full impact within 100m
        0.2: 0.8,   # 80% impact within 200m
        0.5: 0.5,   # 50% impact within 500m
        1.0: 0.2,   # 20% impact within 1km
        2.0: 0.1    # 10% impact within 2km
    }
    
    @staticmethod
    def calculate_distance(lat1, lng1, lat2, lng2):
        """Calculate distance between two points in kilometers"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng/2) * math.sin(delta_lng/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    @staticmethod
    def get_distance_factor(distance_km):
        """Get impact factor based on distance to hazard"""
        for threshold, factor in sorted(SpeedRecommendationEngine.DISTANCE_FACTORS.items()):
            if distance_km <= threshold:
                return factor
        return 0.0  # No impact beyond 2km
    
    @staticmethod
    def calculate_recommended_speed(current_location, hazards, base_speed_limit):
        """Calculate recommended speed based on nearby hazards"""
        lat, lng = current_location['lat'], current_location['lng']
        
        # Start with base speed limit
        recommended_speed = base_speed_limit
        total_impact = 0.0
        
        for hazard in hazards:
            # Calculate distance to hazard
            distance = SpeedRecommendationEngine.calculate_distance(
                lat, lng, hazard.latitude, hazard.longitude
            )
            
            # Get distance and severity factors
            distance_factor = SpeedRecommendationEngine.get_distance_factor(distance)
            severity_factor = SpeedRecommendationEngine.SPEED_FACTORS[hazard.severity_level]
            
            # Calculate impact for this hazard
            if distance_factor > 0:
                impact = (1 - severity_factor) * distance_factor
                total_impact += impact
        
        # Apply cumulative impact (cap at 0.8 to prevent extremely low speeds)
        total_impact = min(total_impact, 0.8)
        recommended_speed = int(base_speed_limit * (1 - total_impact))
        
        # Ensure minimum speed of 20 km/h for safety
        recommended_speed = max(recommended_speed, 20)
        
        return recommended_speed

@speed_bp.route('/speed-recommendations', methods=['POST'])
def get_speed_recommendations():
    """Calculate safe speeds for route segments"""
    try:
        data = request.get_json()
        
        # Expected data: {'waypoints': [{'lat': float, 'lng': float, 'speed_limit': int}], 'search_radius_km': float}
        waypoints = data.get('waypoints', [])
        search_radius_km = data.get('search_radius_km', 1.0)
        
        if not waypoints:
            return jsonify({'error': 'No waypoints provided'}), 400
        
        recommendations = []
        
        for i, waypoint in enumerate(waypoints):
            lat = waypoint['lat']
            lng = waypoint['lng']
            speed_limit = waypoint.get('speed_limit', 50)  # Default 50 km/h
            
            # Find nearby hazards
            radius_deg = search_radius_km / 111.0
            hazards = Hazard.query.filter(
                and_(
                    Hazard.latitude >= lat - radius_deg,
                    Hazard.latitude <= lat + radius_deg,
                    Hazard.longitude >= lng - radius_deg,
                    Hazard.longitude <= lng + radius_deg
                )
            ).all()
            
            # Calculate recommended speed
            recommended_speed = SpeedRecommendationEngine.calculate_recommended_speed(
                {'lat': lat, 'lng': lng}, hazards, speed_limit
            )
            
            # Get hazard details for this segment
            hazard_details = []
            for hazard in hazards:
                distance = SpeedRecommendationEngine.calculate_distance(
                    lat, lng, hazard.latitude, hazard.longitude
                )
                if distance <= search_radius_km:
                    hazard_details.append({
                        'id': hazard.id,
                        'type': hazard.hazard_type.value,
                        'severity': hazard.severity_level.value,
                        'distance_km': round(distance, 2),
                        'road_name': hazard.road_name
                    })
            
            recommendations.append({
                'waypoint_index': i,
                'location': {'lat': lat, 'lng': lng},
                'speed_limit': speed_limit,
                'recommended_speed': recommended_speed,
                'speed_reduction': speed_limit - recommended_speed,
                'hazards_count': len(hazard_details),
                'hazards': hazard_details
            })
        
        return jsonify({
            'recommendations': recommendations,
            'search_radius_km': search_radius_km,
            'total_waypoints': len(waypoints)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@speed_bp.route('/speed-recommendations/location', methods=['GET'])
def get_location_speed_recommendation():
    """Get speed recommendation for a specific location"""
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        speed_limit = request.args.get('speed_limit', type=int, default=50)
        radius_km = request.args.get('radius_km', type=float, default=1.0)
        
        if not lat or not lng:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        # Find nearby hazards
        radius_deg = radius_km / 111.0
        hazards = Hazard.query.filter(
            and_(
                Hazard.latitude >= lat - radius_deg,
                Hazard.latitude <= lat + radius_deg,
                Hazard.longitude >= lng - radius_deg,
                Hazard.longitude <= lng + radius_deg
            )
        ).all()
        
        # Calculate recommended speed
        recommended_speed = SpeedRecommendationEngine.calculate_recommended_speed(
            {'lat': lat, 'lng': lng}, hazards, speed_limit
        )
        
        # Get hazard details
        hazard_details = []
        for hazard in hazards:
            distance = SpeedRecommendationEngine.calculate_distance(
                lat, lng, hazard.latitude, hazard.longitude
            )
            if distance <= radius_km:
                hazard_details.append({
                    'id': hazard.id,
                    'type': hazard.hazard_type.value,
                    'severity': hazard.severity_level.value,
                    'distance_km': round(distance, 2),
                    'road_name': hazard.road_name,
                    'recommended_speed': hazard.recommended_speed
                })
        
        return jsonify({
            'location': {'lat': lat, 'lng': lng},
            'speed_limit': speed_limit,
            'recommended_speed': recommended_speed,
            'speed_reduction': speed_limit - recommended_speed,
            'hazards_count': len(hazard_details),
            'hazards': hazard_details,
            'safety_status': 'safe' if len(hazard_details) == 0 else 'caution' if recommended_speed > speed_limit * 0.8 else 'danger'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@speed_bp.route('/speed-recommendations/route-analysis', methods=['POST'])
def analyze_route_safety():
    """Analyze overall route safety and provide summary"""
    try:
        data = request.get_json()
        
        waypoints = data.get('waypoints', [])
        if not waypoints:
            return jsonify({'error': 'No waypoints provided'}), 400
        
        # Get speed recommendations for all waypoints
        recommendations_response = get_speed_recommendations()
        recommendations_data = recommendations_response[0].get_json()
        
        if 'recommendations' not in recommendations_data:
            return jsonify({'error': 'Failed to get recommendations'}), 500
        
        recommendations = recommendations_data['recommendations']
        
        # Analyze route safety
        total_hazards = sum(rec['hazards_count'] for rec in recommendations)
        total_speed_reduction = sum(rec['speed_reduction'] for rec in recommendations)
        avg_speed_reduction = total_speed_reduction / len(recommendations) if recommendations else 0
        
        # Categorize route safety
        if total_hazards == 0:
            safety_level = 'safe'
        elif avg_speed_reduction <= 10:
            safety_level = 'low_risk'
        elif avg_speed_reduction <= 20:
            safety_level = 'moderate_risk'
        else:
            safety_level = 'high_risk'
        
        # Find most dangerous segment
        most_dangerous = max(recommendations, key=lambda x: x['speed_reduction']) if recommendations else None
        
        # Hazard distribution
        hazard_types = {}
        severity_distribution = {'low': 0, 'medium': 0, 'high': 0}
        
        for rec in recommendations:
            for hazard in rec['hazards']:
                hazard_types[hazard['type']] = hazard_types.get(hazard['type'], 0) + 1
                severity_distribution[hazard['severity']] += 1
        
        return jsonify({
            'route_analysis': {
                'total_waypoints': len(waypoints),
                'total_hazards': total_hazards,
                'average_speed_reduction': round(avg_speed_reduction, 1),
                'safety_level': safety_level,
                'hazard_distribution': hazard_types,
                'severity_distribution': severity_distribution,
                'most_dangerous_segment': most_dangerous,
                'estimated_extra_time_minutes': round(total_speed_reduction * 0.1, 1)  # Rough estimate
            },
            'detailed_recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 