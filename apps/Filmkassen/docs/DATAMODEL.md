# Datamodel - Filmkassen

## Overordnet beskrivelse

Datamodellen understøtter en filmkasse applikation hvor brugere kan søge efter film via DFI's API og organisere dem i personlige samlinger.

## Entiteter

### Bruger (User)
**Beskrivelse**: Repræsenterer en registreret bruger af systemet

**Attributter**:
- `id` (Primær nøgle): Unikt identifikationsnummer
- `username` (Unik): Brugernavn til login
- `email` (Unik): E-mail adresse
- `password_hash`: Krypteret password
- `created_at`: Dato for oprettelse
- `updated_at`: Dato for sidste opdatering

**Eksempel**:
```
id: 1
username: "filmfan123"
email: "filmfan@example.com"
password_hash: "$2b$12$..."
created_at: "2024-01-15T10:30:00Z"
updated_at: "2024-01-15T10:30:00Z"
```

### Film (Movie)
**Beskrivelse**: Repræsenterer en film fra DFI's API med cached data

**Attributter**:
- `id` (Primær nøgle): Unikt identifikationsnummer
- `dfi_id` (Unik): ID fra DFI's API
- `title`: Filmtitel
- `year`: Udgivelsesår
- `poster_url`: URL til filmplakat
- `director`: Instruktør navn
- `cast`: Medvirkende (JSON array)
- `clips`: Billeder fra filmen (JSON array)
- `videotek_url`: Link til videoteket
- `description`: Beskrivelse af filmen
- `cached_at`: Dato for cache opdatering
- `created_at`: Dato for første cache

**Eksempel**:
```
id: 1
dfi_id: 74245
title: "Jagten"
year: 2012
poster_url: "https://api.dfi.dk/v1/film/74245/poster.jpg"
director: "Thomas Vinterberg"
cast: ["Mads Mikkelsen", "Thomas Bo Larsen", "Annika Wedderkopp"]
clips: ["https://api.dfi.dk/v1/film/74245/clip1.jpg", "..."]
videotek_url: "https://www.dfi.dk/videotek/film/jagten"
description: "En lærer bliver falsk anklaget for at have begået overgreb..."
cached_at: "2024-01-15T10:30:00Z"
created_at: "2024-01-15T10:30:00Z"
```

### Filmkasse (MovieCollection)
**Beskrivelse**: Repræsenterer en bruger's samling af film

**Attributter**:
- `id` (Primær nøgle): Unikt identifikationsnummer
- `user_id` (Fremmed nøgle): Refererer til Bruger
- `name`: Navn på filmkassen
- `description`: Beskrivelse af filmkassen
- `created_at`: Dato for oprettelse
- `updated_at`: Dato for sidste opdatering

**Eksempel**:
```
id: 1
user_id: 1
name: "Danske film"
description: "Mine yndlings danske film"
created_at: "2024-01-15T10:30:00Z"
updated_at: "2024-01-15T10:30:00Z"
```

### Filmkasse Film (CollectionMovie)
**Beskrivelse**: Repræsenterer en film i en filmkasse med bruger note

**Attributter**:
- `id` (Primær nøgle): Unikt identifikationsnummer
- `collection_id` (Fremmed nøgle): Refererer til Filmkasse
- `movie_id` (Fremmed nøgle): Refererer til Film
- `note`: Bruger's note til filmen
- `added_at`: Dato for tilføjelse til filmkassen

**Eksempel**:
```
id: 1
collection_id: 1
movie_id: 1
note: "Fantastisk film med stærk fortælling"
added_at: "2024-01-15T10:30:00Z"
```

### Instruktør (Director)
**Beskrivelse**: Repræsenterer en instruktør med cached data

**Attributter**:
- `id` (Primær nøgle): Unikt identifikationsnummer
- `name`: Instruktør navn
- `dfi_id`: ID fra DFI's API (hvis tilgængelig)
- `bio`: Biografi
- `cached_at`: Dato for cache opdatering
- `created_at`: Dato for første cache

**Eksempel**:
```
id: 1
name: "Thomas Vinterberg"
dfi_id: "director_123"
bio: "Dansk filminstruktør og manuskriptforfatter..."
cached_at: "2024-01-15T10:30:00Z"
created_at: "2024-01-15T10:30:00Z"
```

## Relationer

### Bruger → Filmkasse (1:N)
- En bruger kan have mange filmkasser
- En filmkasse tilhører kun én bruger

### Filmkasse → Film (M:N via CollectionMovie)
- En filmkasse kan indeholde mange film
- En film kan være i mange filmkasser
- CollectionMovie indeholder note og tilføjelsesdato

### Film → Instruktør (N:1)
- En film har én instruktør
- En instruktør kan have mange film

## Mapping til DFI API

### Film søgning
```
DFI API: GET /v1/film?Title=jagten
Mapping til: Movie.title, Movie.year, Movie.director, Movie.poster_url
```

### Film detaljer
```
DFI API: GET /v1/film/74245
Mapping til: Alle Movie attributter + Movie.clips, Movie.videotek_url
```

### Instruktør søgning
```
DFI API: GET /v1/person?Name=thomas%20vinterberg
Mapping til: Director.name, Director.bio
```

## Funktionelle krav analyse

### Film søgning uden login
✅ **Understøttet**: Movie entiteten cacher alle nødvendige data fra DFI API

### Film detaljer med billeder
✅ **Understøttet**: Movie.poster_url og Movie.clips indeholder billede URLs

### Bruger login/registrering
✅ **Understøttet**: User entiteten håndterer authentication

### Filmkasser med noter
✅ **Understøttet**: MovieCollection og CollectionMovie entiteter

### Instruktør søgning
✅ **Understøttet**: Director entitet med cached data

### Videotek link
✅ **Understøttet**: Movie.videotek_url attribut

## Cache strategi

- **Film data**: Caches ved første søgning, opdateres hvis ældre end 7 dage
- **Instruktør data**: Caches ved første søgning, opdateres hvis ældre end 30 dage
- **Bruger data**: Ingen cache, altid live data
- **Filmkasser**: Ingen cache, altid live data
