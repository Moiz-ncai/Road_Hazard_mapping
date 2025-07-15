export interface Hazard {
  id: number;
  latitude: number;
  longitude: number;
  hazard_type: 'pothole' | 'crack' | 'debris' | 'construction' | 'flooding';
  severity_level: 'low' | 'medium' | 'high';
  detection_timestamp: string;
  confidence_score: number;
  image_path?: string;
  speed_limit: number;
  recommended_speed: number;
  verified: boolean;
  road_name: string;
  area: string;
  weather_condition?: string;
}

export interface GPSPosition {
  timestamp: string;
  latitude: number;
  longitude: number;
  speed: number;
  heading: number;
  accuracy: number;
  altitude?: number;
  road_name?: string;
}

export interface SpeedRecommendation {
  waypoint_index: number;
  location: {
    lat: number;
    lng: number;
  };
  speed_limit: number;
  recommended_speed: number;
  speed_reduction: number;
  hazards_count: number;
  hazards: HazardDetail[];
}

export interface HazardDetail {
  id: number;
  type: string;
  severity: string;
  distance_km: number;
  road_name: string;
  recommended_speed?: number;
}

export interface RouteAnalysis {
  total_waypoints: number;
  total_hazards: number;
  average_speed_reduction: number;
  safety_level: 'safe' | 'low_risk' | 'moderate_risk' | 'high_risk';
  hazard_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  most_dangerous_segment?: SpeedRecommendation;
  estimated_extra_time_minutes: number;
}

export interface MapBounds {
  north: number;
  south: number;
  east: number;
  west: number;
}

export interface HazardFilters {
  hazard_type?: string;
  severity_level?: string;
  hours_back?: number;
  verified_only?: boolean;
}

export interface RouteWaypoint {
  lat: number;
  lng: number;
  speed_limit?: number;
}

export interface MapViewState {
  longitude: number;
  latitude: number;
  zoom: number;
  bearing?: number;
  pitch?: number;
}

export interface HazardCluster {
  id: string;
  coordinates: [number, number];
  point_count: number;
  point_count_abbreviated: string;
  cluster: true;
}

export interface HazardMarker {
  id: number;
  coordinates: [number, number];
  properties: Hazard;
  cluster: false;
}

export type MapFeature = HazardCluster | HazardMarker;

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface HazardResponse {
  hazards: Hazard[];
  count: number;
}

export interface SpeedRecommendationResponse {
  recommendations: SpeedRecommendation[];
  search_radius_km: number;
  total_waypoints: number;
}

export interface RouteAnalysisResponse {
  route_analysis: RouteAnalysis;
  detailed_recommendations: SpeedRecommendation[];
}

export interface LocationSpeedResponse {
  location: { lat: number; lng: number };
  speed_limit: number;
  recommended_speed: number;
  speed_reduction: number;
  hazards_count: number;
  hazards: HazardDetail[];
  safety_status: 'safe' | 'caution' | 'danger';
}

export interface CreateHazardRequest {
  latitude: number;
  longitude: number;
  hazard_type: string;
  severity_level: string;
  speed_limit: number;
  recommended_speed: number;
  road_name: string;
  area: string;
  confidence_score?: number;
  weather_condition?: string;
} 