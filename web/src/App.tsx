import React from 'react';
import SidebarLayout from './components/common/SidebarLayout';

const App: React.FC = () => {
  // We don't pass <Outlet /> here because SidebarLayout already contains it!
  return <SidebarLayout />;
};

export default App;