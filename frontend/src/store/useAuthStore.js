import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authApi } from '../api/authApi.js'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const { data } = await authApi.login({ email, password })
        set({ accessToken: data.access_token, refreshToken: data.refresh_token, isAuthenticated: true })
        const me = await authApi.getMe()
        set({ user: me.data })
        return me.data
      },

      register: async (payload) => {
        await authApi.register(payload)
        return get().login(payload.email, payload.password)
      },

      refreshAccessToken: async () => {
        const { refreshToken } = get()
        if (!refreshToken) throw new Error('No refresh token available')
        const { data } = await authApi.refresh(refreshToken)
        set({ accessToken: data.access_token })
        return data.access_token
      },

      logout: async () => {
        try {
          await authApi.logout()
        } catch {
          // best-effort server-side revocation; always clear local state
        }
        set({ accessToken: null, refreshToken: null, user: null, isAuthenticated: false })
      },

      hasRole: (roles) => {
        const role = get().user?.role
        return role ? roles.includes(role) : false
      },
    }),
    { name: 'disaster-relief-auth' },
  ),
)
