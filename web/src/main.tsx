import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import MapPage from './pages/map/MapPage'
import UploadPage from './pages/upload/UploadPage'

const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, // App now acts as the layout wrapper
    children: [
      {
        // Redirects "/" to "/map"
        index: true,
        element: <Navigate to="/map" replace />,
      },
      {
        path: "map/:spoorkabel_id",
        element: <MapPage />,
      },
      {
        path: "upload",
        element: <UploadPage />
      }
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router}/>
    </QueryClientProvider>
  </React.StrictMode>,
)