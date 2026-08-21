import { create } from 'zustand'
import { alertApi } from '../api/alertApi.js'

export const useAlertStore = create((set) => ({
  activeAlerts: [],

  fetchNearby: async (longitude, latitude, radiusKm = 50) => {
    const { data } = await alertApi.getNearby({ longitude, latitude, radius_km: radiusKm })
    set({ activeAlerts: data })
  },

  pushRealtimeAlert: (alert) =>
    set((state) => ({ activeAlerts: [alert, ...state.activeAlerts] })),

  dismissAlert: (alertId) =>
    set((state) => ({ activeAlerts: state.activeAlerts.filter((a) => a.id !== alertId) })),
}))
