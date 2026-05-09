import React, { Suspense, lazy } from 'react';
import { Box, CircularProgress, Typography, Paper } from '@mui/material';

// Lazy load the MapInstance
const MapInstance = lazy(() => import('../../components/map/MapInstance'));

const MapPage: React.FC = () => {
  return (
    <Box 
      component="section" 
      sx={{ 
        position: 'relative',
        height: '83%', // Fills the parent container's height
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}
    >
      {/* Optional: Local Map Toolbar for quick actions */}
      <Paper 
        elevation={2} 
        sx={{ 
          position: 'absolute', 
          top: 16, 
          left: 16, 
          zIndex: 1000, // Above Leaflet
          p: 1,
          display: 'flex',
          gap: 1,
          backgroundColor: 'rgba(255, 255, 255, 0.9)'
        }}
      >
        <Typography variant="caption" fontWeight="bold" sx={{ px: 1 }}>
          VIEW: STANDARD
        </Typography>
      </Paper>

      <Suspense fallback={
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          justifyContent: 'center', 
          flexGrow: 1 
        }}>
          <CircularProgress size={40} />
          <Typography variant="body2" sx={{ mt: 2, color: 'text.secondary' }}>
            Loading Map View...
          </Typography>
        </Box>
      }>
        {/* The Actual Leaflet Map */}
        <MapInstance />
      </Suspense>
    </Box>
  );
};

export default MapPage;