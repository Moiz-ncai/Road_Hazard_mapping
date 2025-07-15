# Road Hazard Detection & Mapping System

A comprehensive web application for detecting, mapping, and analyzing road hazards using dash cam footage and GPS data. The system provides real-time hazard visualization, speed recommendations, and route safety analysis.

## 🚀 Features

### Core Functionality
- **Real-time Hazard Mapping**: Interactive map displaying detected road hazards with severity-based color coding
- **Speed Recommendations**: Dynamic speed suggestions based on hazard proximity and severity
- **Route Analysis**: Safety assessment for planned routes with detailed hazard reports
- **GPS Integration**: Mock GPS tracking for testing and development
- **Hazard Classification**: Support for potholes, cracks, debris, construction, and flooding

### Technical Highlights
- **Geospatial Database**: PostgreSQL with PostGIS for efficient location-based queries
- **RESTful API**: Flask-based backend with comprehensive hazard management endpoints
- **Interactive Frontend**: React with TypeScript and Mapbox GL JS for smooth map interactions
- **Real-time Updates**: WebSocket support for live hazard updates
- **Mobile-Responsive**: PWA-ready design for cross-platform compatibility

## 📁 Project Structure

```
road-hazard-system/
├── backend/                 # Flask API server
│   ├── app.py              # Main application entry point
│   ├── models/             # Database models
│   │   └── hazard.py       # Hazard data model
│   ├── routes/             # API endpoints
│   │   ├── hazard_routes.py # Hazard CRUD operations
│   │   └── speed_routes.py  # Speed recommendation logic
│   ├── utils/              # Utility functions
│   │   └── gps_simulator.py # GPS simulation for testing
│   ├── data/               # Data management
│   │   └── dummy_data_generator.py # Peshawar-specific dummy data
│   └── requirements.txt    # Python dependencies
├── frontend/               # React TypeScript app
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── MapView.tsx # Main map component
│   │   │   ├── HazardPopup.tsx # Hazard detail popup
│   │   │   ├── Sidebar.tsx # Filter controls
│   │   │   └── Header.tsx  # Navigation header
│   │   ├── services/       # API integration
│   │   │   └── api.ts      # Backend API calls
│   │   ├── types/          # TypeScript definitions
│   │   │   └── index.ts    # Type definitions
│   │   └── App.tsx         # Main app component
│   ├── package.json        # Node dependencies
│   └── tsconfig.json       # TypeScript configuration
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ with PostGIS extension
- Mapbox account and API token

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd road-hazard-system
   ```

2. **Set up Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE road_hazards;
   CREATE EXTENSION postgis;
   ```

5. **Configure environment variables**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/road_hazards
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   ```

6. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Generate dummy data**
   ```bash
   cd data
   python dummy_data_generator.py
   ```

8. **Start the Flask server**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables**
   Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_URL=http://localhost:5000/api
   REACT_APP_MAPBOX_TOKEN=your-mapbox-token-here
   ```

3. **Start the React development server**
   ```bash
   npm start
   ```
   The app will be available at `http://localhost:3000`

## 🗺️ API Documentation

### Hazard Endpoints

#### GET /api/hazards
Retrieve hazards with optional filtering and geographic bounds.

**Query Parameters:**
- `north`, `south`, `east`, `west`: Geographic bounds
- `hazard_type`: Filter by hazard type (pothole, crack, debris, construction, flooding)
- `severity_level`: Filter by severity (low, medium, high)
- `hours_back`: Time range in hours (default: 24)
- `verified_only`: Boolean to show only verified hazards

**Response:**
```json
{
  "hazards": [
    {
      "id": 1,
      "latitude": 34.0151,
      "longitude": 71.5249,
      "hazard_type": "pothole",
      "severity_level": "medium",
      "detection_timestamp": "2024-01-15T10:30:00Z",
      "confidence_score": 0.85,
      "speed_limit": 50,
      "recommended_speed": 35,
      "road_name": "University Road",
      "area": "University Town",
      "verified": false
    }
  ],
  "count": 1
}
```

