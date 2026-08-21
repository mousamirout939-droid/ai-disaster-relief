import axiosClient from './axiosClient.js'

export const incidentApi = {
  report: (formData) =>
    axiosClient.post('/incidents', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  getNearby: (params) => axiosClient.get('/incidents/nearby', { params }),
  list: (params) => axiosClient.get('/incidents', { params }),
  verify: (incidentId, payload) => axiosClient.post(`/incidents/${incidentId}/verify`, payload),
}
