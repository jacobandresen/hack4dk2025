<template>
  <div class="movie-detail">
    <div class="container">
      <div v-if="loading" class="loading">
        <p>Henter filmdetaljer...</p>
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="movie" class="movie-content">
        <div class="movie-header">
          <div class="movie-poster-section">
            <img
              v-if="movie?.poster_url"
              :src="movie.poster_url"
              :alt="movie.title"
              class="movie-poster-large"
            />
            <div v-else class="movie-poster-placeholder-large">
              <span>Ingen plakat tilgængelig</span>
            </div>
          </div>
          
          <div class="movie-info-section">
            <h1 class="movie-title">{{ movie?.title }}</h1>
            <p v-if="movie?.year" class="movie-year">{{ movie.year }}</p>
            
            <div v-if="movie?.director" class="movie-director">
              <strong>Instruktør:</strong>
              <a @click="goToDirector(movie.director)" class="director-link">
                {{ movie.director }}
              </a>
            </div>

            <div v-if="movie?.cast && movie.cast.length > 0" class="movie-cast">
              <strong>Medvirkende:</strong>
              <p>{{ movie.cast.join(', ') }}</p>
            </div>

            <div v-if="movie?.videotek_url" class="movie-videotek">
              <a :href="movie.videotek_url" target="_blank" class="btn">
                Se i Videoteket
              </a>
            </div>

            <div v-if="user" class="collection-actions">
              <h3>Tilføj til filmkasse</h3>
              <div v-if="availableCollections.length > 0" class="add-to-collection">
                <select v-model="selectedCollectionId" class="form-input">
                  <option value="">Vælg filmkasse...</option>
                  <option
                    v-for="collection in availableCollections"
                    :key="collection.id"
                    :value="collection.id"
                  >
                    {{ collection.name }}
                  </option>
                </select>
                <button
                  @click="addToCollection"
                  :disabled="!selectedCollectionId || addingToCollection"
                  class="btn"
                >
                  {{ addingToCollection ? 'Tilføjer...' : 'Tilføj' }}
                </button>
              </div>
              <p v-else class="no-collections">
                Du har ingen filmkasser endnu.
                <router-link to="/collections">Opret en filmkasse</router-link>
              </p>
            </div>
          </div>
        </div>

        <div v-if="movie?.description" class="movie-description">
          <h3>Beskrivelse</h3>
          <p>{{ movie.description }}</p>
        </div>

        <div v-if="movie?.clips && movie.clips.length > 0" class="movie-clips">
          <h3>Billeder fra filmen</h3>
          <div class="clips-grid">
            <img
              v-for="(clip, index) in movie.clips"
              :key="index"
              :src="clip"
              :alt="`Billede ${index + 1} fra ${movie.title}`"
              class="clip-image"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoviesStore } from '../stores/movies'
import { useCollectionsStore } from '../stores/collections'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const moviesStore = useMoviesStore()
const collectionsStore = useCollectionsStore()
const userStore = useUserStore()

const selectedCollectionId = ref<number | null>(null)
const addingToCollection = ref(false)

const collections = computed(() => collectionsStore.collections)

const movie = computed(() => moviesStore.currentMovie || null)
const loading = computed(() => moviesStore.loading)
const error = computed(() => moviesStore.error)
const user = computed(() => userStore.user)

const availableCollections = computed(() => {
  if (!movie.value || !collections.value) return []
  
  // Filter out collections that already contain this movie
  return collections.value.filter((collection: any) => {
    // This would need to be implemented based on your data structure
    return true // For now, show all collections
  })
})

onMounted(async () => {
  const movieId = parseInt(route.params.id as string)
  console.log('MovieDetailView mounted with movieId:', movieId)
  if (movieId) {
    try {
      console.log('Fetching movie details for ID:', movieId)
      const movie = await moviesStore.getMovieDetails(movieId)
      console.log('Movie details loaded:', movie)
      console.log('Current movie in store:', moviesStore.currentMovie)
      if (user.value) {
        await collectionsStore.fetchCollections()
      }
    } catch (err) {
      console.error('Error loading movie details:', err)
    }
  } else {
    console.error('No movie ID provided in route params')
  }
})

const goToDirector = (directorName: string) => {
  router.push({ name: 'home', query: { director: directorName } })
}

// Watch for route changes to load new movie
watch(() => route.params.id, async (newId) => {
  if (newId) {
    const movieId = parseInt(newId as string)
    console.log('Route changed, loading movie ID:', movieId)
    try {
      await moviesStore.getMovieDetails(movieId)
    } catch (err) {
      console.error('Error loading new movie details:', err)
    }
  }
})

onUnmounted(() => {
  // Clear current movie when leaving the page
  moviesStore.currentMovie = null
})

const addToCollection = async () => {
  if (!selectedCollectionId.value || !movie.value) return
  
  addingToCollection.value = true
  try {
    await collectionsStore.addMovieToCollection(selectedCollectionId.value, {
      movie_id: movie.value.id,
      note: ''
    })
    alert('Film tilføjet til filmkasse!')
    selectedCollectionId.value = null
  } catch (err) {
    console.error('Error adding movie to collection:', err)
    alert('Fejl ved tilføjelse af film til filmkasse')
  } finally {
    addingToCollection.value = false
  }
}
</script>

<style scoped>
.movie-detail {
  padding: 2rem 0;
}

.movie-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.movie-header {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  padding: 2rem;
}

.movie-poster-section {
  display: flex;
  justify-content: center;
}

.movie-poster-large {
  width: 100%;
  max-width: 300px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.movie-poster-placeholder-large {
  width: 100%;
  max-width: 300px;
  aspect-ratio: 2/3;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  border-radius: 8px;
}

.movie-info-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.movie-title {
  font-size: 2.5rem;
  margin: 0;
  color: #1a1a1a;
}

.movie-year {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

.movie-director {
  font-size: 1.1rem;
}

.director-link {
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
}

.director-link:hover {
  text-decoration: underline;
}

.movie-cast p {
  margin: 0.5rem 0 0 0;
  color: #666;
}

.movie-videotek {
  margin-top: 1rem;
}

.collection-actions {
  margin-top: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.add-to-collection {
  display: flex;
  gap: 1rem;
  align-items: end;
  margin-top: 1rem;
}

.add-to-collection select {
  flex: 1;
}

.no-collections {
  color: #666;
  font-style: italic;
}

.movie-description {
  padding: 2rem;
  border-top: 1px solid #dee2e6;
}

.movie-description h3 {
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.movie-clips {
  padding: 2rem;
  border-top: 1px solid #dee2e6;
}

.movie-clips h3 {
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.clips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.clip-image {
  width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  .movie-header {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .movie-poster-large {
    max-width: 250px;
  }
  
  .add-to-collection {
    flex-direction: column;
  }
}
</style>
