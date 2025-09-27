import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../services/api'
import type { User, LoginResponse } from '../types/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const login = async (username: string, password: string) => {
    try {
      const response = await api.post<LoginResponse>('/auth/login', {
        username,
        password
      })
      
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('token', response.data.access_token)
      
      console.log('Login successful, token stored:', response.data.access_token)
      return response.data
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  const register = async (username: string, email: string, password: string) => {
    try {
      const response = await api.post<User>('/auth/register', {
        username,
        email,
        password
      })
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const checkAuth = async () => {
    if (!token.value) return false
    
    try {
      const response = await api.get<User>('/auth/me')
      user.value = response.data
      return true
    } catch (error) {
      logout()
      return false
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth
  }
})
