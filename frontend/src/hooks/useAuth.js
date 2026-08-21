import { useAuthStore } from '../store/useAuthStore.js'

export function useAuth() {
  const { user, isAuthenticated, login, register, logout, hasRole } = useAuthStore()
  return { user, isAuthenticated, login, register, logout, hasRole }
}
