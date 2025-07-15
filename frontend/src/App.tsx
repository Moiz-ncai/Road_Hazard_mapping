import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import styled from 'styled-components';
import MapView from './components/MapView';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import RouteAnalyzer from './components/RouteAnalyzer';
import AdminPanel from './components/AdminPanel';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background-color: #f5f5f5;
`;

const MainContent = styled.div`
  display: flex;
  flex: 1;
  overflow: hidden;
`;

const MapContainer = styled.div`
  flex: 1;
  position: relative;
`;

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AppContainer>
          <Header />
          <MainContent>
            <Routes>
              <Route path="/" element={
                <>
                  <Sidebar />
                  <MapContainer>
                    <MapView />
                  </MapContainer>
                </>
              } />
              <Route path="/route-analyzer" element={<RouteAnalyzer />} />
              <Route path="/admin" element={<AdminPanel />} />
            </Routes>
          </MainContent>
        </AppContainer>
      </Router>
    </QueryClientProvider>
  );
}

export default App; 