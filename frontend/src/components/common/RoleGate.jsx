import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../../store/useAuthStore.js'

/** Blocks access to nested routes unless the current user's role is in `allow`. */
export default function RoleGate({ allow = [] }) {
  const user = useAuthStore((s) => s.user)
  if (!user) return <Navigate to="/login" replace />
  if (!allow.includes(user.role)) return <Navigate to="/dashboard" replace />
  return <Outlet />
}
