import { Paper, Typography, Stack, Checkbox, FormControlLabel } from '@mui/material';
import { groepColors } from '../utils/styleUtils';
import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';

interface LegendProps {
  onVisibilityChange?: (visibleGroups: string[]) => void;
}

export const Legend = ({ onVisibilityChange }: LegendProps) => {
  const legendRef = useRef<HTMLDivElement>(null);
  
  // Initialize state with all groups visible
  const [visibleGroups, setVisibleGroups] = useState<Record<string, boolean>>(
    Object.keys(groepColors).reduce((acc, key) => ({ ...acc, [key]: true }), {})
  );

  useEffect(() => {
        const container = legendRef.current;
        if (container) {
        // These prevent the map from dragging or clicking when you use the legend
        L.DomEvent.disableClickPropagation(container);
        L.DomEvent.disableScrollPropagation(container);
        }
    }, []);

  const handleToggle = (name: string) => {
    const newState = { ...visibleGroups, [name]: !visibleGroups[name] };
    setVisibleGroups(newState);
    
    // Pass the list of active strings back to the map
    if (onVisibilityChange) {
      const activeGroups = Object.keys(newState).filter(key => newState[key]);
      onVisibilityChange(activeGroups);
    }
  };

  return (
    <div className="leaflet-bottom leaflet-left" style={{ zIndex: 1000, margin: '10px' }}>
      <Paper
        ref={legendRef}
        elevation={3}
        sx={{ p: 2, pointerEvents: 'auto', backgroundColor: 'rgba(255, 255, 255, 0.9)', minWidth: '180px' }}
      >
        <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
          Lagen Filter
        </Typography>
        <Stack spacing={0.5}>
          {Object.entries(groepColors).map(([name, color]) => (
            <FormControlLabel
              key={name}
              control={
                <Checkbox
                  size="small"
                  checked={visibleGroups[name]}
                  onChange={() => handleToggle(name)}
                  sx={{
                    color: color,
                    '&.Mui-checked': { color: color },
                  }}
                />
              }
              label={
                <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                  {name}
                </Typography>
              }
            />
          ))}
        </Stack>
      </Paper>
    </div>
  );
};