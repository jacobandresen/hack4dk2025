<template>
  <div id="app">
    <header class="header">
      <div class="container">
        <h1 class="logo">
          <router-link to="/">Filmkassen</router-link>
        </h1>
        <nav class="nav">
          <router-link to="/" class="nav-link">Hjem</router-link>
          <router-link v-if="!user" to="/login" class="nav-link">Login</router-link>
          <router-link v-if="!user" to="/register" class="nav-link">Registrer</router-link>
          <router-link v-if="user" to="/collections" class="nav-link">Mine Filmkasser</router-link>
          <button v-if="user" @click="logout" class="nav-link logout-btn">Log ud</button>
        </nav>
      </div>
    </header>
    
    <main class="main">
      <router-view />
    </main>
    
    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 Filmkassen. Powered by DFI API.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from './stores/user'

const userStore = useUserStore()
const user = computed(() => userStore.user)

const logout = () => {
  userStore.logout()
}
</script>

<style scoped>
.header {
  background: #1a1a1a;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: rgba(255,255,255,0.1);
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: inherit;
}

.main {
  min-height: calc(100vh - 120px);
}

.footer {
  background: #f5f5f5;
  padding: 1rem 0;
  text-align: center;
  color: #666;
}
</style>
