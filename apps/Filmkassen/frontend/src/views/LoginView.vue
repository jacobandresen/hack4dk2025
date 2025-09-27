<template>
  <div class="login">
    <div class="container">
      <div class="login-form-container">
        <h2>Log ind</h2>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">Brugernavn</label>
            <input
              id="username"
              v-model="username"
              type="text"
              class="form-input"
              placeholder="Indtast brugernavn..."
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
            />
          </div>

          <div v-if="error" class="error">
            {{ error }}
          </div>

          <button type="submit" class="btn" :disabled="loading">
            {{ loading ? 'Logger ind...' : 'Log ind' }}
          </button>
        </form>

        <div class="login-footer">
          <p>Har du ikke en konto?</p>
          <router-link to="/register" class="btn btn-secondary">
            Opret konto
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')

const { loading, error } = userStore

const handleLogin = async () => {
  if (!username.value.trim() || !password.value.trim()) return
  
  try {
    await userStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    console.error('Login error:', err)
  }
}
</script>

<style scoped>
.login {
  padding: 4rem 0;
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
}

.login-form-container {
  max-width: 400px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.login-form {
  margin-bottom: 2rem;
}

.login-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.login-footer p {
  margin-bottom: 1rem;
  color: #666;
}
</style>
