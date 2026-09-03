import axios from 'axios'
import { ElMessage } from 'element-plus'

// Axios 实例：统一管理后端接口
const service = axios.create({
  baseURL: '/api',
  timeout: 120000,
})

// 请求拦截器：附加 token
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('herb_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：统一处理返回结构与错误
service.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res && res.code !== undefined && res.code !== 200) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || 'Error'))
    }
    return res
  },
  (error) => {
    ElMessage.error(error.response?.data?.detail || error.message || '网络错误')
    return Promise.reject(error)
  }
)

// ============ 接口封装 ============

// 登录（调用后端校验，注册的账号可登录）
export function login(username, password) {
  return service.post('/login', { username, password }).then((res) => {
    localStorage.setItem('herb_token', 'herb_' + Date.now())
    localStorage.setItem('herb_user', res.data?.username || username)
    return res
  })
}

// 用户注册
export function register(username, password) {
  return service.post('/register', { username, password })
}

// 图片上传 + 检测识别
export function detectImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  return service.post('/detect', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// 查询历史识别记录
export function getHistory() {
  return service.get('/history')
}

// 删除指定历史记录
export function deleteHistory(id) {
  return service.delete(`/history/${id}`)
}

// 查询类别信息
export function getClasses() {
  return service.get('/classes')
}

// 健康检查
export function getHealth() {
  return service.get('/health')
}

export default service
