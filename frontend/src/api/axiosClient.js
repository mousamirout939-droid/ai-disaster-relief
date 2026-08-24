import axios from 'axios'
import { useAuthStore } from '../store/useAuthStore.js'

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 15000,
})

axiosClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let isRefreshing = false
let pendingQueue = []

axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          pendingQueue.push({ resolve, reject })
        }).then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return axiosClient(originalRequest)
        })
      }

      isRefreshing = true
      try {
        const newToken = await useAuthStore.getState().refreshAccessToken()
        pendingQueue.forEach(({ resolve }) => resolve(newToken))
        pendingQueue = []
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return axiosClient(originalRequest)
      } catch (refreshError) {
        pendingQueue.forEach(({ reject }) => reject(refreshError))
        pendingQueue = []
        useAuthStore.getState().logout()
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  },
)

export default axiosClient