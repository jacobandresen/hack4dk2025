import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../services/api'
import type { Artwork, ArtworkSearchResponse } from '../types/api'

export const useArtworksStore = defineStore('artworks', () => {
  const searchResults = ref<Artwork[]>([])
  const currentArtwork = ref<Artwork | null>(null)
  const isLoading = ref(false)
  const searchQuery = ref('')
  const totalResults = ref(0)
  const currentOffset = ref(0)
  const limit = ref(20)

  const searchArtworks = async (query: string, offset: number = 0) => {
    if (!query.trim()) return
    
    isLoading.value = true
    searchQuery.value = query
    currentOffset.value = offset
    
    try {
      const response = await api.get<ArtworkSearchResponse>('/artworks/search', {
        params: {
          q: query,
          offset,
          limit: limit.value
        }
      })
      
      if (offset === 0) {
        searchResults.value = response.data.artworks
      } else {
        searchResults.value = [...searchResults.value, ...response.data.artworks]
      }
      
      totalResults.value = response.data.total
    } catch (error) {
      console.error('Error searching artworks:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const getArtwork = async (objectNumber: string) => {
    isLoading.value = true
    
    try {
      const response = await api.get<Artwork>(`/artworks/${objectNumber}`)
      currentArtwork.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching artwork:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const clearSearch = () => {
    searchResults.value = []
    searchQuery.value = ''
    totalResults.value = 0
    currentOffset.value = 0
  }

  const loadMore = async () => {
    if (searchQuery.value && !isLoading.value) {
      await searchArtworks(searchQuery.value, currentOffset.value + limit.value)
    }
  }

  return {
    searchResults,
    currentArtwork,
    isLoading,
    searchQuery,
    totalResults,
    currentOffset,
    limit,
    searchArtworks,
    getArtwork,
    clearSearch,
    loadMore
  }
})
