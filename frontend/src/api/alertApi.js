import axiosClient from './axiosClient.js'

export const alertApi = {
  broadcast: (payload) => axiosClient.post('/alerts/broadcast', payload),
  getNearby: (params) => axiosClient.get('/alerts/nearby', { params }),
}
