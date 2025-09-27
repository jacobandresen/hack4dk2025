# Kørsel af Filmkassen

## Hurtig start

1. **Start alle services:**
   ```bash
   ./test-setup.sh
   ```

2. **Åbn applikationen:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API dokumentation: http://localhost:8000/swagger

## Manuel start

1. **Start Docker services:**
   ```bash
   docker-compose up --build
   ```

2. **I en ny terminal, kør E2E tests:**
   ```bash
   cd tests/e2e
   npm install
   npx playwright test --headed
   ```

## Test af funktionalitet

### Accept tests

1. **Søgning efter "Jagten":**
   - Gå til http://localhost:3000
   - Indtast "Jagten" i søgefeltet
   - Klik "Søg"
   - Verificer at der vises mindst 1 resultat med filmplakat

2. **Oprettelse af filmkasse "Danske film":**
   - Klik "Registrer" for at oprette en bruger
   - Log ind med den nye bruger
   - Gå til "Mine Filmkasser"
   - Opret en filmkasse med navnet "Danske film"
   - Søg efter "Jagten" og tilføj den til filmkassen

## Fejlfinding

### Tjek service status
```bash
docker-compose logs
```

### Genstart services
```bash
docker-compose down
docker-compose up --build
```

### Ryd op
```bash
docker-compose down -v
```

## Arkitektur

- **Frontend:** Vue.js på port 3000
- **Backend:** FastAPI på port 8000 (internt)
- **Database:** PostgreSQL på port 5432
- **Proxy:** Frontend proxier /api til backend

## API endpoints

- `GET /health` - Health check
- `GET /swagger` - API dokumentation
- `POST /auth/register` - Registrer bruger
- `POST /auth/login` - Log ind
- `GET /movies/search?title=jagten` - Søg film
- `GET /movies/{id}` - Hent filmdetaljer
- `GET /collections` - Hent filmkasser (kræver login)
- `POST /collections` - Opret filmkasse (kræver login)
