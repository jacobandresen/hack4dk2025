import axios from 'axios'
import type {
  User, UserCreate, UserLogin, UserResponse,
  Movie, MovieSummary, Director,
  Collection, CollectionCreate, CollectionUpdate, CollectionDetail,
  CollectionMovie, CollectionMovieAdd, CollectionMovieUpdate,
  SearchResponse
} from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    console.log('API Interceptor: Adding token to request:', token ? 'Token found' : 'No token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('API Interceptor: Authorization header set:', config.headers.Authorization)
    }
    return config
  },
  (error) => {
    console.error('API Interceptor: Request error:', error)
    return Promise.reject(error)
  }
)

// Request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  register: async (userData: UserCreate): Promise<UserResponse> => {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  login: async (userData: UserLogin): Promise<UserResponse> => {
    const response = await api.post('/auth/login', userData)
    return response.data
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout')
  }
}

// Movies API
export const moviesApi = {
  search: async (title: string, director?: string): Promise<SearchResponse<MovieSummary>> => {
    const params: any = { title }
    if (director) params.director = director
    
    const response = await api.get('/movies/search', { params })
    return response.data
  },

  getDetails: async (movieId: number): Promise<Movie> => {
    const response = await api.get(`/movies/${movieId}`)
    return response.data
  }
}

// Directors API
export const directorsApi = {
  search: async (name: string): Promise<SearchResponse<Director>> => {
    const response = await api.get('/directors/search', { params: { name } })
    return response.data
  },

  getMovies: async (directorId: number): Promise<{ director: Director; movies: MovieSummary[] }> => {
    const response = await api.get(`/directors/${directorId}/movies`)
    return response.data
  }
}

// Collections API
export const collectionsApi = {
  getAll: async (): Promise<Collection[]> => {
    const response = await api.get('/collections')
    return response.data
  },

  create: async (collectionData: CollectionCreate): Promise<Collection> => {
    const response = await api.post('/collections', collectionData)
    return response.data
  },

  getDetails: async (collectionId: number): Promise<CollectionDetail> => {
    const response = await api.get(`/collections/${collectionId}`)
    return response.data
  },

  update: async (collectionId: number, collectionData: CollectionUpdate): Promise<Collection> => {
    const response = await api.put(`/collections/${collectionId}`, collectionData)
    return response.data
  },

  delete: async (collectionId: number): Promise<void> => {
    await api.delete(`/collections/${collectionId}`)
  },

  addMovie: async (collectionId: number, movieData: CollectionMovieAdd): Promise<CollectionMovie> => {
    const response = await api.post(`/collections/${collectionId}/movies`, movieData)
    return response.data
  },

  removeMovie: async (collectionId: number, movieId: number): Promise<void> => {
    await api.delete(`/collections/${collectionId}/movies/${movieId}`)
  },

  updateMovieNote: async (collectionId: number, movieId: number, movieData: CollectionMovieUpdate): Promise<CollectionMovie> => {
    const response = await api.put(`/collections/${collectionId}/movies/${movieId}`, movieData)
    return response.data
  }
}

export default api
