import React, { useState } from 'react';
import styled from 'styled-components';
import { HazardFilters } from '../types';

interface SidebarProps {
  onFiltersChange?: (filters: HazardFilters) => void;
}

const SidebarContainer = styled.div`
  width: 320px;
  background: white;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  height: 100%;
`;

const SidebarHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
`;

const SidebarTitle = styled.h2`
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
`;

const SidebarSubtitle = styled.p`
  margin: 0;
  font-size: 14px;
  color: #666;
`;

const FiltersSection = styled.div`
  padding: 20px;
  flex: 1;
`;

const FilterGroup = styled.div`
  margin-bottom: 20px;
`;

const FilterLabel = styled.label`
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
`;

const FilterSelect = styled.select`
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background-color: white;
  cursor: pointer;
  
  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

const FilterInput = styled.input`
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  
  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

const CheckboxContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

const CheckboxInput = styled.input`
  cursor: pointer;
`;

const FilterButton = styled.button`
  width: 100%;
  padding: 10px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  
  &:hover {
    background: #2980b9;
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }
`;

const ClearButton = styled.button`
  width: 100%;
  padding: 8px;
  background: transparent;
  color: #7f8c8d;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 8px;
  transition: all 0.2s ease;
  
  &:hover {
    color: #2c3e50;
    border-color: #95a5a6;
  }
`;

const StatsSection = styled.div`
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
`;

const StatItem = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
`;

const StatLabel = styled.span`
  color: #666;
`;

const StatValue = styled.span`
  font-weight: 500;
  color: #333;
`;

const Sidebar: React.FC<SidebarProps> = ({ onFiltersChange }) => {
  const [filters, setFilters] = useState<HazardFilters>({
    hazard_type: '',
    severity_level: '',
    hours_back: 24,
    verified_only: false
  });

  const handleFilterChange = (key: keyof HazardFilters, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFiltersChange?.(newFilters);
  };

  const clearFilters = () => {
    const clearedFilters: HazardFilters = {
      hazard_type: '',
      severity_level: '',
      hours_back: 24,
      verified_only: false
    };
    setFilters(clearedFilters);
    onFiltersChange?.(clearedFilters);
  };

  return (
    <SidebarContainer>
      <SidebarHeader>
        <SidebarTitle>Hazard Filters</SidebarTitle>
        <SidebarSubtitle>Filter hazards by type, severity, and time</SidebarSubtitle>
      </SidebarHeader>

      <FiltersSection>
        <FilterGroup>
          <FilterLabel>Hazard Type</FilterLabel>
          <FilterSelect
            value={filters.hazard_type || ''}
            onChange={(e) => handleFilterChange('hazard_type', e.target.value || undefined)}
          >
            <option value="">All Types</option>
            <option value="pothole">Pothole</option>
            <option value="crack">Crack</option>
            <option value="debris">Debris</option>
            <option value="construction">Construction</option>
            <option value="flooding">Flooding</option>
          </FilterSelect>
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Severity Level</FilterLabel>
          <FilterSelect
            value={filters.severity_level || ''}
            onChange={(e) => handleFilterChange('severity_level', e.target.value || undefined)}
          >
            <option value="">All Severities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </FilterSelect>
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Time Period (hours)</FilterLabel>
          <FilterInput
            type="number"
            min="1"
            max="168"
            value={filters.hours_back || 24}
            onChange={(e) => handleFilterChange('hours_back', parseInt(e.target.value) || 24)}
          />
        </FilterGroup>

        <FilterGroup>
          <CheckboxContainer>
            <CheckboxInput
              type="checkbox"
              checked={filters.verified_only || false}
              onChange={(e) => handleFilterChange('verified_only', e.target.checked)}
            />
            <FilterLabel style={{ marginBottom: 0 }}>Verified hazards only</FilterLabel>
          </CheckboxContainer>
        </FilterGroup>

        <ClearButton onClick={clearFilters}>
          Clear All Filters
        </ClearButton>
      </FiltersSection>

      <StatsSection>
        <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', fontWeight: '600' }}>
          Quick Stats
        </h3>
        <StatItem>
          <StatLabel>Total Hazards:</StatLabel>
          <StatValue>Loading...</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>High Severity:</StatLabel>
          <StatValue>Loading...</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Verified:</StatLabel>
          <StatValue>Loading...</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Recent (24h):</StatLabel>
          <StatValue>Loading...</StatValue>
        </StatItem>
      </StatsSection>
    </SidebarContainer>
  );
};

export default Sidebar; 