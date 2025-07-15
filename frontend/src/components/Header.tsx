import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';

const HeaderContainer = styled.header`
  background: #2c3e50;
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
`;

const HeaderContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  max-width: 1200px;
  margin: 0 auto;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: 700;
  color: white;
  text-decoration: none;
`;

const LogoIcon = styled.div`
  width: 32px;
  height: 32px;
  background: #e74c3c;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  font-size: 16px;
  font-weight: bold;
`;

const Navigation = styled.nav`
  display: flex;
  align-items: center;
  gap: 8px;
`;

const NavLink = styled(Link)<{ $active: boolean }>`
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  color: white;
  font-weight: 500;
  transition: background-color 0.2s ease;
  background-color: ${props => props.$active ? '#34495e' : 'transparent'};
  
  &:hover {
    background-color: #34495e;
  }
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
`;

const StatusDot = styled.div<{ $status: 'online' | 'offline' | 'error' }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: ${props => {
    switch (props.$status) {
      case 'online': return '#27ae60';
      case 'offline': return '#95a5a6';
      case 'error': return '#e74c3c';
      default: return '#95a5a6';
    }
  }};
`;

const Header: React.FC = () => {
  const location = useLocation();

  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo>
          <LogoIcon>🛣️</LogoIcon>
          Road Hazard Detection System
        </Logo>
        
        <Navigation>
          <NavLink to="/" $active={location.pathname === '/'}>
            Map View
          </NavLink>
          <NavLink to="/route-analyzer" $active={location.pathname === '/route-analyzer'}>
            Route Analyzer
          </NavLink>
          <NavLink to="/admin" $active={location.pathname === '/admin'}>
            Admin Panel
          </NavLink>
        </Navigation>
        
        <StatusIndicator>
          <StatusDot $status="online" />
          <span>System Online</span>
        </StatusIndicator>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header; 