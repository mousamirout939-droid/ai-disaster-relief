import axiosClient from './axiosClient.js'

export const aidRequestApi = {
  create: (payload) => axiosClient.post('/aid-requests', payload),
  update: (id, payload) => axiosClient.patch(`/aid-requests/${id}`, payload),
}
