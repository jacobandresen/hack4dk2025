<template>
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Mine samlinger</h1>
        <p class="text-gray-600 mt-2">Administrer dine kunstsamlinger</p>
      </div>
      
      <button
        @click="showCreateModal = true"
        class="btn-primary"
      >
        Opret ny samling
      </button>
    </div>

    <!-- Collections Grid -->
    <div v-if="collectionsStore.isLoading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-smk-blue mx-auto"></div>
      <p class="mt-4 text-gray-600">Indlæser samlinger...</p>
    </div>

    <div v-else-if="collectionsStore.collections.length === 0" class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <h3 class="text-xl font-medium text-gray-900 mb-2">Ingen samlinger endnu</h3>
      <p class="text-gray-600 mb-6">Opret din første samling for at begynde at samle kunstværker</p>
      <button
        @click="showCreateModal = true"
        class="btn-primary"
      >
        Opret første samling
      </button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="collection in collectionsStore.collections"
        :key="collection.id"
        class="card p-6 hover:shadow-lg transition-shadow duration-200 cursor-pointer"
        @click="$router.push(`/collections/${collection.id}`)"
      >
        <h3 class="text-xl font-semibold text-gray-900 mb-2">
          {{ collection.name }}
        </h3>
        
        <p v-if="collection.description" class="text-gray-600 mb-4 line-clamp-2">
          {{ collection.description }}
        </p>
        
        <div class="flex justify-between items-center text-sm text-gray-500">
          <span>Oprettet {{ formatDate(collection.created_at) }}</span>
          <span>{{ collection.artworks?.length || 0 }} kunstværker</span>
        </div>
      </div>
    </div>

    <!-- Create Collection Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="showCreateModal = false"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Opret ny samling</h3>
        
        <form @submit.prevent="handleCreateCollection" class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Navn
            </label>
            <input
              id="name"
              v-model="newCollection.name"
              type="text"
              required
              class="input-field"
              placeholder="Indtast samlingens navn"
            />
          </div>
          
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
              Beskrivelse (valgfrit)
            </label>
            <textarea
              id="description"
              v-model="newCollection.description"
              class="input-field"
              rows="3"
              placeholder="Beskriv din samling"
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="showCreateModal = false"
              class="btn-secondary"
            >
              Annuller
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="isCreating"
            >
              <span v-if="isCreating">Opretter...</span>
              <span v-else>Opret samling</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCollectionsStore } from '../stores/collections'

const collectionsStore = useCollectionsStore()
// Don't destructure to maintain reactivity

const showCreateModal = ref(false)
const isCreating = ref(false)

const newCollection = ref({
  name: '',
  description: ''
})

const handleCreateCollection = async () => {
  if (!newCollection.value.name.trim()) return
  
  isCreating.value = true
  try {
    await collectionsStore.createCollection(
      newCollection.value.name,
      newCollection.value.description || undefined
    )
    
    newCollection.value = { name: '', description: '' }
    showCreateModal.value = false
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Fejl ved oprettelse af samling'
    alert(message)
  } finally {
    isCreating.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('da-DK')
}

onMounted(async () => {
  await collectionsStore.fetchCollections()
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
