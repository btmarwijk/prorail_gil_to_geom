import React, { useEffect, useState, useCallback, useRef } from 'react';
import { GeoJSON, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import { getGroepStyle } from "../utils/styleUtils";

const MIN_ZOOM_LEVEL = 11;

interface FeatureLayersProps {
  activeGroups: string[];
}

export const FeatureLayers: React.FC<FeatureLayersProps> = ({ activeGroups }) => {
  const [data, setData] = useState<any>(null);
  const [currentZoom, setCurrentZoom] = useState<number>(0);
  const [renderKey, setRenderKey] = useState<number>(Date.now());
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const fetchBboxData = useCallback((map: L.Map) => {
    if (map.getZoom() < MIN_ZOOM_LEVEL) {
      setData(null);
      return;
    }

    const bounds = map.getBounds();
    const bbox = [
      bounds.getWest(),
      bounds.getSouth(),
      bounds.getEast(),
      bounds.getNorth()
    ].join(',');

    const wfsUrl = "/geoserver/kabelsleidingen/ows?" + 
                   "service=WFS&version=1.1.0&request=GetFeature&" +
                   "typeName=kabelsleidingen:spoorkabel&" +
                   "outputFormat=application/json&" +
                   "srsName=EPSG:4326&" +
                   `bbox=${bbox},EPSG:4326`;

    fetch(wfsUrl)
      .then(res => res.json())
      .then(json => {
        if (json.features) {
          setData(json);
        }
      })
      .catch(err => console.error("WFS BBOX Error:", err));
  }, []);

    const map = useMapEvents({
        zoomend: () => {
        // 1. Clear any existing timer (prevents firing mid-zoom)
        if (timerRef.current) clearTimeout(timerRef.current);

        // 2. Start a new 500ms countdown
        timerRef.current = setTimeout(() => {
            const newZoom = map.getZoom();
            
            // 3. Update state to trigger the fetch and re-render
            setCurrentZoom(newZoom);
            setRenderKey(Date.now()); // Update the key
            fetchBboxData(map);
        }, 500); // Your 500ms requirement
        },
        moveend: () => {
            // You likely want to debounce moveend the same way
            if (timerRef.current) clearTimeout(timerRef.current);
            timerRef.current = setTimeout(() => {
                fetchBboxData(map);
                setRenderKey(Date.now());
            }, 500);
        }
    });

  useEffect(() => {
    fetchBboxData(map);
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [fetchBboxData, map]);

  // --- LOGIC CHECKS START HERE ---

  // 1. Guard against null data immediately
  if (!data || !data.features) {
    return null;
  }

  // 2. Perform filtering only after we know data exists
  const filteredFeatures = data.features.filter((f: any) => 
    activeGroups.includes(f.properties?.groep)
  );

  // 3. Return null if no features match the current filter
  if (filteredFeatures.length === 0) {
    return null;
  }

  const filteredData = { ...data, features: filteredFeatures };
  if (!data || filteredFeatures.length === 0) return null;

    return (
    <GeoJSON
        key={`${renderKey}-${activeGroups.join(',')}`} 
        data={filteredData} 
        style={getGroepStyle}
        onEachFeature={(feature, layer) => {
        // Create a nice HTML template using the feature's properties
        const { kabelnummer, kabelnaam, kabeltype, groep, sub_groep, van, naar } = feature.properties;
        
        const popupContent = `
            <div style="min-width: 150px; font-family: sans-serif;">
            <strong style="color: #2c3e50;">Kabel Details</strong><br />
            <hr style="border: 0; border-top: 1px solid #eee; margin: 8px 0;" />
            <table style="width: 100%; font-size: 12px;">
                <tr><td><strong>Kabelnummer:</strong></td><td>${kabelnummer || 'N/B'}</td></tr>
                <tr><td><strong>Kabelnaam:</strong></td><td>${kabelnaam || 'N/B'}</td></tr>
                <tr><td><strong>Kabeltype:</strong></td><td>${kabeltype || 'N/B'}</td></tr>
                <tr><td><strong>Groep:</strong></td><td>${groep || 'N/B'}</td></tr>
                <tr><td><strong>Subgroep:</strong></td><td>${sub_groep || 'N/B'}</td></tr>
                <tr><td><strong>Van:</strong></td><td>${van || 'N/B'}</td></tr>
                <tr><td><strong>Naar:</strong></td><td>${naar || 'N/B'}</td></tr>
            </table>
            </div>
        `;

        layer.bindPopup(popupContent);

        if (kabelnaam) {
            layer.bindTooltip(kabelnaam, {
                sticky: true,
                direction: 'auto',
                className: 'kabel-label'
            });
    }
        }}

        
    />
    );
}