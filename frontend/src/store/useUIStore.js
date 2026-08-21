import { create } from 'zustand'

export const useUIStore = create((set) => ({
  isSidebarOpen: true,
  activeModal: null,

  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  openModal: (modalName) => set({ activeModal: modalName }),
  closeModal: () => set({ activeModal: null }),
}))
