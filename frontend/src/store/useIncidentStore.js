import { create } from 'zustand'
import { incidentApi } from '../api/incidentApi.js'

export const useIncidentStore = create((set, get) => ({
  incidents: [],
  isLoading: false,
  error: null,

  fetchNearby: async (longitude, latitude, radiusKm = 25) => {
    set({ isLoading: true, error: null })
    try {
      const { data } = await incidentApi.getNearby({ longitude, latitude, radius_km: radiusKm })
      set({ incidents: data, isLoading: false })
    } catch (err) {
      set({ error: err.message, isLoading: false })
    }
  },

  submitReport: async (formData) => {
    const { data } = await incidentApi.report(formData)
    set({ incidents: [data, ...get().incidents] })
    return data
  },

  verifyIncident: async (incidentId, approve, notes) => {
    const { data } = await incidentApi.verify(incidentId, { approve, notes })
    set({
      incidents: get().incidents.map((i) => (i.id === incidentId ? data : i)),
    })
    return data
  },
}))
