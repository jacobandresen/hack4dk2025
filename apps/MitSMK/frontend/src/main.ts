import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Initialize auth store to check for existing token
const authStore = useAuthStore()
authStore.checkAuth()

app.mount('#app')
