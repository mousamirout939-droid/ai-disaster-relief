import axiosClient from './axiosClient.js'

export const shelterApi = {
  getNearby: (params) => axiosClient.get('/shelters/nearby', { params }),
  getById: (id) => axiosClient.get(`/shelters/${id}`),
  create: (payload) => axiosClient.post('/shelters', payload),
  update: (id, payload) => axiosClient.patch(`/shelters/${id}`, payload),
  remove: (id) => axiosClient.delete(`/shelters/${id}`),
}
