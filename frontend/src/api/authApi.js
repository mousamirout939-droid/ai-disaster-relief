import axiosClient from './axiosClient.js'

export const authApi = {
  register: (payload) => axiosClient.post('/auth/register', payload),
  login: (payload) => axiosClient.post('/auth/login', payload),
  refresh: (refreshToken) => axiosClient.post('/auth/refresh', { refresh_token: refreshToken }),
  logout: () => axiosClient.post('/auth/logout'),
  getMe: () => axiosClient.get('/auth/me'),
}
