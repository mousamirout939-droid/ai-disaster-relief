import { create } from 'zustand'

export const useMapStore = create((set) => ({
  center: [37.7749, -122.4194], // default fallback: San Francisco
  zoom: 12,
  userLocation: null,
  activeLayers: { incidents: true, shelters: true, heatmap: false },

  setCenter: (center, zoom) => set({ center, zoom: zoom ?? 12 }),
  setUserLocation: (location) => set({ userLocation: location, center: [location.lat, location.lng] }),
  toggleLayer: (layerName) =>
    set((state) => ({ activeLayers: { ...state.activeLayers, [layerName]: !state.activeLayers[layerName] } })),
}))
