import { create } from 'zustand'
import { chatApi } from '../api/chatApi.js'

export const useChatStore = create((set, get) => ({
  sessionId: null,
  messages: [],
  isSending: false,

  sendMessage: async (message) => {
    set({ isSending: true, messages: [...get().messages, { role: 'user', content: message }] })
    try {
      const { data } = await chatApi.sendMessage({ session_id: get().sessionId, message })
      set({
        sessionId: data.session_id,
        messages: [...get().messages, { role: 'assistant', content: data.reply }],
        isSending: false,
      })
    } catch (err) {
      set({ isSending: false })
      throw err
    }
  },

  resetSession: () => set({ sessionId: null, messages: [] }),
}))
