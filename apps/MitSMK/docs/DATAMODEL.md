# MitSMK Datamodel

## Overordnet beskrivelse

Datamodellen understøtter brugere der kan søge efter kunstværker og oprette personlige samlinger. Data kommer primært fra SMK's API og caches lokalt for bedre performance.

## Entiteter

### 1. Bruger (User)
Repræsenterer en registreret bruger af systemet.

**Attributter:**
- `id`: Unikt identifikationsnummer (UUID)
- `username`: Brugernavn (unik)
- `email`: E-mail adresse (unik)
- `password_hash`: Krypteret adgangskode
- `created_at`: Oprettelsesdato
- `updated_at`: Sidste opdatering

**Eksempel:**
```
id: "123e4567-e89b-12d3-a456-426614174000"
username: "kunstelsker123"
email: "bruger@example.com"
password_hash: "$2b$12$..."
created_at: "2024-01-15T10:30:00Z"
```

### 2. Kunstværk (Artwork)
Repræsenterer et kunstværk fra SMK's samling.

**Attributter:**
- `id`: Unikt identifikationsnummer (UUID)
- `object_number`: SMK's inventarnummer (unik)
- `title`: Titel på kunstværket
- `year`: Årstal for kunstværket
- `artist_name`: Kunstnerens navn
- `image_thumbnail`: URL til thumbnail billede
- `image_iiif_id`: IIIF ID til højopløseligt billede
- `public_domain`: Om værket er i public domain
- `object_names`: Type af kunstværk (f.eks. "maleri")
- `has_image`: Om værket har et billede
- `cached_at`: Hvornår data blev cachelagret
- `raw_data`: Fuldstændig JSON data fra SMK API

**Eksempel:**
```
id: "456e7890-e89b-12d3-a456-426614174001"
object_number: "KMS1"
title: "Amager"
year: "1920"
artist_name: "Jens Ferdinand Willumsen"
image_thumbnail: "https://api.smk.dk/api/v1/images/thumbnail/..."
image_iiif_id: "https://api.smk.dk/api/v1/images/iiif/..."
public_domain: true
object_names: ["maleri"]
has_image: true
cached_at: "2024-01-15T10:30:00Z"
```

### 3. Samling (Collection)
Repræsenterer en brugeres personlige samling af kunstværker.

**Attributter:**
- `id`: Unikt identifikationsnummer (UUID)
- `name`: Navn på samlingen
- `description`: Beskrivelse af samlingen
- `user_id`: ID på ejeren af samlingen
- `created_at`: Oprettelsesdato
- `updated_at`: Sidste opdatering

**Eksempel:**
```
id: "789e0123-e89b-12d3-a456-426614174002"
name: "Amagerkana"
description: "Samling af Amager-relaterede kunstværker"
user_id: "123e4567-e89b-12d3-a456-426614174000"
created_at: "2024-01-15T11:00:00Z"
```

### 4. Samlingsindhold (CollectionItem)
Repræsenterer et kunstværk i en samling med brugerens note.

**Attributter:**
- `id`: Unikt identifikationsnummer (UUID)
- `collection_id`: ID på samlingen
- `artwork_id`: ID på kunstværket
- `note`: Brugerens note til kunstværket
- `added_at`: Dato for tilføjelse til samlingen

**Eksempel:**
```
id: "012e3456-e89b-12d3-a456-426614174003"
collection_id: "789e0123-e89b-12d3-a456-426614174002"
artwork_id: "456e7890-e89b-12d3-a456-426614174001"
note: "Fantastisk maleri af Amager"
added_at: "2024-01-15T11:15:00Z"
```

## Relationer

- **Bruger** → **Samling**: En-til-mange (en bruger kan have mange samlinger)
- **Samling** → **Samlingsindhold**: En-til-mange (en samling kan indeholde mange kunstværker)
- **Kunstværk** → **Samlingsindhold**: En-til-mange (et kunstværk kan være i mange samlinger)
- **Bruger** → **Samlingsindhold**: En-til-mange (via samlinger)

## Mapping til SMK API

### Søgning
SMK API søgning mappes til:
- `keys` parameter: Brugerens søgetekst
- `offset`: Paginering
- `rows`: Antal resultater
- `filters`: Filtrering (f.eks. `[has_image:true]`)

### Kunstværk data
SMK API kunstværk mappes til:
- `object_number` → `object_number`
- `titles[0].title` → `title`
- `production_dates[0].year` → `year`
- `creators[0].name` → `artist_name`
- `image_thumbnail` → `image_thumbnail`
- `image_iiif_id` → `image_iiif_id`
- `public_domain` → `public_domain`
- `object_names` → `object_names`
- `has_image` → `has_image`

## Caching strategi

- Kunstværk data caches i PostgreSQL når det hentes fra SMK API
- Cache opdateres ikke automatisk - ny data hentes kun ved nye søgninger
- Cached data inkluderer fuld JSON fra SMK API for fremtidig brug

