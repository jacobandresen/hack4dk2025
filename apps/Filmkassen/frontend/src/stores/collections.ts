import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Collection, CollectionCreate, CollectionUpdate, CollectionDetail, CollectionMovieAdd, CollectionMovieUpdate } from '../types'
import { collectionsApi } from '../services/api'

export const useCollectionsStore = defineStore('collections', () => {
  const collections = ref<Collection[]>([])
  const currentCollection = ref<CollectionDetail | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchCollections = async () => {
    loading.value = true
    error.value = null
    
    try {
      console.log('CollectionsStore: Fetching collections...')
      console.log('CollectionsStore: Current token in localStorage:', localStorage.getItem('access_token'))
      const data = await collectionsApi.getAll()
      console.log('CollectionsStore: Received collections:', data)
      collections.value = data
      console.log('CollectionsStore: Updated collections state:', collections.value)
      return data
    } catch (err: any) {
      console.error('CollectionsStore: Error fetching collections:', err)
      console.error('CollectionsStore: Error details:', err.response)
      console.error('CollectionsStore: Error status:', err.response?.status)
      console.error('CollectionsStore: Error data:', err.response?.data)
      console.error('CollectionsStore: Error message:', err.message)
      if (err.response?.status === 401) {
        console.error('CollectionsStore: Authentication failed - user may need to log in again')
        error.value = 'Du skal logge ind for at se dine filmkasser'
      } else {
        error.value = err.response?.data?.detail || 'Hentning af filmkasser fejlede'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  const createCollection = async (collectionData: CollectionCreate) => {
    loading.value = true
    error.value = null
    
    try {
      console.log('CollectionsStore: Creating collection:', collectionData)
      const collection = await collectionsApi.create(collectionData)
      console.log('CollectionsStore: Collection created:', collection)
      collections.value.push(collection)
      return collection
    } catch (err: any) {
      console.error('CollectionsStore: Error creating collection:', err)
      error.value = err.response?.data?.detail || 'Oprettelse af filmkasse fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getCollectionDetails = async (collectionId: number) => {
    loading.value = true
    error.value = null
    
    try {
      const collection = await collectionsApi.getDetails(collectionId)
      currentCollection.value = collection
      return collection
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Hentning af filmkasse detaljer fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateCollection = async (collectionId: number, collectionData: CollectionUpdate) => {
    loading.value = true
    error.value = null
    
    try {
      const collection = await collectionsApi.update(collectionId, collectionData)
      const index = collections.value.findIndex(c => c.id === collectionId)
      if (index !== -1) {
        collections.value[index] = collection
      }
      return collection
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Opdatering af filmkasse fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteCollection = async (collectionId: number) => {
    loading.value = true
    error.value = null
    
    try {
      await collectionsApi.delete(collectionId)
      collections.value = collections.value.filter(c => c.id !== collectionId)
      if (currentCollection.value?.id === collectionId) {
        currentCollection.value = null
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Sletning af filmkasse fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const addMovieToCollection = async (collectionId: number, movieData: CollectionMovieAdd) => {
    loading.value = true
    error.value = null
    
    try {
      const collectionMovie = await collectionsApi.addMovie(collectionId, movieData)
      
      // Update current collection if it's the one being modified
      if (currentCollection.value?.id === collectionId) {
        currentCollection.value.movies.push(collectionMovie)
      }
      
      return collectionMovie
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Tilføjelse af film til filmkasse fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const removeMovieFromCollection = async (collectionId: number, movieId: number) => {
    loading.value = true
    error.value = null
    
    try {
      await collectionsApi.removeMovie(collectionId, movieId)
      
      // Update current collection if it's the one being modified
      if (currentCollection.value?.id === collectionId) {
        currentCollection.value.movies = currentCollection.value.movies.filter(
          cm => cm.movie.id !== movieId
        )
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Fjernelse af film fra filmkasse fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateMovieNote = async (collectionId: number, movieId: number, movieData: CollectionMovieUpdate) => {
    loading.value = true
    error.value = null
    
    try {
      const collectionMovie = await collectionsApi.updateMovieNote(collectionId, movieId, movieData)
      
      // Update current collection if it's the one being modified
      if (currentCollection.value?.id === collectionId) {
        const index = currentCollection.value.movies.findIndex(cm => cm.movie.id === movieId)
        if (index !== -1) {
          currentCollection.value.movies[index] = collectionMovie
        }
      }
      
      return collectionMovie
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Opdatering af filmnote fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearCurrentCollection = () => {
    currentCollection.value = null
  }

  const clearError = () => {
    error.value = null
  }

  return {
    collections,
    currentCollection,
    loading,
    error,
    fetchCollections,
    createCollection,
    getCollectionDetails,
    updateCollection,
    deleteCollection,
    addMovieToCollection,
    removeMovieFromCollection,
    updateMovieNote,
    clearCurrentCollection,
    clearError
  }
})
