import React, { useCallback, useEffect, useRef, useState } from 'react';
import Map, { Marker, Popup, NavigationControl, GeolocateControl } from 'react-map-gl';
import { useQuery } from 'react-query';
import styled from 'styled-components';
import { hazardApi } from '../services/api';
import { Hazard, MapBounds, MapViewState } from '../types';
import HazardPopup from './HazardPopup';

const MapContainer = styled.div`
  position: relative;
  width: 100%;
  height: 100%;
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ErrorMessage = styled.div`
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  background: #f8d7da;
  color: #721c24;
  padding: 12px 16px;
  border-radius: 4px;
  border: 1px solid #f5c6cb;
  z-index: 1000;
`;

const MapStats = styled.div`
  position: absolute;
  top: 20px;
  right: 20px;
  background: white;
  padding: 12px 16px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  font-size: 14px;
`;

const HazardMarker = styled.div<{ $severity: 'low' | 'medium' | 'high' }>`
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid white;
  cursor: pointer;
  transition: transform 0.2s ease;
  background-color: ${props => {
    switch (props.$severity) {
      case 'high': return '#e74c3c';
      case 'medium': return '#f39c12';
      case 'low': return '#27ae60';
      default: return '#95a5a6';
    }
  }};
  
  &:hover {
    transform: scale(1.2);
  }
`;

// Default map configuration for Peshawar
const PESHAWAR_CENTER = {
  latitude: 34.0151,
  longitude: 71.5249,
  zoom: 12
};

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || 'pk.eyJ1IjoidGVzdCIsImEiOiJjbGJwdGZyYmswM3JtM29wNzJqZmF3YWpzIn0.TEST_TOKEN';

const MapView: React.FC = () => {
  const [viewState, setViewState] = useState<MapViewState>(PESHAWAR_CENTER);
  const [selectedHazard, setSelectedHazard] = useState<Hazard | null>(null);
  const [mapBounds, setMapBounds] = useState<MapBounds | null>(null);
  const mapRef = useRef<any>(null);

  // Calculate map bounds from current view
  const calculateBounds = useCallback(() => {
    if (!mapRef.current) return null;
    
    const map = mapRef.current.getMap();
    const bounds = map.getBounds();
    
    return {
      north: bounds.getNorth(),
      south: bounds.getSouth(),
      east: bounds.getEast(),
      west: bounds.getWest()
    };
  }, []);

  // Fetch hazards based on current map bounds
  const { data: hazardsData, isLoading, error, refetch } = useQuery(
    ['hazards', mapBounds],
    () => hazardApi.getHazards(mapBounds || undefined),
    {
      enabled: !!mapBounds,
      refetchOnWindowFocus: false,
      staleTime: 30000, // 30 seconds
    }
  );

  // Update bounds when map moves
  const handleMapMove = useCallback(() => {
    const newBounds = calculateBounds();
    if (newBounds) {
      setMapBounds(newBounds);
    }
  }, [calculateBounds]);

  // Initialize bounds when map loads
  const handleMapLoad = useCallback(() => {
    handleMapMove();
  }, [handleMapMove]);

  // Handle hazard marker click
  const handleHazardClick = useCallback((hazard: Hazard) => {
    setSelectedHazard(hazard);
  }, []);

  // Close popup
  const handleClosePopup = useCallback(() => {
    setSelectedHazard(null);
  }, []);

  // Get severity color for stats
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return '#e74c3c';
      case 'medium': return '#f39c12';
      case 'low': return '#27ae60';
      default: return '#95a5a6';
    }
  };

  // Calculate severity statistics
  const severityStats = hazardsData?.hazards.reduce((acc, hazard) => {
    acc[hazard.severity_level] = (acc[hazard.severity_level] || 0) + 1;
    return acc;
  }, {} as Record<string, number>) || {};

  return (
    <MapContainer>
      <Map
        {...viewState}
        ref={mapRef}
        onMove={evt => setViewState(evt.viewState)}
        onMoveEnd={handleMapMove}
        onLoad={handleMapLoad}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/streets-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
        attributionControl={false}
      >
        {/* Navigation controls */}
        <NavigationControl position="bottom-right" />
        <GeolocateControl
          position="bottom-right"
          trackUserLocation={true}
          showAccuracyCircle={false}
        />

        {/* Hazard markers */}
        {hazardsData?.hazards.map((hazard) => (
          <Marker
            key={hazard.id}
            latitude={hazard.latitude}
            longitude={hazard.longitude}
            anchor="center"
            onClick={() => handleHazardClick(hazard)}
          >
            <HazardMarker $severity={hazard.severity_level} />
          </Marker>
        ))}

        {/* Hazard popup */}
        {selectedHazard && (
          <Popup
            latitude={selectedHazard.latitude}
            longitude={selectedHazard.longitude}
            anchor="bottom"
            onClose={handleClosePopup}
            closeButton={true}
            closeOnClick={false}
          >
            <HazardPopup hazard={selectedHazard} />
          </Popup>
        )}
      </Map>

      {/* Loading overlay */}
      {isLoading && (
        <LoadingOverlay>
          <div className="loading-spinner" />
        </LoadingOverlay>
      )}

      {/* Error message */}
      {error && (
        <ErrorMessage>
          Failed to load hazards. Please try again.
        </ErrorMessage>
      )}

      {/* Map statistics */}
      {hazardsData && (
        <MapStats>
          <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
            Hazards: {hazardsData.count}
          </div>
          {Object.entries(severityStats).map(([severity, count]) => (
            <div key={severity} style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
              <div
                style={{
                  width: '12px',
                  height: '12px',
                  borderRadius: '50%',
                  backgroundColor: getSeverityColor(severity),
                  marginRight: '8px'
                }}
              />
              <span style={{ textTransform: 'capitalize' }}>{severity}: {count}</span>
            </div>
          ))}
        </MapStats>
      )}
    </MapContainer>
  );
};

export default MapView; 