import React from 'react';
import { Box, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar, AppBar, Typography } from '@mui/material';
import { Link, Outlet, useLocation } from 'react-router-dom';
import MapIcon from '@mui/icons-material/Map';
import CableIcon from '@mui/icons-material/Cable';
import UploadIcon from '@mui/icons-material/Upload';
import PersonIcon from '@mui/icons-material/Person';
import type { MenuItem } from '../../types/navigation';

const drawerWidth = 240;

const menuItems: MenuItem[] = [
  { text: 'Map', path: '/map', icon: <MapIcon /> },
  { text: 'Spoorkabels', path: '/spoorkabels', icon: <CableIcon /> },
  { text: 'Upload', path: '/upload', icon: <UploadIcon /> },
  { text: 'User Profile', path: '/user', icon: <PersonIcon /> },
];

interface SidebarLayoutProps {}

const SidebarLayout: React.FC<SidebarLayoutProps> = () => {
  const location = useLocation();

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Project Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                {/* 
                  Note: In TS, we use the component prop with the Link from react-router-dom.
                  The 'to' prop is passed through to the Link component.
                */}
                <ListItemButton 
                  component={Link} 
                  to={item.path}
                  selected={location.pathname === item.path}
                >
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Outlet /> 
      </Box>
    </Box>
  );
};

export default SidebarLayout;