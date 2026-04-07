import { Container, Typography, AppBar, Toolbar, Paper } from '@mui/material';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'; // CRITICAL: Don't forget this!

function App() {
  const position: [number, number] = [52.0907, 5.1214]; // Utrecht coords

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">KabelLeiding GIS Viewer</Typography>
        </Toolbar>
      </AppBar>

      <Container sx={{ mt: 4 }}>
        <Paper elevation={3} style={{ height: '500px', width: '100%' }}>
          <MapContainer center={position} zoom={13} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            />
            <Marker position={position}>
              <Popup>Utrecht: Project Center</Popup>
            </Marker>
          </MapContainer>
        </Paper>
      </Container>
    </>
  );
}

export default App;