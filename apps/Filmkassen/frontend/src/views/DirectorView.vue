<template>
  <div class="director">
    <div class="container">
      <div v-if="loading" class="loading">
        <p>Henter instruktør information...</p>
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="director" class="director-content">
        <div class="director-header">
          <h1>{{ director.name }}</h1>
          <p v-if="director.bio" class="director-bio">{{ director.bio }}</p>
        </div>

        <div v-if="directorMovies.length > 0" class="director-movies">
          <h2>Film af {{ director.name }}</h2>
          <div class="movie-grid">
            <div
              v-for="movie in directorMovies"
              :key="movie.id"
              class="movie-card"
              @click="goToMovie(movie.id)"
            >
              <img
                v-if="movie.poster_url"
                :src="movie.poster_url"
                :alt="movie.title"
                class="movie-poster"
              />
              <div v-else class="movie-poster-placeholder">
                <span>Ingen plakat</span>
              </div>
              <div class="movie-info">
                <h4 class="movie-title">{{ movie.title }}</h4>
                <p v-if="movie.year" class="movie-year">{{ movie.year }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-movies">
          <p>Ingen film fundet for denne instruktør.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoviesStore } from '../stores/movies'

const route = useRoute()
const router = useRouter()
const moviesStore = useMoviesStore()

const { currentDirector, directorMovies, loading, error } = moviesStore

const director = currentDirector

onMounted(async () => {
  const directorId = parseInt(route.params.id as string)
  if (directorId) {
    try {
      await moviesStore.getDirectorMovies(directorId)
    } catch (err) {
      console.error('Error loading director details:', err)
    }
  }
})

const goToMovie = (movieId: number) => {
  router.push({ name: 'movie-detail', params: { id: movieId } })
}
</script>

<style scoped>
.director {
  padding: 2rem 0;
}

.director-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.director-header {
  padding: 2rem;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.director-header h1 {
  margin: 0 0 1rem 0;
  color: #1a1a1a;
}

.director-bio {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.director-movies {
  padding: 2rem;
}

.director-movies h2 {
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.no-movies {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-style: italic;
}
</style>
