<template>
  <div class="collections">
    <div class="container">
      <div class="collections-header">
        <h2>Mine Filmkasser</h2>
        <button @click="showCreateForm = !showCreateForm" class="btn">
          {{ showCreateForm ? 'Annuller' : 'Opret ny filmkasse' }}
        </button>
      </div>

      <div v-if="showCreateForm" class="create-collection-form">
        <h3>Opret ny filmkasse</h3>
        <form @submit.prevent="handleCreateCollection">
          <div class="form-group">
            <label for="name" class="form-label">Navn</label>
            <input
              id="name"
              v-model="newCollection.name"
              type="text"
              class="form-input"
              placeholder="Indtast navn på filmkasse..."
              required
            />
          </div>
          
          <div class="form-group">
            <label for="description" class="form-label">Beskrivelse (valgfri)</label>
            <textarea
              id="description"
              v-model="newCollection.description"
              class="form-textarea"
              placeholder="Beskriv filmkassen..."
            />
          </div>

          <div v-if="error" class="error">
            {{ error }}
          </div>

          <button type="submit" class="btn" :disabled="loading">
            {{ loading ? 'Opretter...' : 'Opret filmkasse' }}
          </button>
        </form>
      </div>

      <div v-if="loading && collections.length === 0" class="loading">
        <p>Henter filmkasser...</p>
      </div>

      <div v-else-if="collections.length === 0" class="no-collections">
        <p>Du har ingen filmkasser endnu.</p>
        <p>Debug: collections.length = {{ collections.length }}</p>
        <p>Debug: collections = {{ collections }}</p>
        <p>Debug: collectionsStore.collections.length = {{ collectionsStore.collections.length }}</p>
        <p>Debug: collectionsStore.collections = {{ collectionsStore.collections }}</p>
        <button @click="showCreateForm = true" class="btn">
          Opret din første filmkasse
        </button>
      </div>

      <div v-else class="collections-grid">
        <div
          v-for="collection in collections"
          :key="collection.id"
          class="collection-card"
        >
          <div class="collection-header" @click="toggleCollection(collection.id)">
            <h3>{{ collection.name }}</h3>
            <span class="toggle-icon">
              {{ expandedCollections.has(collection.id) ? '−' : '+' }}
            </span>
          </div>
          
          <div
            v-if="expandedCollections.has(collection.id)"
            class="collection-content"
          >
            <p v-if="collection.description" class="collection-description">
              {{ collection.description }}
            </p>
            
            <div v-if="collectionMovies[collection.id]" class="collection-movies">
              <h4>Film i kassen ({{ collectionMovies[collection.id].length }})</h4>
              <div v-if="collectionMovies[collection.id].length === 0" class="no-movies">
                <p>Ingen film i denne kasse endnu.</p>
              </div>
              <div v-else class="movies-list">
                <div
                  v-for="collectionMovie in collectionMovies[collection.id]"
                  :key="collectionMovie.id"
                  class="collection-movie-item"
                >
                  <div class="movie-info">
                    <h5>{{ collectionMovie.movie.title }}</h5>
                    <p v-if="collectionMovie.movie.year">{{ collectionMovie.movie.year }}</p>
                    <p v-if="collectionMovie.note" class="movie-note">
                      <em>{{ collectionMovie.note }}</em>
                    </p>
                  </div>
                  <div class="movie-actions">
                    <button
                      @click="goToMovie(collectionMovie.movie.id)"
                      class="btn btn-secondary"
                    >
                      Se detaljer
                    </button>
                    <button
                      @click="removeMovie(collection.id, collectionMovie.movie.id)"
                      class="btn btn-danger"
                    >
                      Fjern
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="collection-actions">
              <button
                @click="editCollection(collection)"
                class="btn btn-secondary"
              >
                Rediger
              </button>
              <button
                @click="deleteCollection(collection.id)"
                class="btn btn-danger"
              >
                Slet filmkasse
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCollectionsStore } from '../stores/collections'
import type { Collection, CollectionCreate } from '../types'

const router = useRouter()
const collectionsStore = useCollectionsStore()

const showCreateForm = ref(false)
const expandedCollections = ref(new Set<number>())
const collectionMovies = ref<Record<number, any[]>>({})

const newCollection = ref<CollectionCreate>({
  name: '',
  description: ''
})

