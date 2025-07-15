import random
import time
from datetime import datetime
from typing import Dict, List, Optional
import math

class GPSSimulator:
    """Simulate GPS tracking for testing purposes"""
    
    def __init__(self, start_lat: float, start_lng: float, speed_kmh: float = 50):
        self.current_lat = start_lat
        self.current_lng = start_lng
        self.speed_kmh = speed_kmh
        self.heading = random.uniform(0, 360)  # Initial heading in degrees
        self.accuracy = random.uniform(3, 8)   # GPS accuracy in meters
        
    def calculate_new_position(self, time_delta_seconds: float) -> tuple:
        """Calculate new position based on speed and heading"""
        # Convert speed from km/h to m/s
        speed_ms = self.speed_kmh * 1000 / 3600
        
        # Calculate distance traveled
        distance_m = speed_ms * time_delta_seconds
        
        # Convert to degrees (rough approximation)
        distance_deg = distance_m / 111320  # meters per degree at equator
        
        # Calculate new position
        lat_change = distance_deg * math.cos(math.radians(self.heading))
        lng_change = distance_deg * math.sin(math.radians(self.heading))
        
        new_lat = self.current_lat + lat_change
        new_lng = self.current_lng + lng_change
        
        return new_lat, new_lng
    
    def add_noise(self, lat: float, lng: float) -> tuple:
        """Add GPS noise to simulate real-world conditions"""
        # Add random noise based on accuracy
        noise_range = self.accuracy / 111320  # Convert meters to degrees
        
        lat_noise = random.uniform(-noise_range, noise_range)
        lng_noise = random.uniform(-noise_range, noise_range)
        
        return lat + lat_noise, lng + lng_noise
    
    def update_heading(self):
        """Randomly update heading to simulate turns"""
        if random.random() < 0.1:  # 10% chance to turn
            heading_change = random.uniform(-30, 30)
            self.heading = (self.heading + heading_change) % 360
    
    def update_speed(self):
        """Randomly update speed to simulate traffic"""
        if random.random() < 0.05:  # 5% chance to change speed
            speed_change = random.uniform(-10, 10)
            self.speed_kmh = max(20, min(80, self.speed_kmh + speed_change))
    
    def get_current_position(self) -> Dict:
        """Get current GPS position with realistic data"""
        # Add noise to current position
        noisy_lat, noisy_lng = self.add_noise(self.current_lat, self.current_lng)
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'latitude': round(noisy_lat, 6),
            'longitude': round(noisy_lng, 6),
            'speed': round(self.speed_kmh, 1),
            'heading': round(self.heading, 1),
            'accuracy': round(self.accuracy, 1),
            'altitude': random.uniform(300, 600),  # Peshawar elevation
            'road_name': self.get_road_name(noisy_lat, noisy_lng)
        }
    
    def get_road_name(self, lat: float, lng: float) -> str:
        """Get road name based on coordinates (simplified)"""
        # This is a simplified implementation
        # In a real system, you'd use reverse geocoding
        
        if 34.01 <= lat <= 34.02 and 71.51 <= lng <= 71.53:
            return "University Road"
        elif 34.00 <= lat <= 34.01 and 71.54 <= lng <= 71.57:
            return "GT Road"
        elif 33.98 <= lat <= 34.00 and 71.47 <= lng <= 71.50:
            return "Ring Road"
        elif 34.00 <= lat <= 34.01 and 71.53 <= lng <= 71.55:
            return "Jamrud Road"
        else:
            return f"Local Road {random.randint(1, 100)}"
    
    def move(self, time_delta_seconds: float = 1.0):
        """Move to next position"""
        # Update position
        new_lat, new_lng = self.calculate_new_position(time_delta_seconds)
        self.current_lat = new_lat
        self.current_lng = new_lng
        
        # Update heading and speed occasionally
        self.update_heading()
        self.update_speed()
        
        # Update accuracy randomly
        self.accuracy = random.uniform(3, 8)

class RouteSimulator:
    """Simulate GPS tracking along a predefined route"""
    
    def __init__(self, waypoints: List[Dict], speed_kmh: float = 50):
        self.waypoints = waypoints
        self.current_waypoint_index = 0
        self.speed_kmh = speed_kmh
        self.progress = 0.0  # Progress between current and next waypoint (0-1)
        self.gps_simulator = GPSSimulator(
            waypoints[0]['lat'], 
            waypoints[0]['lng'], 
            speed_kmh
        )
    
    def get_current_position(self) -> Dict:
        """Get current position along the route"""
        if self.current_waypoint_index >= len(self.waypoints) - 1:
            # Reached end of route
            return self.gps_simulator.get_current_position()
        
        # Interpolate between current and next waypoint
        current = self.waypoints[self.current_waypoint_index]
        next_wp = self.waypoints[self.current_waypoint_index + 1]
        
        # Linear interpolation
        lat = current['lat'] + (next_wp['lat'] - current['lat']) * self.progress
        lng = current['lng'] + (next_wp['lng'] - current['lng']) * self.progress
        
        # Update GPS simulator position
        self.gps_simulator.current_lat = lat
        self.gps_simulator.current_lng = lng
        
        return self.gps_simulator.get_current_position()
    
    def move(self, time_delta_seconds: float = 1.0):
        """Move along the route"""
        if self.current_waypoint_index >= len(self.waypoints) - 1:
            return  # Reached end of route
        
        # Calculate distance to travel
        speed_ms = self.speed_kmh * 1000 / 3600
        distance_m = speed_ms * time_delta_seconds
        
        # Calculate total distance between current and next waypoint
        current = self.waypoints[self.current_waypoint_index]
        next_wp = self.waypoints[self.current_waypoint_index + 1]
        
        total_distance = self.calculate_distance(
            current['lat'], current['lng'],
            next_wp['lat'], next_wp['lng']
        )
        
        # Update progress
        distance_increment = distance_m / (total_distance * 1000)  # Convert to fraction
        self.progress += distance_increment
        
        # Check if we've reached the next waypoint
        if self.progress >= 1.0:
            self.current_waypoint_index += 1
            self.progress = 0.0
    
    @staticmethod
    def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
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

# Example usage and test functions
def test_gps_simulator():
    """Test GPS simulator with sample data"""
    print("Testing GPS Simulator...")
    
    # Start at University Road, Peshawar
    gps = GPSSimulator(34.0151, 71.5249, speed_kmh=50)
    
    print("Initial position:")
    print(gps.get_current_position())
    
    # Simulate movement for 10 seconds
    for i in range(10):
        time.sleep(1)
        gps.move(1.0)
        position = gps.get_current_position()
        print(f"Step {i+1}: Lat={position['latitude']}, Lng={position['longitude']}, Speed={position['speed']}")

def test_route_simulator():
    """Test route simulator with sample waypoints"""
    print("\nTesting Route Simulator...")
    
    # Sample route in Peshawar
    waypoints = [
        {'lat': 34.0151, 'lng': 71.5249},  # University Road
        {'lat': 34.0089, 'lng': 71.5456},  # GT Road
        {'lat': 34.0023, 'lng': 71.5678},  # Further along GT Road
        {'lat': 33.9889, 'lng': 71.4756},  # Ring Road
    ]
    
    route_sim = RouteSimulator(waypoints, speed_kmh=60)
    
    print("Route simulation:")
    for i in range(20):
        position = route_sim.get_current_position()
        print(f"Step {i+1}: Lat={position['latitude']}, Lng={position['longitude']}")
        route_sim.move(1.0)
        time.sleep(0.5)

if __name__ == "__main__":
    test_gps_simulator()
    test_route_simulator() 