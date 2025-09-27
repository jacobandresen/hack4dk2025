<template>
  <div class="max-w-md mx-auto">
    <div class="card p-8">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-smk-blue rounded-lg flex items-center justify-center mx-auto mb-4">
          <span class="text-white font-bold text-2xl">M</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">Opret konto</h1>
        <p class="text-gray-600 mt-2">Opret en ny MitSMK konto</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
            Brugernavn
          </label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            minlength="3"
            maxlength="50"
            class="input-field"
            :disabled="isLoading"
            placeholder="Vælg et brugernavn"
          />
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            E-mail
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            class="input-field"
            :disabled="isLoading"
            placeholder="Indtast din e-mail"
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
            minlength="8"
            class="input-field"
            :disabled="isLoading"
            placeholder="Vælg en adgangskode (mindst 8 tegn)"
          />
        </div>

        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
            Bekræft adgangskode
          </label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            class="input-field"
            :disabled="isLoading"
            placeholder="Bekræft din adgangskode"
          />
        </div>

        <div v-if="form.password && form.confirmPassword && form.password !== form.confirmPassword" class="text-red-600 text-sm">
          Adgangskoderne matcher ikke
        </div>

        <button
          type="submit"
          class="btn-primary w-full"
          :disabled="isLoading || form.password !== form.confirmPassword"
        >
          <span v-if="isLoading">Opretter konto...</span>
          <span v-else>Opret konto</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-600">
          Har du allerede en konto?
          <RouterLink to="/login" class="text-smk-blue hover:underline font-medium">
            Log ind
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
  email: '',
  password: '',
  confirmPassword: ''
})

const isLoading = ref(false)

const handleRegister = async () => {
  if (!form.value.username || !form.value.email || !form.value.password) return
  if (form.value.password !== form.value.confirmPassword) return
  
  isLoading.value = true
  try {
    await authStore.register(form.value.username, form.value.email, form.value.password)
    // Auto-login after registration
    await authStore.login(form.value.username, form.value.password)
    router.push('/')
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Fejl ved oprettelse af konto'
    alert(message)
  } finally {
    isLoading.value = false
  }
}
</script>
