# Kørsel af MitSMK

## Forudsætninger

- Docker og Docker Compose installeret
- Node.js (for Playwright tests)

## Start af applikationen

1. **Start alle services:**
   ```bash
   docker-compose up --build
   ```

2. **Åbn applikationen:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/swagger

## Test af applikationen

### E2E Tests med Playwright

1. **Installer Playwright:**
   ```bash
   npx playwright install
   ```

2. **Kør alle tests:**
   ```bash
   npm run test:e2e
   ```

3. **Kør specifikke tests:**
   ```bash
   # Test søgning efter "Amager"
   npm run test:artwork-search
   
   # Test brugerregistrering og login
   npm run test:user-login
   
   # Test samlingshåndtering
   npm run test:collections
   
   # Test alle acceptancetests
   npm run test:acceptance
   ```

### Manuel test af krav

1. **Søgning efter "Amager":**
   - Gå til http://localhost:3000
   - Søg efter "Amager"
   - Verificer at der er mindst 1 resultat med billede

2. **Oprettelse af bruger og samling "Amagerkana":**
   - Klik på "Opret konto"
   - Opret en bruger
   - Gå til "Mine samlinger"
   - Opret samling "Amagerkana"

3. **Tilføjelse af kunstværk til samling:**
   - Søg efter "Amager"
   - Klik på første resultat
   - Vælg "Amagerkana" samling
   - Tilføj kunstværket
   - Gå til samlingen og verificer at kunstværket er der

## Fejlfinding

### Docker services kører ikke
```bash
# Tjek status af services
docker-compose ps

# Se logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database
```

### Database problemer
```bash
# Genstart database
docker-compose restart database

# Slet og genopret database
docker-compose down -v
docker-compose up --build
```

### Frontend problemer
```bash
# Genstart frontend
docker-compose restart frontend

# Tjek frontend logs
docker-compose logs frontend
```

### Backend problemer
```bash
# Genstart backend
docker-compose restart backend

# Tjek backend logs
docker-compose logs backend
```

## Struktur

```
MitSMK/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── ...
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/         # Page views
│   │   ├── stores/        # Pinia stores
│   │   └── ...
│   ├── package.json
│   └── Dockerfile
├── tests/                  # Playwright tests
│   ├── acceptance-tests.spec.ts
│   ├── artwork-search.spec.ts
│   └── ...
├── docs/                   # Dokumentation
│   ├── ARCHITECTURE.md
│   └── DATAMODEL.md
└── docker-compose.yml
```

