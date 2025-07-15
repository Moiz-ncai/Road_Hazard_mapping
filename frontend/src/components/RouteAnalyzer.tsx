import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: #f8f9fa;
`;

const Card = styled.div`
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
`;

const Title = styled.h1`
  margin: 0 0 16px 0;
  font-size: 24px;
  font-weight: 600;
  color: #333;
`;

const Description = styled.p`
  margin: 0 0 24px 0;
  font-size: 16px;
  color: #666;
  line-height: 1.6;
`;

const ComingSoon = styled.div`
  display: inline-block;
  padding: 8px 16px;
  background: #3498db;
  color: white;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
`;

const RouteAnalyzer: React.FC = () => {
  return (
    <Container>
      <Card>
        <Title>🛣️ Route Analyzer</Title>
        <Description>
          Plan your routes with real-time hazard analysis and speed recommendations. 
          Get detailed safety reports and optimal path suggestions.
        </Description>
        <ComingSoon>Coming Soon</ComingSoon>
      </Card>
    </Container>
  );
};

export default RouteAnalyzer; 