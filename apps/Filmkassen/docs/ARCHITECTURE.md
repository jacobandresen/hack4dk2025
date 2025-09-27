# Arkitektur - Filmkassen

## Systemoversigt

Filmkassen er en webapplikation der giver brugere mulighed for at søge efter film via DFI's API og organisere dem i personlige filmkasser.

## C4 Model - System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Filmkassen System                        │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   Web Browser   │    │   Vue Frontend  │    │  FastAPI    │ │
│  │                 │◄──►│                 │◄──►│  Backend    │ │
│  │   (User)        │    │   (Port 3000)   │    │ (Port 8000) │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│                                                      │         │
│                                                      ▼         │
│                                            ┌─────────────────┐ │
│                                            │   PostgreSQL    │ │
│                                            │   Database      │ │
│                                            │   (Port 5432)   │ │
│                                            └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │   DFI API       │
                    │   (External)    │
                    │   api.dfi.dk    │
                    └─────────────────┘
```

## Komponenter

### Frontend (Vue.js)
- **Port**: 3000
- **Funktioner**:
  - Film søgning
  - Film detaljer visning
  - Bruger login/registrering
  - Filmkasser management
  - Instruktør søgning

### Backend (FastAPI)
- **Port**: 8000 (internt)
- **Funktioner**:
  - DFI API integration
  - Bruger authentication
  - Filmkasser CRUD operations
  - Data caching
  - OpenAPI/Swagger dokumentation

### Database (PostgreSQL)
- **Port**: 5432
- **Funktioner**:
  - Bruger data
  - Filmkasser og film relationer
  - Cached film data fra DFI API
  - Session management

### External API (DFI)
- **URL**: api.dfi.dk
- **Funktioner**:
  - Film søgning
  - Film detaljer
  - Billeder og metadata

## Docker Compose Setup

```yaml
services:
  database:
    image: postgres:15
    environment:
      POSTGRES_DB: filmkassen
      POSTGRES_USER: filmkassen
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://filmkassen:password@database:5432/filmkassen
      DFI_API_BASE_URL: https://api.dfi.dk/v1
    depends_on:
      - database

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_BASE_URL: http://localhost:3000/api
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

## Data Flow

1. **Film Søgning**:
   - Bruger indtaster søgeterm i frontend
   - Frontend sender request til backend via proxy
   - Backend henter data fra DFI API
   - Backend cacher data i PostgreSQL
   - Frontend viser søgeresultater

2. **Film Detaljer**:
   - Bruger klikker på film i søgeresultater
   - Frontend henter detaljer fra backend
   - Backend returnerer cached eller nye data fra DFI API
   - Frontend viser film detaljer med billeder

3. **Filmkasser**:
   - Logged-in bruger opretter filmkasse
   - Data gemmes i PostgreSQL
   - Film tilføjes til filmkasse med note
   - Frontend viser filmkasser som accordion

## Sikkerhed

- CORS konfigureret for lokal udvikling
- Bruger authentication via sessions
- Ingen passwords i Docker Compose
- Environment variables for sensitive data

## Caching Strategi

- Alle DFI API resultater caches i PostgreSQL
- Cache TTL baseret på data type
- Automatisk cache invalidation ved opdateringer
