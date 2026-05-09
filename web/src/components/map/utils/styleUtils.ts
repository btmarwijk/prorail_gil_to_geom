// 1. Centralized color mapping - easy to import into Legend.tsx
export const groepColors: Record<string, string> = {
  "Beveiliging":      "#e74c3c",
  "Derden":           "#cd804c",
  "Energie":          "#2ecc71",
  "Overige":          "#52fdcf",
  "Riolering":        "#58330a",
  "Telecom":          "#9b59b6",
  "Verlaten":         "#114d0a",
  "Water":            "#3498db",
  "Wisselverwarming": "#f1c40f",
};

// 2. Styling function for the Leaflet GeoJSON layer
export const getGroepStyle = (feature: any) => {
  const groep = feature.properties?.groep;

  // Lookup the color, fallback to black if the key doesn't exist
  const color = groepColors[groep] || "#000000";

  return {
    color: color,
    weight: 3,
    opacity: 1,
    lineJoin: 'round' as const,
    lineCap: 'round' as const,
  };
};