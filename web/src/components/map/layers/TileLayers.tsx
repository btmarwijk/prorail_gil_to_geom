import { LayersControl, TileLayer, WMSTileLayer } from "react-leaflet";

// components/map/layers/TileLayers.tsx
export const TileLayers: React.FC = () => (
  <LayersControl position="topright">
    <LayersControl.BaseLayer checked name="Standard">
        <TileLayer
            url="https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            maxZoom={22}
            maxNativeZoom={22}
        />
    </LayersControl.BaseLayer>
    <LayersControl.BaseLayer name="PDOK Luchtfoto (NL)">
      <WMSTileLayer
        url="https://service.pdok.nl/hwh/luchtfotorgb/wms/v1_0"
        layers="Actueel_ortho25"
        format="image/jpeg"
        transparent={true}
        version="1.3.0"
        attribution='&copy; <a href="https://www.pdok.nl/">PDOK</a>'
        maxZoom={22}
        maxNativeZoom={22}
      />
    </LayersControl.BaseLayer>
    <LayersControl.BaseLayer name="Satellite">
      <TileLayer 
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        maxZoom={22} 
        maxNativeZoom={22}
        />
    </LayersControl.BaseLayer>
  </LayersControl>
);