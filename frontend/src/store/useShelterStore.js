import { create } from 'zustand'
import { shelterApi } from '../api/shelterApi.js'

export const useShelterStore = create((set, get) => ({
  shelters: [],
  selectedShelter: null,
  isLoading: false,

  fetchNearby: async (longitude, latitude, radiusKm = 25, shelterType = null) => {
    set({ isLoading: true })
    const { data } = await shelterApi.getNearby({
      longitude,
      latitude,
      radius_km: radiusKm,
      shelter_type: shelterType || undefined,
    })
    set({ shelters: data, isLoading: false })
  },

  selectShelter: (shelter) => set({ selectedShelter: shelter }),

  updateShelter: async (id, payload) => {
    const { data } = await shelterApi.update(id, payload)
    set({ shelters: get().shelters.map((s) => (s.id === id ? data : s)) })
    return data
  },
}))
