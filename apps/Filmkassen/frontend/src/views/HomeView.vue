<template>
  <div class="home">
    <div class="container">
      <div class="search-form">
        <h2>Søg efter film</h2>
        <form @submit.prevent="handleSearch" class="search-input-group">
          <div class="form-group search-input">
            <label for="title" class="form-label">Filmtitel</label>
            <input
              id="title"
              v-model="searchTitle"
              type="text"
              class="form-input"
              placeholder="Indtast filmtitel..."
              required
            />
          </div>
          <div class="form-group">
            <label for="director" class="form-label">Instruktør (valgfri)</label>
            <input
              id="director"
              v-model="searchDirector"
              type="text"
              class="form-input"
              placeholder="Instruktør navn..."
            />
          </div>
          <button type="submit" class="btn" :disabled="loading">
            {{ loading ? 'Søger...' : 'Søg' }}
          </button>
        </form>
      </div>

      <div v-if="error" class="error">
        {{ error }}
      </div>

      <div v-if="searchResults.length > 0" class="search-results">
        <h3>Søgeresultater ({{ searchResults.length }} film)</h3>
        <div class="movie-grid">
          <div
            v-for="movie in searchResults"
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
              <a
                v-if="movie.director"
                @click.stop="searchByDirector(movie.director)"
                class="movie-director"
              >
                {{ movie.director }}
              </a>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!loading && hasSearched" class="no-results">
        <p>Ingen film fundet. Prøv at søge efter noget andet.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMoviesStore } from '../stores/movies'

const router = useRouter()
const moviesStore = useMoviesStore()

const searchTitle = ref('')
const searchDirector = ref('')
const hasSearched = ref(false)

const searchResults = computed(() => moviesStore.searchResults)
const loading = computed(() => moviesStore.loading)
const error = computed(() => moviesStore.error)

const handleSearch = async () => {
  if (!searchTitle.value.trim()) return
  
  hasSearched.value = true
  try {
    const response = await moviesStore.searchMovies(searchTitle.value, searchDirector.value || undefined)
    console.log('Search response:', response)
    console.log('Search results:', searchResults.value)
  } catch (err) {
    console.error('Search error:', err)
  }
}

const goToMovie = (movieId: number) => {
  router.push({ name: 'movie-detail', params: { id: movieId } })
}

const searchByDirector = (directorName: string) => {
  searchDirector.value = directorName
  searchTitle.value = ''
  handleSearch()
}
</script>

<style scoped>
.home {
  padding: 2rem 0;
}

.search-form {
  margin-bottom: 2rem;
}

.search-input-group {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.search-input {
  flex: 1;
}

.search-results h3 {
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
}

.movie-poster-placeholder {
  width: 100%;
  aspect-ratio: 2/3;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .search-input-group {
    flex-direction: column;
  }
}
</style>
