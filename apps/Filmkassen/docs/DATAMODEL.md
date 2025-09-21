# Filmkassen Datamodel

## Oversigt
Datamodellen beskriver de centrale entiteter og deres relationer i Filmkassen systemet. Modellen er designet til at understøtte alle funktionelle krav og integrere med DFI API'et.

## Entiteter

### Bruger (User)
**Beskrivelse**: Repræsenterer en registreret bruger af systemet.

**Attributter**:
- `id` (UUID): Unik identifikator for brugeren
- `username` (String): Unikt brugernavn
- `email` (String): E-mail adresse
- `password_hash` (String): Krypteret adgangskode
- `created_at` (DateTime): Oprettelsesdato
- `updated_at` (DateTime): Seneste opdatering

**Eksempel**:
```
id: 550e8400-e29b-41d4-a716-446655440000
username: "filmfan123"
email: "filmfan@example.com"
password_hash: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J5..."
created_at: "2024-01-15T10:30:00Z"
updated_at: "2024-01-15T10:30:00Z"
```

### Film (Movie)
**Beskrivelse**: Repræsenterer en film fra DFI API'et med cached data.

**Attributter**:
- `id` (Integer): DFI film ID (primær nøgle)
- `title` (String): Filmtitel
- `year` (Integer): Udgivelsesår
- `director` (String): Instruktør
- `poster_url` (String): URL til filmplakat
- `description` (Text): Filmbeskrivelse
- `cast` (JSON): Medvirkende som JSON array
- `clips` (JSON): Filmklip som JSON array med billeder
- `videotek_url` (String): Link til videoteket (hvis tilgængelig)
- `cached_at` (DateTime): Hvornår data blev cachet
- `created_at` (DateTime): Oprettelsesdato i systemet
- `updated_at` (DateTime): Seneste opdatering

**Eksempel**:
```
id: 74245
title: "Jagten"
year: 2012
director: "Thomas Vinterberg"
poster_url: "https://api.dfi.dk/v1/film/74245/poster.jpg"
description: "En lærer bliver falsk anklaget for at have begået overgreb..."
cast: ["Mads Mikkelsen", "Thomas Bo Larsen", "Annika Wedderkopp"]
clips: [
  {"url": "https://api.dfi.dk/v1/film/74245/clip1.jpg", "description": "Scene fra skolen"},
  {"url": "https://api.dfi.dk/v1/film/74245/clip2.jpg", "description": "Konfrontation"}
]
videotek_url: "https://www.dfi.dk/videotek/film/jagten"
cached_at: "2024-01-15T10:30:00Z"
created_at: "2024-01-15T10:30:00Z"
updated_at: "2024-01-15T10:30:00Z"
```

### Filmkasse (MovieCollection)
**Beskrivelse**: Repræsenterer en samling af film oprettet af en bruger.

**Attributter**:
- `id` (UUID): Unik identifikator for filmkassen
- `name` (String): Navn på filmkassen
- `description` (Text): Beskrivelse af filmkassen
- `user_id` (UUID): ID på brugeren der ejer filmkassen
- `created_at` (DateTime): Oprettelsesdato
- `updated_at` (DateTime): Seneste opdatering

**Eksempel**:
```
id: 123e4567-e89b-12d3-a456-426614174000
name: "Danske film"
description: "Mine yndlings danske film"
user_id: 550e8400-e29b-41d4-a716-446655440000
created_at: "2024-01-15T10:30:00Z"
updated_at: "2024-01-15T10:30:00Z"
```

### Filmkasse Film (MovieCollectionItem)
**Beskrivelse**: Repræsenterer en film der er tilføjet til en filmkasse med brugerens note.

**Attributter**:
- `id` (UUID): Unik identifikator for tilføjelsen
- `collection_id` (UUID): ID på filmkassen
- `movie_id` (Integer): DFI film ID
- `user_note` (Text): Brugerens note til filmen
- `added_at` (DateTime): Dato for tilføjelse
- `created_at` (DateTime): Oprettelsesdato
- `updated_at` (DateTime): Seneste opdatering

**Eksempel**:
```
id: 987fcdeb-51a2-43d1-9f12-345678901234
collection_id: 123e4567-e89b-12d3-a456-426614174000
movie_id: 74245
user_note: "Fantastisk film med stærk fortælling om mobning"
added_at: "2024-01-15T10:30:00Z"
created_at: "2024-01-15T10:30:00Z"
updated_at: "2024-01-15T10:30:00Z"
```

## Relationer

### Bruger → Filmkasser
- **Type**: One-to-Many
- **Beskrivelse**: En bruger kan have flere filmkasser
- **Foreign Key**: `MovieCollection.user_id` → `User.id`

### Filmkasse → Filmkasse Film
- **Type**: One-to-Many
- **Beskrivelse**: En filmkasse kan indeholde flere film
- **Foreign Key**: `MovieCollectionItem.collection_id` → `MovieCollection.id`

### Film → Filmkasse Film
- **Type**: One-to-Many
- **Beskrivelse**: En film kan være i flere filmkasser
- **Foreign Key**: `MovieCollectionItem.movie_id` → `Movie.id`

## Datamodel Analyse mod Funktionelle Krav

### Film Søgning
✅ **Understøttet**: Film entiteten caches alle nødvendige data fra DFI API
- Titel, år, instruktør, plakat, beskrivelse, medvirkende, klip

### Film Detaljer
✅ **Understøttet**: Alle detaljer gemmes i Film entiteten
- Plakat, instruktør (med link til søgning), medvirkende, klip, videotek link

### Instruktør Søgning
✅ **Understøttet**: Kan søge i Film.director felt og vise relaterede film

### Bruger Authentication
✅ **Understøttet**: User entiteten med username/email og password_hash

### Filmkasser
✅ **Understøttet**: MovieCollection og MovieCollectionItem entiteter
- Brugere kan oprette filmkasser
- Film kan tilføjes med noter
- Film kan slettes fra filmkasser

### Caching
✅ **Understøttet**: Film entiteten caches DFI API data med cached_at timestamp

## API Mapping

### DFI API → Lokal Film Entitet
- `id` → `id`
- `title` → `title`
- `year` → `year`
- `director` → `director`
- `poster` → `poster_url`
- `description` → `description`
- `cast` → `cast` (JSON array)
- `clips` → `clips` (JSON array)
- `videotek_url` → `videotek_url` (konstrueret)

## Database Indekser

### Performance Optimering
- `User.username` (UNIQUE)
- `User.email` (UNIQUE)
- `Movie.id` (PRIMARY KEY)
- `Movie.title` (INDEX for søgning)
- `Movie.director` (INDEX for instruktør søgning)
- `MovieCollection.user_id` (INDEX for bruger filmkasser)
- `MovieCollectionItem.collection_id` (INDEX for filmkasse film)
- `MovieCollectionItem.movie_id` (INDEX for film søgning)
