import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

// API functions
export const certificateAPI = {
  // Upload certificates
  uploadSingle: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/upload/single', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  uploadBulk: (files: File[]) => {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    return apiClient.post('/upload/bulk', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // Get certificates
  getCertificates: (params?: { status_filter?: string; limit?: number; skip?: number }) => {
    return apiClient.get('/certificates/', { params })
  },

  getCertificate: (id: string) => {
    return apiClient.get(`/certificates/${id}`)
  },

  deleteCertificate: (id: string) => {
    return apiClient.delete(`/certificates/${id}`)
  },

  // Verification
  getVerificationResults: (params?: { status_filter?: string; days?: number; limit?: number }) => {
    return apiClient.get('/verification/results', { params })
  },

  getStatistics: (days?: number) => {
    return apiClient.get('/verification/statistics', { params: { days } })
  },

  requestManualReview: (certificateId: string) => {
    return apiClient.post('/verification/manual-review', { certificate_id: certificateId })
  },

  // Batch progress
  getBatchProgress: (batchId: string) => {
    return apiClient.get(`/upload/batch/${batchId}/progress`)
  }
}

export const userAPI = {
  getProfile: () => apiClient.get('/users/me'),
  updateProfile: (data: any) => apiClient.put('/users/me', data),
  getStats: () => apiClient.get('/users/stats')
}

export const authAPI = {
  register: (userData: {
    email: string
    password: string
    full_name: string
    role?: string
    institution_name?: string
  }) => {
    return apiClient.post('/auth/register', userData)
  },

  login: (credentials: { email: string; password: string }) => {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    return apiClient.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  getCurrentUser: () => {
    return apiClient.get('/auth/me')
  },

  logout: () => {
    localStorage.removeItem('token')
    window.location.href = '/'
  }
}