const collections = computed(() => {
  console.log('CollectionsView: collections computed - store collections:', collectionsStore.collections)
  console.log('CollectionsView: collections computed - length:', collectionsStore.collections.length)
  console.log('CollectionsView: collections computed - returning:', collectionsStore.collections)
  return collectionsStore.collections
})
const loading = computed(() => collectionsStore.loading)
const error = computed(() => collectionsStore.error)

const toggleCollection = async (collectionId: number) => {
  if (expandedCollections.value.has(collectionId)) {
    expandedCollections.value.delete(collectionId)
  } else {
    expandedCollections.value.add(collectionId)
    // Load collection details if not already loaded
    if (!collectionMovies.value[collectionId]) {
      try {
        const details = await collectionsStore.getCollectionDetails(collectionId)
        collectionMovies.value[collectionId] = details.movies
      } catch (err) {
        console.error('Error loading collection details:', err)
      }
    }
  }
}

const handleCreateCollection = async () => {
  if (!newCollection.value.name.trim()) return
  
  try {
    console.log('Creating collection:', newCollection.value)
    await collectionsStore.createCollection(newCollection.value)
    console.log('Collection created successfully')
    newCollection.value = { name: '', description: '' }
    showCreateForm.value = false
  } catch (err) {
    console.error('Error creating collection:', err)
  }
}

const editCollection = (collection: Collection) => {
  // TODO: Implement edit functionality
  console.log('Edit collection:', collection)
}

const deleteCollection = async (collectionId: number) => {
  if (!confirm('Er du sikker på, at du vil slette denne filmkasse?')) return
  
  try {
    await collectionsStore.deleteCollection(collectionId)
    expandedCollections.value.delete(collectionId)
    delete collectionMovies.value[collectionId]
  } catch (err) {
    console.error('Error deleting collection:', err)
  }
}

const removeMovie = async (collectionId: number, movieId: number) => {
  if (!confirm('Er du sikker på, at du vil fjerne denne film fra filmkassen?')) return
  
  try {
    await collectionsStore.removeMovieFromCollection(collectionId, movieId)
    // Update local state
    if (collectionMovies.value[collectionId]) {
      collectionMovies.value[collectionId] = collectionMovies.value[collectionId].filter(
        cm => cm.movie.id !== movieId
      )
    }
  } catch (err) {
    console.error('Error removing movie:', err)
  }
}

const goToMovie = (movieId: number) => {
  router.push({ name: 'movie-detail', params: { id: movieId } })
}

// Watch for changes in collections
watch(() => collectionsStore.collections, (newCollections) => {
  console.log('CollectionsView: collections changed in store:', newCollections)
  console.log('CollectionsView: new collections length:', newCollections.length)
}, { deep: true })

// Watch for changes in computed collections
watch(collections, (newCollections) => {
  console.log('CollectionsView: computed collections changed:', newCollections)
  console.log('CollectionsView: computed collections length:', newCollections.length)
}, { deep: true })

onMounted(async () => {
  console.log('CollectionsView: Component mounted, fetching collections...')
  try {
    await collectionsStore.fetchCollections()
    console.log('CollectionsView: Collections fetched, current collections:', collections.value)
  } catch (err) {
    console.error('CollectionsView: Error loading collections:', err)
  }
})
</script>

<style scoped>
.collections {
  padding: 2rem 0;
}

.collections-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.create-collection-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.collections-grid {
  display: grid;
  gap: 1rem;
}

.collection-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.collection-header {
  background: #f8f9fa;
  padding: 1rem;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dee2e6;
}

.collection-header:hover {
  background: #e9ecef;
}

.toggle-icon {
  font-size: 1.5rem;
  font-weight: bold;
  color: #666;
}

.collection-content {
  padding: 1rem;
}

.collection-description {
  color: #666;
  margin-bottom: 1rem;
  font-style: italic;
}

.collection-movies h4 {
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.no-movies {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}

.movies-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.collection-movie-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.movie-info h5 {
  margin: 0 0 0.5rem 0;
  color: #1a1a1a;
}

.movie-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.movie-note {
  font-style: italic;
  color: #007bff;
}

.movie-actions {
  display: flex;
  gap: 0.5rem;
}

.collection-actions {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  gap: 1rem;
}

.no-collections {
  text-align: center;
  padding: 3rem;
  color: #666;
}

@media (max-width: 768px) {
  .collections-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .collection-movie-item {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .movie-actions {
    justify-content: center;
  }
  
  .collection-actions {
    flex-direction: column;
  }
}
</style>
