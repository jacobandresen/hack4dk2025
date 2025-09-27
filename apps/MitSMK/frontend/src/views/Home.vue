<template>
  <div class="max-w-7xl mx-auto">
    <!-- Search Section -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">
        Søg efter kunstværker
      </h1>
      <p class="text-lg text-gray-600 mb-8">
        Udforsk Statens Museum for Kunsts samling og opret dine egne samlinger
      </p>
      
      <!-- Search Form -->
      <form @submit.prevent="handleSearch" class="max-w-2xl mx-auto">
        <div class="flex gap-2">
          <input
            v-model="localSearchQuery"
            type="text"
            placeholder="Søg efter kunstværker, kunstnere eller emner..."
            class="input-field flex-1"
            :disabled="store.isLoading"
          />
          <button
            type="submit"
            class="btn-primary px-8"
            :disabled="store.isLoading || !localSearchQuery.trim()"
          >
            <span v-if="store.isLoading">Søger...</span>
            <span v-else>Søg</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Search Results -->
    <div v-if="store.searchResults.length > 0" class="mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold text-gray-900">
          Søgeresultater for "{{ localSearchQuery }}"
        </h2>
        <span class="text-gray-600">
          {{ store.totalResults }} resultater fundet
        </span>
      </div>
      
      <ArtworkGrid
        :artworks="store.searchResults"
        @artwork-click="handleArtworkClick"
      />
      
      <!-- Load More Button -->
      <div v-if="store.searchResults.length < store.totalResults" class="text-center mt-8">
        <button
          @click="store.loadMore"
          class="btn-secondary"
          :disabled="store.isLoading"
        >
          <span v-if="store.isLoading">Indlæser...</span>
          <span v-else>Indlæs flere</span>
        </button>
      </div>
    </div>

    <!-- No Results -->
    <div v-else-if="localSearchQuery && !store.isLoading" class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <h3 class="text-xl font-medium text-gray-900 mb-2">Ingen resultater fundet</h3>
      <p class="text-gray-600">Prøv at søge efter noget andet</p>
    </div>

    <!-- Welcome Message -->
    <div v-else-if="!localSearchQuery" class="text-center py-12">
      <div class="text-smk-blue mb-4">
        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      <h3 class="text-xl font-medium text-gray-900 mb-2">Velkommen til MitSMK</h3>
      <p class="text-gray-600">Søg efter kunstværker i Statens Museum for Kunsts samling</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArtworksStore } from '../stores/artworks'
import ArtworkGrid from '../components/ArtworkGrid.vue'

const router = useRouter()
const artworksStore = useArtworksStore()

// Don't destructure to maintain reactivity
const store = artworksStore

// Make sure searchQuery is reactive
const localSearchQuery = ref('')

const handleSearch = async () => {
  if (!localSearchQuery.value.trim()) return
  
  try {
    await store.searchArtworks(localSearchQuery.value)
  } catch (error) {
    console.error('Search error:', error)
  }
}

const handleArtworkClick = (artwork: any) => {
  router.push(`/artwork/${artwork.object_number}`)
}

onMounted(() => {
  store.clearSearch()
  localSearchQuery.value = ''
})
</script>
