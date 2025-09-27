<template>
  <div class="max-w-md mx-auto">
    <div class="card p-8">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-smk-blue rounded-lg flex items-center justify-center mx-auto mb-4">
          <span class="text-white font-bold text-2xl">M</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">Log ind</h1>
        <p class="text-gray-600 mt-2">Log ind på din MitSMK konto</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
            Brugernavn
          </label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            class="input-field"
            :disabled="isLoading"
            placeholder="Indtast dit brugernavn"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Adgangskode
          </label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            class="input-field"
            :disabled="isLoading"
            placeholder="Indtast din adgangskode"
          />
        </div>

        <button
          type="submit"
          class="btn-primary w-full"
          :disabled="isLoading"
        >
          <span v-if="isLoading">Logger ind...</span>
          <span v-else>Log ind</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-600">
          Har du ikke en konto?
          <RouterLink to="/register" class="text-smk-blue hover:underline font-medium">
            Opret en konto
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const isLoading = ref(false)

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) return
  
  isLoading.value = true
  try {
    await authStore.login(form.value.username, form.value.password)
    router.push('/')
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Fejl ved login'
    alert(message)
  } finally {
    isLoading.value = false
  }
}
</script>

