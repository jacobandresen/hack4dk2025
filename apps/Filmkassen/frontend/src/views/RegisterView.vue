<template>
  <div class="register">
    <div class="container">
      <div class="register-form-container">
        <h2>Opret konto</h2>
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="username" class="form-label">Brugernavn</label>
            <input
              id="username"
              v-model="username"
              type="text"
              class="form-input"
              placeholder="Indtast brugernavn..."
              required
              minlength="3"
            />
          </div>
          
          <div class="form-group">
            <label for="email" class="form-label">E-mail</label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="form-input"
              placeholder="Indtast e-mail..."
              required
            />
          </div>
          
          <div class="form-group">
            <label for="password" class="form-label">Adgangskode</label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="form-input"
              placeholder="Indtast adgangskode..."
              required
              minlength="8"
            />
          </div>

          <div class="form-group">
            <label for="confirmPassword" class="form-label">Bekræft adgangskode</label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              class="form-input"
              placeholder="Bekræft adgangskode..."
              required
            />
          </div>

          <div v-if="error" class="error">
            {{ error }}
          </div>

          <div v-if="passwordMismatch" class="error">
            Adgangskoderne matcher ikke
          </div>

          <button type="submit" class="btn" :disabled="loading || passwordMismatch">
            {{ loading ? 'Opretter konto...' : 'Opret konto' }}
          </button>
        </form>

        <div class="register-footer">
          <p>Har du allerede en konto?</p>
          <router-link to="/login" class="btn btn-secondary">
            Log ind
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const { loading, error } = userStore

const passwordMismatch = computed(() => {
  return password.value && confirmPassword.value && password.value !== confirmPassword.value
})

const handleRegister = async () => {
  if (!username.value.trim() || !email.value.trim() || !password.value.trim()) return
  if (passwordMismatch.value) return
  
  try {
    await userStore.register(username.value, email.value, password.value)
    alert('Konto oprettet! Du kan nu logge ind.')
    router.push('/login')
  } catch (err) {
    console.error('Registration error:', err)
  }
}
</script>

<style scoped>
.register {
  padding: 4rem 0;
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
}

.register-form-container {
  max-width: 400px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.register-form {
  margin-bottom: 2rem;
}

.register-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.register-footer p {
  margin-bottom: 1rem;
  color: #666;
}
</style>
