import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../services/api'
import type { Collection, CollectionDetails, CollectionItem } from '../types/api'

export const useCollectionsStore = defineStore('collections', () => {
  const collections = ref<Collection[]>([])
  const currentCollection = ref<CollectionDetails | null>(null)
  const isLoading = ref(false)

  const fetchCollections = async () => {
    isLoading.value = true
    
    try {
      const response = await api.get<Collection[]>('/collections')
      collections.value = response.data
    } catch (error) {
      console.error('Error fetching collections:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const createCollection = async (name: string, description?: string) => {
    isLoading.value = true
    
    try {
      console.log('Creating collection:', name, description)
      const response = await api.post<Collection>('/collections', {
        name,
        description
      })
      
      console.log('Collection created successfully:', response.data)
      collections.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Error creating collection:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const updateCollection = async (id: string, name: string, description?: string) => {
    isLoading.value = true
    
    try {
      const response = await api.put<Collection>(`/collections/${id}`, {
        name,
        description
      })
      
      const index = collections.value.findIndex(c => c.id === id)
      if (index !== -1) {
        collections.value[index] = response.data
      }
      
      return response.data
    } catch (error) {
      console.error('Error updating collection:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const deleteCollection = async (id: string) => {
    isLoading.value = true
    
    try {
      await api.delete(`/collections/${id}`)
      collections.value = collections.value.filter(c => c.id !== id)
    } catch (error) {
      console.error('Error deleting collection:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchCollectionDetails = async (id: string) => {
    isLoading.value = true
    
    try {
      const response = await api.get<CollectionDetails>(`/collections/${id}`)
      currentCollection.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching collection details:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const addArtworkToCollection = async (collectionId: string, artworkId: string, note?: string) => {
    try {
      const response = await api.post<CollectionItem>(`/collections/${collectionId}/artworks`, {
        artwork_id: artworkId,
        note
      })
      
      if (currentCollection.value && currentCollection.value.id === collectionId) {
        currentCollection.value.artworks.push(response.data)
      }
      
      return response.data
    } catch (error) {
      console.error('Error adding artwork to collection:', error)
      throw error
    }
  }

  const removeArtworkFromCollection = async (collectionId: string, artworkId: string) => {
    try {
      await api.delete(`/collections/${collectionId}/artworks/${artworkId}`)
      
      if (currentCollection.value && currentCollection.value.id === collectionId) {
        currentCollection.value.artworks = currentCollection.value.artworks.filter(
          item => item.artwork.id !== artworkId
        )
      }
    } catch (error) {
      console.error('Error removing artwork from collection:', error)
      throw error
    }
  }

  return {
    collections,
    currentCollection,
    isLoading,
    fetchCollections,
    createCollection,
    updateCollection,
    deleteCollection,
    fetchCollectionDetails,
    addArtworkToCollection,
    removeArtworkFromCollection
  }
})
