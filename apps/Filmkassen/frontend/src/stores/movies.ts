import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { MovieSummary, Movie, Director } from '../types'
import { moviesApi, directorsApi } from '../services/api'

export const useMoviesStore = defineStore('movies', () => {
  const searchResults = ref<MovieSummary[]>([])
  const currentMovie = ref<Movie | null>(null)
  const currentDirector = ref<Director | null>(null)
  const directorMovies = ref<MovieSummary[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const searchMovies = async (title: string, director?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await moviesApi.search(title, director)
      searchResults.value = response.movies || []
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Søgning fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getMovieDetails = async (movieId: number) => {
    loading.value = true
    error.value = null
    
    try {
      console.log('MoviesStore: Fetching movie details for ID:', movieId)
      const movie = await moviesApi.getDetails(movieId)
      console.log('MoviesStore: Received movie data:', movie)
      currentMovie.value = movie
      return movie
    } catch (err: any) {
      console.error('MoviesStore: Error fetching movie details:', err)
      error.value = err.response?.data?.detail || 'Hentning af filmdetaljer fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const searchDirectors = async (name: string) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await directorsApi.search(name)
      return response.directors || []
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Søgning efter instruktør fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const getDirectorMovies = async (directorId: number) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await directorsApi.getMovies(directorId)
      currentDirector.value = response.director
      directorMovies.value = response.movies
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Hentning af instruktørs film fejlede'
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearSearchResults = () => {
    searchResults.value = []
  }

  const clearCurrentMovie = () => {
    currentMovie.value = null
  }

  const clearCurrentDirector = () => {
    currentDirector.value = null
    directorMovies.value = []
  }

  const clearError = () => {
    error.value = null
  }

  return {
    searchResults,
    currentMovie,
    currentDirector,
    directorMovies,
    loading,
    error,
    searchMovies,
    getMovieDetails,
    searchDirectors,
    getDirectorMovies,
    clearSearchResults,
    clearCurrentMovie,
    clearCurrentDirector,
    clearError
  }
})
