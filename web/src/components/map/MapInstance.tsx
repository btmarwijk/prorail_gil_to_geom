import React, { useState } from 'react';
import { MapContainer, ZoomControl } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

import { TileLayers } from './layers/TileLayers';
import { FeatureLayers } from './layers/FeatureLayers';
import { Legend } from './controls/Legend';
import { groepColors } from './utils/styleUtils';

const MapInstance: React.FC = () => {
  const [activeGroups, setActiveGroups] = useState<string[]>(Object.keys(groepColors));
  const defaultCenter: [number, number] = [52.1326, 5.2913]; // Netherlands
  const defaultZoom = 9;
  const _maxZoom = 22;

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        zoomControl={false} // Disable default to reposition it
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
        preferCanvas={false}
        maxZoom={_maxZoom}
      >
        {/* 1. Basemaps */}
        <TileLayers />

        {/* 2. Data Layers */}
        <FeatureLayers activeGroups={activeGroups}/>

        {/* 3. Controls & Overlays */}
        <ZoomControl position="bottomright" />
        <Legend onVisibilityChange={setActiveGroups}/>
      </MapContainer>
    </div>
  );
};

export default MapInstance;