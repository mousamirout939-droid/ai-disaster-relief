import axiosClient from './axiosClient.js'

export const analyticsApi = {
  getDashboard: () => axiosClient.get('/analytics/dashboard'),
}
