<template>
  <div v-if="store.isLoading" class="text-center py-12">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-smk-blue mx-auto"></div>
    <p class="mt-4 text-gray-600">Indlæser kunstværk...</p>
  </div>

  <div v-else-if="artwork" class="max-w-6xl mx-auto">
    <!-- Back Button -->
    <button
      @click="$router.back()"
      class="flex items-center text-smk-blue hover:text-blue-800 mb-6 transition-colors duration-200"
    >
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      Tilbage
    </button>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Image Section -->
      <div class="space-y-4">
        <div class="aspect-square bg-gray-100 rounded-lg overflow-hidden">
          <img
            v-if="artwork.image_thumbnail"
            :src="artwork.image_thumbnail"
            :alt="artwork.title || 'Kunstværk'"
            class="w-full h-full object-contain"
            @error="handleImageError"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center text-gray-400"
          >
            <span>Intet billede tilgængeligt</span>
          </div>
        </div>
        
        <!-- Download Button -->
        <div v-if="artwork.image_thumbnail" class="text-center">
          <a
            :href="artwork.image_thumbnail"
            target="_blank"
            class="btn-primary inline-flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download billede
          </a>
        </div>
      </div>

      <!-- Details Section -->
      <div class="space-y-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            {{ artwork.title || 'Uden titel' }}
          </h1>
          
          <div class="space-y-2 text-lg text-gray-600">
            <p v-if="artwork.artist_name">
              <span class="font-medium">Kunstner:</span> {{ artwork.artist_name }}
            </p>
            <p v-if="artwork.year">
              <span class="font-medium">År:</span> {{ artwork.year }}
            </p>
            <p v-if="artwork.object_number">
              <span class="font-medium">Inventarnummer:</span> {{ artwork.object_number }}
            </p>
            <p v-if="artwork.object_names && artwork.object_names.length > 0">
              <span class="font-medium">Type:</span> {{ artwork.object_names.join(', ') }}
            </p>
            <p v-if="artwork.public_domain">
              <span class="font-medium text-green-600">Public Domain</span>
            </p>
          </div>
        </div>

        <!-- Add to Collection (if authenticated) -->
        <div v-if="isAuthenticated" class="border-t pt-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Tilføj til samling</h3>
          
          <div v-if="collections.length === 0" class="text-gray-600 mb-4">
            Du har ingen samlinger endnu. 
            <RouterLink to="/collections" class="text-smk-blue hover:underline">
              Opret din første samling
            </RouterLink>
          </div>
          
          <div v-else class="space-y-3">
            <select
              v-model="selectedCollectionId"
              class="input-field"
            >
              <option value="">Vælg en samling</option>
              <option
                v-for="collection in collections"
                :key="collection.id"
                :value="collection.id"
              >
                {{ collection.name }}
              </option>
            </select>
            
            <textarea
              v-model="note"
              placeholder="Tilføj en note (valgfrit)"
              class="input-field"
              rows="3"
            ></textarea>
            
            <button
              @click="addToCollection"
              :disabled="!selectedCollectionId || isAddingToCollection"
              class="btn-primary w-full"
            >
              <span v-if="isAddingToCollection">Tilføjer...</span>
              <span v-else>Tilføj til samling</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="text-center py-12">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">Kunstværk ikke fundet</h2>
    <p class="text-gray-600 mb-6">Det ønskede kunstværk kunne ikke findes.</p>
    <RouterLink to="/" class="btn-primary">
      Tilbage til søgning
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useArtworksStore } from '../stores/artworks'
import { useCollectionsStore } from '../stores/collections'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const artworksStore = useArtworksStore()
const collectionsStore = useCollectionsStore()
const authStore = useAuthStore()

// Don't destructure to maintain reactivity
const store = artworksStore
const { collections, fetchCollections, addArtworkToCollection } = collectionsStore
const { isAuthenticated } = authStore

const selectedCollectionId = ref('')
const note = ref('')
const isAddingToCollection = ref(false)

const artwork = computed(() => store.currentArtwork)

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  img.parentElement!.innerHTML = '<div class="w-full h-full flex items-center justify-center text-gray-400"><span>Intet billede tilgængeligt</span></div>'
}

const addToCollection = async () => {
  if (!selectedCollectionId.value || !artwork.value) return
  
  isAddingToCollection.value = true
  try {
    await addArtworkToCollection(
      selectedCollectionId.value,
      artwork.value.id,
      note.value || undefined
    )
    
    selectedCollectionId.value = ''
    note.value = ''
    
    // Show success message (you could add a toast notification here)
    alert('Kunstværk tilføjet til samling!')
  } catch (error) {
    console.error('Error adding artwork to collection:', error)
    alert('Fejl ved tilføjelse til samling')
  } finally {
    isAddingToCollection.value = false
  }
}

onMounted(async () => {
  const objectNumber = route.params.objectNumber as string
  try {
    await store.getArtwork(objectNumber)
  } catch (error) {
    console.error('Error loading artwork:', error)
  }
  
  if (isAuthenticated.value) {
    await fetchCollections()
  }
})
</script>
