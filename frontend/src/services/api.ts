import axios from 'axios';
import {
  Hazard,
  HazardResponse,
  SpeedRecommendationResponse,
  RouteAnalysisResponse,
  LocationSpeedResponse,
  CreateHazardRequest,
  HazardFilters,
  MapBounds,
  RouteWaypoint
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const hazardApi = {
  // Get hazards with filters and bounds
  getHazards: async (bounds?: MapBounds, filters?: HazardFilters): Promise<HazardResponse> => {
    const params = new URLSearchParams();
    
    if (bounds) {
      params.append('north', bounds.north.toString());
      params.append('south', bounds.south.toString());
      params.append('east', bounds.east.toString());
      params.append('west', bounds.west.toString());
    }
    
    if (filters) {
      if (filters.hazard_type) params.append('hazard_type', filters.hazard_type);
      if (filters.severity_level) params.append('severity_level', filters.severity_level);
      if (filters.hours_back) params.append('hours_back', filters.hours_back.toString());
      if (filters.verified_only) params.append('verified_only', filters.verified_only.toString());
    }
    
    const response = await api.get(`/hazards?${params.toString()}`);
    return response.data;
  },

  // Get specific hazard by ID
  getHazardById: async (id: number): Promise<Hazard> => {
    const response = await api.get(`/hazards/${id}`);
    return response.data;
  },

  // Create new hazard
  createHazard: async (hazard: CreateHazardRequest): Promise<Hazard> => {
    const response = await api.post('/hazards', hazard);
    return response.data.hazard;
  },

  // Update hazard (verify, change severity, etc.)
  updateHazard: async (id: number, updates: Partial<Hazard>): Promise<Hazard> => {
    const response = await api.put(`/hazards/${id}`, updates);
    return response.data.hazard;
  },

  // Delete hazard
  deleteHazard: async (id: number): Promise<void> => {
    await api.delete(`/hazards/${id}`);
  },

  // Get hazards along a route
  getHazardsAlongRoute: async (
    waypoints: RouteWaypoint[], 
    bufferKm: number = 0.5
  ): Promise<HazardResponse> => {
    const response = await api.post('/hazards/route', {
      waypoints,
      buffer_km: bufferKm
    });
    return response.data;
  },

  // Get nearby hazards
  getNearbyHazards: async (
    lat: number, 
    lng: number, 
    radiusKm: number = 1.0
  ): Promise<HazardResponse> => {
    const params = new URLSearchParams({
      lat: lat.toString(),
      lng: lng.toString(),
      radius_km: radiusKm.toString()
    });
    
    const response = await api.get(`/hazards/nearby?${params.toString()}`);
    return response.data;
  }
};

export const speedApi = {
  // Get speed recommendations for route
  getSpeedRecommendations: async (
    waypoints: RouteWaypoint[], 
    searchRadiusKm: number = 1.0
  ): Promise<SpeedRecommendationResponse> => {
    const response = await api.post('/speed-recommendations', {
      waypoints,
      search_radius_km: searchRadiusKm
    });
    return response.data;
  },

  // Get speed recommendation for specific location
  getLocationSpeedRecommendation: async (
    lat: number, 
    lng: number, 
    speedLimit: number = 50, 
    radiusKm: number = 1.0
  ): Promise<LocationSpeedResponse> => {
    const params = new URLSearchParams({
      lat: lat.toString(),
      lng: lng.toString(),
      speed_limit: speedLimit.toString(),
      radius_km: radiusKm.toString()
    });
    
    const response = await api.get(`/speed-recommendations/location?${params.toString()}`);
    return response.data;
  },

  // Analyze route safety
  analyzeRouteSafety: async (waypoints: RouteWaypoint[]): Promise<RouteAnalysisResponse> => {
    const response = await api.post('/speed-recommendations/route-analysis', {
      waypoints
    });
    return response.data;
  }
};

export const healthApi = {
  // Check API health
  checkHealth: async (): Promise<{ status: string; message: string }> => {
    const response = await api.get('/');
    return response.data;
  }
};

// Export the main API instance for direct use if needed
export default api; 