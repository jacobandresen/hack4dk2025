<template>
  <div v-if="isLoading" class="text-center py-12">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-smk-blue mx-auto"></div>
    <p class="mt-4 text-gray-600">Indlæser samling...</p>
  </div>

  <div v-else-if="collection" class="max-w-7xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <button
        @click="$router.push('/collections')"
        class="flex items-center text-smk-blue hover:text-blue-800 mb-4 transition-colors duration-200"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Tilbage til samlinger
      </button>

      <div class="flex justify-between items-start">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            {{ collection.name }}
          </h1>
          <p v-if="collection.description" class="text-gray-600 text-lg">
            {{ collection.description }}
          </p>
          <p class="text-gray-500 mt-2">
            {{ collection.artworks.length }} kunstværker
          </p>
        </div>

        <div class="flex space-x-3">
          <button
            @click="showEditModal = true"
            class="btn-secondary"
          >
            Rediger
          </button>
          <button
            @click="confirmDelete"
            class="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
          >
            Slet samling
          </button>
        </div>
      </div>
    </div>

    <!-- Artworks Grid -->
    <div v-if="collection.artworks.length === 0" class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      <h3 class="text-xl font-medium text-gray-900 mb-2">Ingen kunstværker endnu</h3>
      <p class="text-gray-600 mb-6">Tilføj kunstværker til din samling ved at søge efter dem</p>
      <RouterLink to="/" class="btn-primary">
        Søg efter kunstværker
      </RouterLink>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div
        v-for="item in collection.artworks"
        :key="item.id"
        class="artwork-card group"
        @click="$router.push(`/artwork/${item.artwork.object_number}`)"
      >
        <div class="aspect-square mb-3 overflow-hidden rounded-lg bg-gray-100">
          <img
            v-if="item.artwork.image_thumbnail"
            :src="item.artwork.image_thumbnail"
            :alt="item.artwork.title || 'Kunstværk'"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            @error="handleImageError"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center text-gray-400"
          >
            <span>Intet billede</span>
          </div>
        </div>
        
        <div class="space-y-1">
          <h3 class="font-medium text-gray-900 line-clamp-2">
            {{ item.artwork.title || 'Uden titel' }}
          </h3>
          
          <div class="flex items-center justify-between text-sm text-gray-600">
            <span v-if="item.artwork.artist_name">{{ item.artwork.artist_name }}</span>
            <span v-if="item.artwork.year">{{ item.artwork.year }}</span>
          </div>

          <p v-if="item.note" class="text-sm text-gray-500 line-clamp-2">
            {{ item.note }}
          </p>

          <button
            @click.stop="removeArtwork(item.artwork.id)"
            class="text-red-600 hover:text-red-800 text-sm font-medium"
          >
            Fjern fra samling
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Collection Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="showEditModal = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Rediger samling</h3>
        
        <form @submit.prevent="handleUpdateCollection" class="space-y-4">
          <div>
            <label for="editName" class="block text-sm font-medium text-gray-700 mb-2">
              Navn
            </label>
            <input
              id="editName"
              v-model="editForm.name"
              type="text"
              required
              class="input-field"
              placeholder="Indtast samlingens navn"
            />
          </div>
          
          <div>
            <label for="editDescription" class="block text-sm font-medium text-gray-700 mb-2">
              Beskrivelse (valgfrit)
            </label>
            <textarea
              id="editDescription"
              v-model="editForm.description"
              class="input-field"
              rows="3"
              placeholder="Beskriv din samling"
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="showEditModal = false"
              class="btn-secondary"
            >
              Annuller
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="isUpdating"
            >
              <span v-if="isUpdating">Gemmer...</span>
              <span v-else>Gem ændringer</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div v-else class="text-center py-12">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">Samling ikke fundet</h2>
    <p class="text-gray-600 mb-6">Den ønskede samling kunne ikke findes.</p>
    <RouterLink to="/collections" class="btn-primary">
      Tilbage til samlinger
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCollectionsStore } from '../stores/collections'

const route = useRoute()
const collectionsStore = useCollectionsStore()

const {
  currentCollection,
  isLoading,
  fetchCollectionDetails,
  updateCollection,
  deleteCollection,
  removeArtworkFromCollection
} = collectionsStore

const showEditModal = ref(false)
const isUpdating = ref(false)

const collection = computed(() => currentCollection)

const editForm = ref({
  name: '',
  description: ''
})

const handleUpdateCollection = async () => {
  if (!collection.value || !editForm.value.name.trim()) return
  
  isUpdating.value = true
  try {
    await updateCollection(
      collection.value.id,
      editForm.value.name,
      editForm.value.description || undefined
    )
    
    showEditModal.value = false
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Fejl ved opdatering af samling'
    alert(message)
  } finally {
    isUpdating.value = false
  }
}

const confirmDelete = () => {
  if (confirm('Er du sikker på, at du vil slette denne samling? Denne handling kan ikke fortrydes.')) {
    handleDeleteCollection()
  }
}

const handleDeleteCollection = async () => {
  if (!collection.value) return
  
  try {
    await deleteCollection(collection.value.id)
    // Redirect to collections list
    window.location.href = '/collections'
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Fejl ved sletning af samling'
    alert(message)
  }
}

const removeArtwork = async (artworkId: string) => {
  if (!collection.value) return
  
  if (confirm('Er du sikker på, at du vil fjerne dette kunstværk fra samlingen?')) {
    try {
      await removeArtworkFromCollection(collection.value.id, artworkId)
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Fejl ved fjernelse af kunstværk'
      alert(message)
    }
  }
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  img.parentElement!.innerHTML = '<div class="w-full h-full flex items-center justify-center text-gray-400"><span>Intet billede</span></div>'
}

onMounted(async () => {
  const collectionId = route.params.id as string
  await fetchCollectionDetails(collectionId)
  
  if (collection.value) {
    editForm.value = {
      name: collection.value.name,
      description: collection.value.description || ''
    }
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

