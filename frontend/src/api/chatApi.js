import axiosClient from './axiosClient.js'

export const chatApi = {
  sendMessage: (payload) => axiosClient.post('/chat/message', payload),
}
