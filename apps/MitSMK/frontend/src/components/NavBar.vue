<template>
  <nav class="bg-white shadow-lg border-b border-gray-200">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-smk-blue rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-lg">M</span>
          </div>
          <span class="text-xl font-bold text-gray-900">MitSMK</span>
        </RouterLink>

        <!-- Navigation Links -->
        <div class="flex items-center space-x-6">
          <RouterLink 
            to="/" 
            class="text-gray-600 hover:text-smk-blue transition-colors duration-200"
            :class="{ 'text-smk-blue font-medium': $route.name === 'Home' }"
          >
            Søg kunst
          </RouterLink>
          
          <RouterLink 
            v-if="authStore.isAuthenticated"
            to="/collections" 
            class="text-gray-600 hover:text-smk-blue transition-colors duration-200"
            :class="{ 'text-smk-blue font-medium': $route.name === 'Collections' }"
          >
            Mine samlinger
          </RouterLink>

          <!-- Auth Buttons -->
          <div v-if="!authStore.isAuthenticated" class="flex items-center space-x-3">
            <RouterLink 
              to="/login" 
              class="text-gray-600 hover:text-smk-blue transition-colors duration-200"
            >
              Log ind
            </RouterLink>
            <RouterLink 
              to="/register" 
              class="btn-primary"
            >
              Opret konto
            </RouterLink>
          </div>

          <!-- User Menu -->
          <div v-else class="flex items-center space-x-3">
            <span class="text-gray-600">Hej, {{ authStore.user?.username }}</span>
            <button 
              @click="authStore.logout" 
              class="text-gray-600 hover:text-smk-blue transition-colors duration-200"
            >
              Log ud
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
// Don't destructure to maintain reactivity
</script>
