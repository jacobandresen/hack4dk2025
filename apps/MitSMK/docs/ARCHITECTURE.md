# MitSMK Arkitektur

## Overordnet arkitektur

MitSMK er en webapplikation der giver brugere mulighed for at søge efter kunstværker via SMK's API og oprette personlige samlinger. Systemet er bygget med en moderne fullstack arkitektur med separation af concerns.

## Teknisk stack

- **Frontend**: Vue.js 3 med TypeScript
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Containerization**: Docker Compose
- **Testing**: Playwright (E2E), Jest (Unit), Pytest (Backend)

## Systemkomponenter

### 1. Frontend (Vue.js)
- **Søgefunktionalitet**: Interface til at søge efter kunstværker
- **Kunstværkvisning**: Detaljeret visning af kunstværker med billeder
- **Brugerautentificering**: Login og registrering
- **Samlingshåndtering**: Oprettelse og administration af kunstsamlinger
- **Responsivt design**: Inspireret af SMK's design med Pinterest-lignende layout

### 2. Backend (FastAPI)
- **SMK API Integration**: Proxy og caching af SMK's kunstværk API
- **Brugerhåndtering**: Autentificering og autorisering
- **Samlingslogik**: CRUD operationer for brugeres samlinger
- **Caching**: PostgreSQL-baseret caching af SMK data
- **OpenAPI**: Swagger dokumentation på /swagger

### 3. Database (PostgreSQL)
- **Brugerdata**: Brugere og deres autentificeringsoplysninger
- **Samlinger**: Brugeres kunstsamlinger
- **Kunstværkdata**: Cached data fra SMK API
- **Samlingsindhold**: Mapping mellem samlinger og kunstværker

## API Integration

### SMK API
- **Base URL**: https://api.smk.dk/api/v1/
- **Søgning**: `/art/search/` med keys parameter
- **Detaljer**: `/art/` med object_number
- **Billeder**: image_thumbnail og image_iiif_id attributter

## Sikkerhed og CORS

- CORS konfigureret for lokal udvikling
- Proxy setup mellem frontend og backend
- Sikker brugerautentificering

## Deployment

Systemet kører i Docker containers med:
- Frontend på port 3000 (med proxy til backend)
- Backend på port 8000 (kun tilgængelig internt)
- PostgreSQL database (kun tilgængelig internt)

## Systemarkitektur diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser       │    │   Frontend      │    │   Backend       │
│   (User)        │◄──►│   (Vue.js)      │◄──►│   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Proxy         │    │   PostgreSQL    │
                       │   /api → :8000  │    │   Database      │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   SMK API       │
                                              │   (External)    │
                                              └─────────────────┘
```

## Teststrategi

- **Unit tests**: Frontend komponenter og backend funktioner
- **Integration tests**: API endpoints og database operationer
- **E2E tests**: Fuldstændige brugerflows med Playwright
