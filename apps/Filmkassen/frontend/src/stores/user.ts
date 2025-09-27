import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '../types'
import { authApi } from '../services/api'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isLoggedIn = computed(() => !!user.value)

  const login = async (username: string, password: string) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.login({ username, password })
      user.value = response.user
      accessToken.value = response.access_token
      // Store token in localStorage for persistence
      localStorage.setItem('access_token', response.access_token)
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const register = async (username: string, email: string, password: string) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.register({ username, email, password })
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registrering fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    loading.value = true
    error.value = null
    
    try {
      await authApi.logout()
      user.value = null
      accessToken.value = null
      localStorage.removeItem('access_token')
    } catch (err: any) {
      console.error('Logout error:', err)
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  // Verify current token and get user info
  const verifyToken = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return false

    try {
      // Decode token to check if it's expired
      const payload = JSON.parse(atob(token.split('.')[1]))
      const now = Math.floor(Date.now() / 1000)
      
      if (payload.exp && payload.exp < now) {
        // Token is expired
        localStorage.removeItem('access_token')
        accessToken.value = null
        user.value = null
        return false
      }

      // Token is valid, try to get user info by making a test API call
      accessToken.value = token
      // For simplicity, we'll create a minimal user object from token
      user.value = {
        id: 0, // We don't have this from token
        username: payload.sub,
        email: '', // We don't have this from token
        created_at: ''
      }
      return true
    } catch (error) {
      console.error('Error verifying token:', error)
      localStorage.removeItem('access_token')
      accessToken.value = null
      user.value = null
      return false
    }
  }

  // Initialize from localStorage on store creation
  const initFromStorage = async () => {
    await verifyToken()
  }

  // Call init on store creation
  initFromStorage()

  return {
    user,
    accessToken,
    loading,
    error,
    isLoggedIn,
    login,
    register,
    logout,
    clearError,
    verifyToken
  }
})