#### POST /api/hazards
Create a new hazard detection.

**Request Body:**
```json
{
  "latitude": 34.0151,
  "longitude": 71.5249,
  "hazard_type": "pothole",
  "severity_level": "medium",
  "speed_limit": 50,
  "recommended_speed": 35,
  "road_name": "University Road",
  "area": "University Town",
  "confidence_score": 0.85
}
```

### Speed Recommendation Endpoints

#### POST /api/speed-recommendations
Get speed recommendations for a route.

**Request Body:**
```json
{
  "waypoints": [
    {"lat": 34.0151, "lng": 71.5249, "speed_limit": 50},
    {"lat": 34.0089, "lng": 71.5456, "speed_limit": 60}
  ],
  "search_radius_km": 1.0
}
```

#### GET /api/speed-recommendations/location
Get speed recommendation for a specific location.

**Query Parameters:**
- `lat`: Latitude
- `lng`: Longitude
- `speed_limit`: Current speed limit (default: 50)
- `radius_km`: Search radius in kilometers (default: 1.0)

## 🎯 Usage Examples

### Basic Map Interaction
1. Open the application in your browser
2. The map will center on Peshawar, Pakistan
3. Hazards are displayed as colored markers:
   - 🔴 Red: High severity
   - 🟡 Yellow: Medium severity
   - 🟢 Green: Low severity
4. Click on any hazard marker to view details

### Filtering Hazards
1. Use the sidebar to filter hazards by:
   - Type (pothole, crack, debris, construction, flooding)
   - Severity level (low, medium, high)
   - Time period (last N hours)
   - Verification status
2. Filters are applied immediately to the map

### Speed Recommendations
1. The system automatically calculates safe approach speeds
2. Recommendations consider:
   - Hazard severity and proximity
   - Current speed limit
   - Multiple hazards in the area
3. Speed reductions are displayed in hazard popups

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### Database Migrations
```bash
cd backend
flask db migrate -m "Description of changes"
flask db upgrade
```

### Adding New Hazard Types
1. Update the `HazardType` enum in `backend/models/hazard.py`
2. Add the new type to the frontend types in `frontend/src/types/index.ts`
3. Update the dummy data generator to include the new type
4. Run database migration

## 🌐 Deployment

### Production Configuration
1. Set environment variables for production
2. Configure PostgreSQL with proper security settings
3. Use a production WSGI server (e.g., Gunicorn)
4. Set up reverse proxy (e.g., Nginx)
5. Configure SSL/TLS certificates

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 📊 Performance Considerations

- **Database Indexing**: Spatial indexes on coordinates for fast location queries
- **API Caching**: Redis caching for frequently accessed hazard data
- **Map Clustering**: Automatic marker clustering for better performance
- **Lazy Loading**: Hazards loaded only for visible map area
- **Pagination**: Large datasets handled with efficient pagination

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Mapbox for mapping services
- PostGIS for geospatial database capabilities
- React and Flask communities for excellent documentation
- OpenStreetMap contributors for geographic data

## 🔮 Future Enhancements

### Planned Features
- **Real YOLO Integration**: Replace dummy data with actual computer vision
- **Mobile App**: React Native mobile application
- **Advanced Analytics**: Machine learning for hazard prediction
- **Social Features**: User reporting and verification system
- **Weather Integration**: Weather-based hazard correlation
- **Navigation Integration**: Direct integration with GPS navigation systems

### Technical Improvements
- **Real-time Updates**: WebSocket implementation for live hazard updates
- **Offline Support**: PWA capabilities for offline usage
- **Performance Optimization**: Advanced caching and data compression
- **Security Enhancements**: OAuth2 authentication and authorization
- **API Rate Limiting**: Prevent abuse with proper rate limiting
- **Monitoring**: Application performance monitoring and logging

## 📞 Support

For support, please create an issue in the GitHub repository or contact the development team.

---

**Note**: This system is currently configured with dummy data for development and testing purposes. For production use, integrate with actual YOLO models and real-time data sources. 