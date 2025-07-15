import random
import json
from datetime import datetime, timedelta
from models.hazard import Hazard, HazardType, SeverityLevel
import sys
import os

# Add parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import db

class PeshawarHazardDataGenerator:
    """Generate realistic hazard data for Peshawar, Pakistan"""
    
    # Peshawar geographic bounds
    PESHAWAR_BOUNDS = {
        'lat_min': 33.9,
        'lat_max': 34.1,
        'lng_min': 71.4,
        'lng_max': 71.7
    }
    
    # Major roads and areas in Peshawar
    MAJOR_ROADS = [
        {
            'name': 'GT Road',
            'area': 'Cantonment',
            'speed_limit': 80,
            'coordinates': [(34.0151, 71.5249), (34.0089, 71.5456), (34.0023, 71.5678)]
        },
        {
            'name': 'University Road',
            'area': 'University Town',
            'speed_limit': 60,
            'coordinates': [(34.0151, 71.5249), (34.0198, 71.5156), (34.0245, 71.5089)]
        },
        {
            'name': 'Ring Road',
            'area': 'Hayatabad',
            'speed_limit': 80,
            'coordinates': [(33.9889, 71.4756), (33.9945, 71.4689), (34.0012, 71.4623)]
        },
        {
            'name': 'Jamrud Road',
            'area': 'Board Bazaar',
            'speed_limit': 50,
            'coordinates': [(34.0151, 71.5249), (34.0089, 71.5356), (34.0023, 71.5478)]
        },
        {
            'name': 'Peshawar Road',
            'area': 'Saddar',
            'speed_limit': 40,
            'coordinates': [(34.0151, 71.5249), (34.0198, 71.5356), (34.0245, 71.5478)]
        },
        {
            'name': 'Charsadda Road',
            'area': 'Charsadda',
            'speed_limit': 60,
            'coordinates': [(34.0312, 71.5234), (34.0378, 71.5156), (34.0445, 71.5089)]
        },
        {
            'name': 'Kohat Road',
            'area': 'Kohat',
            'speed_limit': 70,
            'coordinates': [(34.0089, 71.5456), (34.0023, 71.5578), (33.9956, 71.5689)]
        },
        {
            'name': 'Warsak Road',
            'area': 'Warsak',
            'speed_limit': 50,
            'coordinates': [(34.0456, 71.5123), (34.0523, 71.5056), (34.0589, 71.4989)]
        }
    ]
    
    # Hazard type probabilities (realistic distribution)
    HAZARD_TYPE_PROBABILITIES = {
        HazardType.POTHOLE: 0.45,      # Most common in Pakistan
        HazardType.CRACK: 0.25,        # Second most common
        HazardType.DEBRIS: 0.15,       # Road debris
        HazardType.CONSTRUCTION: 0.10, # Construction zones
        HazardType.FLOODING: 0.05      # Monsoon season
    }
    
    # Severity distribution (60% low, 30% medium, 10% high)
    SEVERITY_PROBABILITIES = {
        SeverityLevel.LOW: 0.60,
        SeverityLevel.MEDIUM: 0.30,
        SeverityLevel.HIGH: 0.10
    }
    
    # Weather conditions in Peshawar
    WEATHER_CONDITIONS = [
        'Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Heavy Rain',
        'Dust Storm', 'Foggy', 'Hot', 'Mild', 'Cold'
    ]
    
    @staticmethod
    def generate_random_coordinate_near_road(road_data):
        """Generate random coordinate near a specific road"""
        coordinates = road_data['coordinates']
        base_coord = random.choice(coordinates)
        
        # Add some randomness around the road (±0.001 degrees ≈ ±100m)
        lat_offset = random.uniform(-0.001, 0.001)
        lng_offset = random.uniform(-0.001, 0.001)
        
        lat = base_coord[0] + lat_offset
        lng = base_coord[1] + lng_offset
        
        return lat, lng
    
    @staticmethod
    def generate_random_coordinate_in_peshawar():
        """Generate random coordinate within Peshawar bounds"""
        lat = random.uniform(
            PeshawarHazardDataGenerator.PESHAWAR_BOUNDS['lat_min'],
            PeshawarHazardDataGenerator.PESHAWAR_BOUNDS['lat_max']
        )
        lng = random.uniform(
            PeshawarHazardDataGenerator.PESHAWAR_BOUNDS['lng_min'],
            PeshawarHazardDataGenerator.PESHAWAR_BOUNDS['lng_max']
        )
        return lat, lng
    
    @staticmethod
    def select_hazard_type():
        """Select hazard type based on probability distribution"""
        rand = random.random()
        cumulative = 0
        for hazard_type, probability in PeshawarHazardDataGenerator.HAZARD_TYPE_PROBABILITIES.items():
            cumulative += probability
            if rand <= cumulative:
                return hazard_type
        return HazardType.POTHOLE  # Default fallback
    
    @staticmethod
    def select_severity_level():
        """Select severity level based on probability distribution"""
        rand = random.random()
        cumulative = 0
        for severity, probability in PeshawarHazardDataGenerator.SEVERITY_PROBABILITIES.items():
            cumulative += probability
            if rand <= cumulative:
                return severity
        return SeverityLevel.LOW  # Default fallback
    
    @staticmethod
    def calculate_recommended_speed(speed_limit, severity_level):
        """Calculate recommended speed based on hazard severity"""
        if severity_level == SeverityLevel.HIGH:
            return max(int(speed_limit * 0.5), 20)
        elif severity_level == SeverityLevel.MEDIUM:
            return max(int(speed_limit * 0.75), 25)
        else:
            return max(int(speed_limit * 0.90), 30)
    
    @staticmethod
    def generate_detection_timestamp():
        """Generate realistic detection timestamp (last 30 days)"""
        days_back = random.randint(0, 30)
        hours_back = random.randint(0, 23)
        minutes_back = random.randint(0, 59)
        
        return datetime.utcnow() - timedelta(days=days_back, hours=hours_back, minutes=minutes_back)
    
    @staticmethod
    def generate_hazard_data(count=200):
        """Generate realistic hazard data for Peshawar"""
        hazards = []
        
        # 70% of hazards near major roads, 30% random locations
        major_road_count = int(count * 0.7)
        random_count = count - major_road_count
        
        # Generate hazards near major roads
        for _ in range(major_road_count):
            road_data = random.choice(PeshawarHazardDataGenerator.MAJOR_ROADS)
            lat, lng = PeshawarHazardDataGenerator.generate_random_coordinate_near_road(road_data)
            
            hazard_type = PeshawarHazardDataGenerator.select_hazard_type()
            severity_level = PeshawarHazardDataGenerator.select_severity_level()
            
            hazard = {
                'latitude': lat,
                'longitude': lng,
                'hazard_type': hazard_type.value,
                'severity_level': severity_level.value,
                'detection_timestamp': PeshawarHazardDataGenerator.generate_detection_timestamp().isoformat(),
                'confidence_score': random.uniform(0.7, 0.95),
                'speed_limit': road_data['speed_limit'],
                'recommended_speed': PeshawarHazardDataGenerator.calculate_recommended_speed(
                    road_data['speed_limit'], severity_level
                ),
                'verified': random.choice([True, False]) if random.random() > 0.3 else False,
                'road_name': road_data['name'],
                'area': road_data['area'],
                'weather_condition': random.choice(PeshawarHazardDataGenerator.WEATHER_CONDITIONS)
            }
            
            hazards.append(hazard)
        
        # Generate hazards at random locations
        for _ in range(random_count):
            lat, lng = PeshawarHazardDataGenerator.generate_random_coordinate_in_peshawar()
            
            hazard_type = PeshawarHazardDataGenerator.select_hazard_type()
            severity_level = PeshawarHazardDataGenerator.select_severity_level()
            speed_limit = random.choice([30, 40, 50, 60])  # Typical city speeds
            
            # Generate area name based on location
            if lat > 34.02:
                area = 'University Town'
            elif lat < 33.95:
                area = 'Hayatabad'
            elif lng > 71.6:
                area = 'Board Bazaar'
            else:
                area = 'Cantonment'
            
            hazard = {
                'latitude': lat,
                'longitude': lng,
                'hazard_type': hazard_type.value,
                'severity_level': severity_level.value,
                'detection_timestamp': PeshawarHazardDataGenerator.generate_detection_timestamp().isoformat(),
                'confidence_score': random.uniform(0.6, 0.9),
                'speed_limit': speed_limit,
                'recommended_speed': PeshawarHazardDataGenerator.calculate_recommended_speed(
                    speed_limit, severity_level
                ),
                'verified': random.choice([True, False]) if random.random() > 0.4 else False,
                'road_name': f'Local Road {random.randint(1, 100)}',
                'area': area,
                'weather_condition': random.choice(PeshawarHazardDataGenerator.WEATHER_CONDITIONS)
            }
            
            hazards.append(hazard)
        
        return hazards
    
    @staticmethod
    def save_to_json(hazards, filename='peshawar_hazards.json'):
        """Save hazards to JSON file"""
        with open(filename, 'w') as f:
            json.dump(hazards, f, indent=2)
        print(f"Saved {len(hazards)} hazards to {filename}")
    
    @staticmethod
    def load_to_database(hazards=None, count=200):
        """Load hazards into database"""
        if hazards is None:
            hazards = PeshawarHazardDataGenerator.generate_hazard_data(count)
        
        try:
            # Clear existing data
            db.session.query(Hazard).delete()
            
            # Add new hazards
            for hazard_data in hazards:
                hazard = Hazard.from_dict(hazard_data)
                db.session.add(hazard)
            
            db.session.commit()
            print(f"Successfully loaded {len(hazards)} hazards into database")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error loading hazards: {str(e)}")
            raise

def main():
    """Main function to generate and save dummy data"""
    print("Generating dummy hazard data for Peshawar...")
    
    # Generate hazards
    hazards = PeshawarHazardDataGenerator.generate_hazard_data(250)
    
    # Save to JSON
    PeshawarHazardDataGenerator.save_to_json(hazards)
    
    # Load to database (uncomment when database is ready)
    # PeshawarHazardDataGenerator.load_to_database(hazards)
    
    print("Dummy data generation complete!")

if __name__ == "__main__":
    main() 