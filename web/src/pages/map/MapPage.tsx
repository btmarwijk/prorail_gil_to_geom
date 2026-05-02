import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Import your types
import type { SpoorkabelGeoJSON } from '../../types/spoorkabel.types'; 

// Component to auto-center the map when data loads
const RecenterMap = ({ data }: { data: SpoorkabelGeoJSON }) => {
  const map = useMap();

  useEffect(() => {
    // Adding the '?' and an extra check for safety
    if (data?.features && data.features.length > 0) {
      try {
        const geoJsonLayer = L.geoJSON(data as any);
        map.fitBounds(geoJsonLayer.getBounds(), { padding: [20, 20] });
      } catch (e) {
        console.error("Leaflet couldn't calculate bounds:", e);
      }
    }
  }, [data, map]);

  return null;
};

const MapPage: React.FC = () => {
  const { spoorkabel_id } = useParams<{ spoorkabel_id: string }>();
  const [geoData, setGeoData] = useState<SpoorkabelGeoJSON | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Using the dynamic ID from the URL
        const response = await fetch(`http://localhost:8000/api/v1/spoorkabels/spoorkabel/${spoorkabel_id}`);
        
        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        const data: SpoorkabelGeoJSON = await response.json();
        setGeoData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch map data');
      } finally {
        setLoading(false);
      }
    };

    if (spoorkabel_id) {
      fetchData();
    }
  }, [spoorkabel_id]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 10 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box sx={{ height: 'calc(100vh - 150px)', width: '100%' }}>
      <Typography variant="h5" gutterBottom>
        Spoorkabel Map: {spoorkabel_id}
      </Typography>
      
      <MapContainer 
        center={[52.1326, 5.2913]} // Default Netherlands center
        zoom={8} 
        style={{ height: '100%', width: '100%', borderRadius: '8px' }}
      >
        <TileLayer
          url="https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />
        {geoData && (
          <>
            <GeoJSON 
              data={geoData as any} 
              style={{ color: '#1976d2', weight: 5 }} 
              onEachFeature={(feature, layer) => {
                // Tooltip showing the cable name from your Spoorkabel interface
                if (feature.properties?.kabelnaam) {
                  layer.bindPopup(`<strong>${feature.properties.kabelnaam}</strong><br/>ID: ${feature.properties.id}`);
                }
              }}
            />
            <RecenterMap data={geoData} />
          </>
        )}
      </MapContainer>
    </Box>
  );
};

export default MapPage;