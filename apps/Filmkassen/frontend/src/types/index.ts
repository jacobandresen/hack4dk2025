// User types
export interface User {
  id: number
  username: string
  email: string
  created_at: string
}

export interface UserCreate {
  username: string
  email: string
  password: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface UserResponse {
  user: User
  access_token: string
  token_type: string
  message: string
}

// Movie types
export interface MovieSummary {
  id: number
  dfi_id: number
  title: string
  year?: number
  poster_url?: string
  director?: string
}

export interface Movie extends MovieSummary {
  cast?: string[]
  clips?: string[]
  videotek_url?: string
  description?: string
  cached_at?: string
}

// Director types
export interface Director {
  id: number
  name: string
  dfi_id?: string
  bio?: string
  cached_at?: string
}

// Collection types
export interface Collection {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at?: string
}

export interface CollectionCreate {
  name: string
  description?: string
}

export interface CollectionUpdate {
  name?: string
  description?: string
}

export interface CollectionMovie {
  id: number
  movie: MovieSummary
  note?: string
  added_at: string
}

export interface CollectionDetail extends Collection {
  movies: CollectionMovie[]
}

export interface CollectionMovieAdd {
  movie_id: number
  note?: string
}

export interface CollectionMovieUpdate {
  note?: string
}

// API Response types
export interface SearchResponse<T> {
  movies?: T[]
  directors?: T[]
  total: number
}

export interface ErrorResponse {
  detail: string
  error_code?: string
}
