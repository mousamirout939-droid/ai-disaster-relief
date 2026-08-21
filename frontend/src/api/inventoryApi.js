import axiosClient from './axiosClient.js'

export const inventoryApi = {
  get: (shelterId) => axiosClient.get(`/shelters/${shelterId}/inventory`),
  update: (shelterId, payload) => axiosClient.put(`/shelters/${shelterId}/inventory`, payload),
}
