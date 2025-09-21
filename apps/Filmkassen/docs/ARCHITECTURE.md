# Filmkassen Arkitektur

## Oversigt
Filmkassen er en webapplikation der giver brugere mulighed for at søge efter film via DFI's API og organisere dem i personlige filmkasser.

## C4 Diagram - System Context

```
                    ┌─────────────────┐
                    │                 │
                    │   DFI API       │
                    │  (External)     │
                    │                 │
                    └─────────┬───────┘
                              │
                              │ HTTPS
                              │
                    ┌─────────▼───────┐
                    │                 │
                    │   Filmkassen    │
                    │   Web App       │
                    │                 │
                    └─────────┬───────┘
                              │
                              │ Browser
                              │
                    ┌─────────▼───────┐
                    │                 │
                    │   End User      │
                    │                 │
                    └─────────────────┘
```

## C4 Diagram - Container View

```
┌─────────────────────────────────────────────────────────────────┐
│                        Filmkassen System                        │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │                 │    │                 │    │             │ │
│  │   Vue Frontend  │    │  FastAPI        │    │ PostgreSQL  │ │
│  │   (Port 3000)   │    │  Backend        │    │ Database    │ │
│  │                 │    │  (Port 8000)    │    │ (Port 5432) │ │
│  │                 │    │                 │    │             │ │
│  └─────────┬───────┘    └─────────┬───────┘    └─────────────┘ │
│            │                      │                            │
│            │ HTTP/API Proxy       │ SQL                        │
│            │                      │                            │
│            └──────────────────────┼────────────────────────────┘
│                                   │
│                                   │ HTTPS
│                                   │
│  ┌─────────────────────────────────▼─────────────────────────┐ │
│  │                                                           │ │
│  │              DFI API (External)                          │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Services

### Frontend (Vue.js)
- **Port**: 3000
- **Teknologi**: Vue 3, TypeScript, Vite
- **Funktioner**:
  - Film søgning
  - Film detaljer visning
  - Bruger authentication
  - Filmkasser management
  - Responsive design med DFI-inspireret styling

### Backend (FastAPI)
- **Port**: 8000 (internt i Docker)
- **Teknologi**: Python, FastAPI, SQLAlchemy
- **Funktioner**:
  - DFI API integration
  - Bruger authentication
  - Filmkasser CRUD operations
  - Data caching
  - OpenAPI/Swagger dokumentation

### Database (PostgreSQL)
- **Port**: 5432 (internt i Docker)
- **Teknologi**: PostgreSQL
- **Funktioner**:
  - Bruger data
  - Filmkasser data
  - Cached film data fra DFI API

## Data Flow

1. **Film Søgning**:
   - Bruger indtaster søgeterm i frontend
   - Frontend sender request til backend via proxy
   - Backend kalder DFI API
   - Resultater caches i database
   - Frontend viser resultater

2. **Film Detaljer**:
   - Bruger klikker på film
   - Frontend henter detaljer fra backend
   - Backend henter fra cache eller DFI API
   - Detaljer vises med plakat og metadata

3. **Filmkasser**:
   - Loggede brugere kan oprette filmkasser
   - Film kan tilføjes til filmkasser med noter
   - Filmkasser vises som accordion med DVD-kasse design

## Tekniske Beslutninger

- **Hexagonal Architecture**: Modulær opdeling med lav kompleksitet
- **Docker Compose**: Alle services kører i containere
- **API Proxy**: Frontend proxyer /api til backend
- **CORS**: Konfigureret til lokal udvikling
- **Caching**: Alle DFI API resultater caches lokalt
- **TypeScript**: Type safety på frontend
- **OpenAPI**: Automatisk API dokumentation
