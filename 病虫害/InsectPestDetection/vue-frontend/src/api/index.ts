import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export const userApi = {
  login: (data: { username: string; password: string }) =>
    api.post('/user/login', data),
  register: (data: { username: string; password: string; captcha: string }) =>
    api.post('/user/register', data),
  getCaptcha: () => api.get('/user/captcha'),
  uploadAvatar: (formData: FormData) =>
    api.post('/user/avatar', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
}

export const detectionApi = {
  uploadFile: (formData: FormData) =>
    api.post('/detection/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  getModels: () => api.get('/detection/model'),
  setModel: (modelPath: string) => api.post('/detection/model', { path: modelPath }),
  getHistory: () => api.get('/detection/history')
}

export default api
