import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './context/AuthContext'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import App from './App'
import MapPage from './pages/map/MapPage'
import UploadPage from './pages/upload/UploadPage'
import LoginPage from './pages/login/LoginPage'
import HomePage from './pages/home/HomePage'

const queryClient = new QueryClient()

const router = createBrowserRouter([
    {
    path: '/',
    element: <HomePage />,         // unprotected, no ProtectedRoute wrapper
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/app',
    element: <ProtectedRoute />,   // guards everything below
    children: [
      {
        element: <App />,          // layout wrapper
        children: [
          { index: true, element: <Navigate to="/map" replace /> },
          { path: 'map', element: <MapPage /> },
          { path: 'upload', element: <UploadPage /> },
        ],
      },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  </React.StrictMode>,
)