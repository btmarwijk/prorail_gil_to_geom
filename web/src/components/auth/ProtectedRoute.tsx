import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth()

  // Don't redirect while rehydrating the token from localStorage
  if (isLoading) return null

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />
}