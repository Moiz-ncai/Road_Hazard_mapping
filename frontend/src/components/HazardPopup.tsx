import React from 'react';
import styled from 'styled-components';
import { format } from 'date-fns';
import { Hazard } from '../types';

interface HazardPopupProps {
  hazard: Hazard;
}

const PopupContainer = styled.div`
  min-width: 240px;
  max-width: 280px;
`;

const HazardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
`;

const HazardTitle = styled.h3`
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  text-transform: capitalize;
`;

const SeverityBadge = styled.span<{ $severity: 'low' | 'medium' | 'high' }>`
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  background-color: ${props => {
    switch (props.$severity) {
      case 'high': return '#f8d7da';
      case 'medium': return '#fff3cd';
      case 'low': return '#d4edda';
      default: return '#f8f9fa';
    }
  }};
  color: ${props => {
    switch (props.$severity) {
      case 'high': return '#721c24';
      case 'medium': return '#856404';
      case 'low': return '#155724';
      default: return '#6c757d';
    }
  }};
`;

const InfoRow = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
`;

const InfoLabel = styled.span`
  font-weight: 500;
  color: #666;
`;

const InfoValue = styled.span`
  color: #333;
`;

const SpeedInfo = styled.div`
  background: #f8f9fa;
  padding: 8px 12px;
  border-radius: 4px;
  margin-top: 8px;
`;

const SpeedRow = styled.div`
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 4px;
`;

const SpeedReduction = styled.span<{ $reduction: number }>`
  font-weight: 600;
  color: ${props => {
    if (props.$reduction > 20) return '#e74c3c';
    if (props.$reduction > 10) return '#f39c12';
    return '#27ae60';
  }};
`;

const VerificationStatus = styled.div<{ $verified: boolean }>`
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  margin-top: 8px;
  color: ${props => props.$verified ? '#27ae60' : '#f39c12'};
`;

const LocationInfo = styled.div`
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #eee;
  font-size: 12px;
  color: #666;
`;

const HazardPopup: React.FC<HazardPopupProps> = ({ hazard }) => {
  const speedReduction = hazard.speed_limit - hazard.recommended_speed;
  const detectionTime = new Date(hazard.detection_timestamp);
  const timeAgo = format(detectionTime, 'PPp');

  const getHazardIcon = (type: string) => {
    switch (type) {
      case 'pothole': return '🕳️';
      case 'crack': return '🔧';
      case 'debris': return '🪨';
      case 'construction': return '🚧';
      case 'flooding': return '🌊';
      default: return '⚠️';
    }
  };

  return (
    <PopupContainer>
      <HazardHeader>
        <HazardTitle>
          {getHazardIcon(hazard.hazard_type)} {hazard.hazard_type}
        </HazardTitle>
        <SeverityBadge $severity={hazard.severity_level}>
          {hazard.severity_level}
        </SeverityBadge>
      </HazardHeader>

      <InfoRow>
        <InfoLabel>Road:</InfoLabel>
        <InfoValue>{hazard.road_name}</InfoValue>
      </InfoRow>

      <InfoRow>
        <InfoLabel>Area:</InfoLabel>
        <InfoValue>{hazard.area}</InfoValue>
      </InfoRow>

      <InfoRow>
        <InfoLabel>Confidence:</InfoLabel>
        <InfoValue>{Math.round(hazard.confidence_score * 100)}%</InfoValue>
      </InfoRow>

      <SpeedInfo>
        <SpeedRow>
          <InfoLabel>Speed Limit:</InfoLabel>
          <InfoValue>{hazard.speed_limit} km/h</InfoValue>
        </SpeedRow>
        <SpeedRow>
          <InfoLabel>Recommended:</InfoLabel>
          <InfoValue>{hazard.recommended_speed} km/h</InfoValue>
        </SpeedRow>
        <SpeedRow>
          <InfoLabel>Reduction:</InfoLabel>
          <SpeedReduction $reduction={speedReduction}>
            -{speedReduction} km/h
          </SpeedReduction>
        </SpeedRow>
      </SpeedInfo>

      <VerificationStatus $verified={hazard.verified}>
        {hazard.verified ? '✅' : '⏳'} 
        {hazard.verified ? 'Verified' : 'Pending verification'}
      </VerificationStatus>

      {hazard.weather_condition && (
        <InfoRow>
          <InfoLabel>Weather:</InfoLabel>
          <InfoValue>{hazard.weather_condition}</InfoValue>
        </InfoRow>
      )}

      <LocationInfo>
        <div>Detected: {timeAgo}</div>
        <div>Location: {hazard.latitude.toFixed(4)}, {hazard.longitude.toFixed(4)}</div>
      </LocationInfo>
    </PopupContainer>
  );
};

export default HazardPopup; 