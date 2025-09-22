# Filmkassen
En webapp der kan bruges til at søge efter film via DFI's api og gruppere film i filmkasser skabt af brugere.

## Features
- Søg efter film via DFI API
- Vis filmdetaljer med plakater og klip
- Opret og administrer filmkasser
- Tilføj film til filmkasser med noter
- Søg efter film efter instruktør

## Teknisk Stack
- **Frontend**: Vue.js 3 + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: PostgreSQL
- **Containerization**: Docker Compose
- **Testing**: Playwright E2E tests + Python pytest

## Setup

### Forudsætninger
- Docker og Docker Compose
- Node.js (for Playwright tests)
- Python 3.11+ (for backend tests)

### 1. Opret .env fil
Opret en `.env` fil i roden af projektet med følgende indhold:

```env
# DFI API Configuration
DFI_API_BASE_URL=https://api.dfi.dk/v1
DFI_API_USERNAME=your_username_here
DFI_API_PASSWORD=your_password_here

# Database Configuration
POSTGRES_DB=filmkassen
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Security
SECRET_KEY=your-secret-key-here-change-in-production
```

**Vigtigt**: Kontakt DFI for at få et brugernavn og password til deres API.

### 2. Start applikationen
```bash
# Start alle services
npm run dev

# Eller direkte med docker-compose
docker-compose up --build
```

### 3. Åbn applikationen
Gå til http://localhost:3000 i din browser.

## Testing

### E2E Tests
```bash
# Installer Playwright
npm run install:playwright

# Kør E2E tests
npm run test:e2e
```

### Backend Tests
```bash
# Kør backend tests
npm run test:backend
```

## Accept Tests

### Docker Services
Alle docker services skal køre uden fejl. Tjek logs med:
```bash
docker-compose logs
```

### E2E Tests
Før du melder løsningen som færdig, skal du vise at disse tests virker:

1. **Søgning efter "Jagten"**: Test at du kan søge efter filmen "Jagten" og se mindst 1 resultat med en filmplakat
2. **Oprettelse af filmkasse "Danske film"**: Test at du kan oprette en bruger, oprette en filmkasse "Danske film", søge efter "Jagten" og tilføje den til filmkassen

Screenshots gemmes automatisk i `./screenshots/` folderen under testkørslen.

## Arkitektur
Se `docs/ARCHITECTURE.md` for detaljeret arkitektur beskrivelse.

## Datamodel
Se `docs/DATAMODEL.md` for datamodel beskrivelse.

## API Dokumentation
Når applikationen kører, kan du se API dokumentationen på:
- Swagger UI: http://localhost:3000/api/docs
- OpenAPI spec: `docs/openapi.yaml`





