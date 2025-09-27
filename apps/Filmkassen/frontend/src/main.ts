import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

// Import views
import HomeView from './views/HomeView.vue'
import MovieDetailView from './views/MovieDetailView.vue'
import DirectorView from './views/DirectorView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import CollectionsView from './views/CollectionsView.vue'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/movie/:id', name: 'movie-detail', component: MovieDetailView },
    { path: '/director/:id', name: 'director', component: DirectorView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/collections', name: 'collections', component: CollectionsView }
  ]
})

// Create app
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
