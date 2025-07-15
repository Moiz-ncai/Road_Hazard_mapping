# Road Hazard Detection & Mapping System - Development Prompt

## Project Overview
Build a comprehensive road hazard detection and mapping system that combines dash cam video processing with GPS logging to create a real-time hazard map similar to Google Maps traffic visualization. The system will eventually use a YOLO model for hazard detection but should be built with dummy data for now.

## Core Components to Develop

### 1. Backend API System
**Framework**: Use Flask/FastAPI (Python) or Express.js (Node.js)

**Required Endpoints**:
- `POST /api/hazards` - Submit new hazard detection
- `GET /api/hazards` - Retrieve hazards by geographic bounds
- `GET /api/hazards/route` - Get hazards along a specific route
- `POST /api/speed-recommendations` - Calculate safe speeds for route segments

**Database Schema**:
```sql
hazards table:
- id (primary key)
- latitude (decimal, precision 8)
- longitude (decimal, precision 8)
- hazard_type (enum: 'pothole', 'crack', 'debris', 'construction', 'flooding')
- severity_level (enum: 'low', 'medium', 'high')
- detection_timestamp (datetime)
- confidence_score (float 0-1)
- image_path (string, optional)
- speed_limit (integer, km/h)
- recommended_speed (integer, km/h)
- verified (boolean, default false)
- road_name (string)
- area (string)
- weather_condition (string, optional)
```

### 2. Frontend Web Application
**Framework**: React.js with TypeScript

**Required Components**:
- Interactive map component using Mapbox GL JS or Google Maps API
- Real-time hazard overlay system with color-coded markers
- Hazard filtering panel (type, severity, time range)
- Route planning with hazard avoidance
- Speed recommendation display
- Admin panel for hazard verification

**Map Features**:
- Cluster hazards when zoomed out
- Color coding: Red (high), Yellow (medium), Green (low severity)
- Popup details showing hazard info and recommended speeds
- Route overlay with speed recommendations per segment

### 3. Dummy Data Generator
Create a realistic dataset for **Peshawar, Pakistan** with:
- 200+ hazard entries covering various road types around Peshawar
- Geographic clustering around major roads (GT Road, Ring Road, University Road, Jamrud Road)
- Realistic severity distributions (60% low, 30% medium, 10% high)
- Time-based patterns (more hazards during monsoon season and winter months)
- Speed limit correlation (lower speeds for higher severity hazards)

**Geographic Coverage for Peshawar**:
- Latitude range: 33.9° to 34.1° N
- Longitude range: 71.4° to 71.7° E
- Focus areas: University Town, Cantonment, Hayatabad, Board Bazaar, Saddar

**Sample Data Structure**:
```json
{
  "latitude": 34.0151,
  "longitude": 71.5249,
  "hazard_type": "pothole",
  "severity_level": "medium",
  "detection_timestamp": "2024-01-15T10:30:00Z",
  "confidence_score": 0.85,
  "speed_limit": 50,
  "recommended_speed": 35,
  "road_name": "University Road",
  "area": "University Town"
}
```

### 4. Speed Recommendation Algorithm
Implement logic that:
- Calculates safe approach speeds based on hazard severity
- Considers current speed limit and road conditions
- Provides gradual speed reduction recommendations
- Accounts for multiple hazards in proximity

**Speed Reduction Formula (adjusted for Pakistani road conditions)**:
- High severity: 40-60% of speed limit
- Medium severity: 70-80% of speed limit  
- Low severity: 85-95% of speed limit

**Common Peshawar Speed Limits**:
- Main roads (GT Road, Ring Road): 80 km/h
- City roads (University Road, Jamrud Road): 60 km/h
- Residential areas: 40 km/h
- Market areas: 30 km/h

### 5. GPS Integration Module
**Mock GPS Data Structure for Peshawar**:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "latitude": 34.0151,
  "longitude": 71.5249,
  "speed": 45,
  "heading": 180,
  "accuracy": 5,
  "road_name": "University Road"
}
```

**Features**:
- Simulate real-time GPS tracking
- Calculate distance to upcoming hazards
- Trigger speed recommendations based on proximity

### 6. Future YOLO Integration Preparation
**Model Interface Structure**:
```python
class HazardDetector:
    def detect_hazards(self, frame):
        # Returns: [(x, y, w, h, class, confidence, severity)]
        pass
    
    def process_video_stream(self, video_path, gps_data):
        # Process dash cam video with GPS sync
        pass
```

**Image Processing Pipeline**:
- Frame extraction from dash cam video
- GPS timestamp synchronization
- Hazard detection placeholder
- Severity classification logic

## Technical Requirements

### Database
- Use PostgreSQL with PostGIS extension for geospatial queries
- Implement spatial indexing for efficient location-based searches
- Add data retention policies for old hazard records

### API Features
- RESTful design with proper HTTP status codes
- Input validation and sanitization
- Rate limiting to prevent abuse
- Swagger/OpenAPI documentation
- CORS configuration for frontend integration

### Frontend Requirements
- Responsive design (mobile-friendly)
- Real-time updates using WebSockets
- Offline capability with service workers
- Progressive Web App (PWA) features
- Accessibility compliance (WCAG 2.1)

### Performance Considerations
- Implement caching for frequently accessed hazard data
- Use map clustering for performance with large datasets
- Optimize database queries with proper indexing
- Implement pagination for hazard lists

## File Structure
```
road-hazard-system/
├── backend/
│   ├── app.py (main API server)
│   ├── models/ (database models)
│   ├── routes/ (API endpoints)
│   ├── utils/ (helper functions)
│   └── data/ (dummy data generator)
├── frontend/
│   ├── src/
│   │   ├── components/ (React components)
│   │   ├── services/ (API calls)
│   │   ├── utils/ (helper functions)
│   │   └── types/ (TypeScript definitions)
│   └── public/
└── docs/ (API documentation)
```

## Testing Requirements
- Unit tests for backend API endpoints
- Integration tests for database operations
- Frontend component testing with Jest/React Testing Library
- End-to-end testing with Cypress
- Performance testing for map rendering

## Deployment Considerations
- Docker containerization for easy deployment
- Environment configuration management
- SSL/HTTPS setup for production
- Database migration scripts
- Monitoring and logging setup

## Phase 1 Deliverables (Current Sprint)
1. Working backend API with dummy data
2. Interactive web map showing hazard locations
3. Basic speed recommendation system
4. Hazard filtering and search functionality
5. Responsive UI design
6. Complete documentation

## Future Integration Points
- YOLO model API integration endpoint
- Real-time video processing pipeline
- Mobile app development (React Native)
- Advanced analytics dashboard
- Integration with existing navigation systems

Please build this system incrementally, starting with the core backend API and basic frontend map visualization, then progressively adding features. Ensure all code is well-documented and follows best practices for the chosen technologies.