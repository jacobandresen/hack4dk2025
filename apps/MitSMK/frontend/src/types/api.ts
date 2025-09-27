export interface User {
  id: string
  username: string
  email: string
  created_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Artwork {
  id: string
  object_number: string
  title?: string
  year?: string
  artist_name?: string
  image_thumbnail?: string
  image_iiif_id?: string
  public_domain: boolean
  object_names?: string[]
  has_image: boolean
  cached_at: string
}

export interface ArtworkSearchResponse {
  artworks: Artwork[]
  total: number
  offset: number
  limit: number
}

export interface Collection {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface CollectionItem {
  id: string
  artwork: Artwork
  note?: string
  added_at: string
}

export interface CollectionDetails extends Collection {
  artworks: CollectionItem[]
}

export interface CollectionCreate {
  name: string
  description?: string
}

export interface CollectionUpdate {
  name: string
  description?: string
}

export interface CollectionItemCreate {
  artwork_id: string
  note?: string
}

