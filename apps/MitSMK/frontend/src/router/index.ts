import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ArtworkDetail from '../views/ArtworkDetail.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Collections from '../views/Collections.vue'
import CollectionDetail from '../views/CollectionDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/artwork/:objectNumber',
    name: 'ArtworkDetail',
    component: ArtworkDetail,
    props: true
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/collections',
    name: 'Collections',
    component: Collections,
    meta: { requiresAuth: true }
  },
  {
    path: '/collections/:id',
    name: 'CollectionDetail',
    component: CollectionDetail,
    props: true,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  // Skip auth check for now to avoid circular dependency issues
  next()
})

export default router
