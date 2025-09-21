# Filmkassen
En webapp der kan bruges til at søge efter film via DFI's api og gruppere film i filmkasser skabt af brugere.

Features er beskrevet i FEATURES.md

Teknik er beskrevet i ../AGENTS.md .

## Brug af .env fil
Løsningen antager at der placeret en .env fil tilgængelig med flg indstillinger:

DFI_API_BASE_URL=https://api.dfi.dk/v1
DFI_API_USERNAME=[Brugernavn]
DFI_API_PASSWORD=[password]
POSTGRES_DB=filmkassen
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres


## Accept tests 

### Docker services

Alle docker services skal køre. Der må ikke fremgå fejl i log fra backend,frontend og database services i docker.


### E2E tests

Før at du melder at løsningen virker skal du vise mig at disse tests virker.

For hver E2E test skal du tage et screenshot og gemme dem i folderen ./screenshots.

### Søgning efter detaljer for "Jagten"
Test at du kan søge efter filmen "Jagten" og se at der er mindst 1 resultat med en filmplakat. 

Testen skal vise at der kan klikkes på søgesultatet og vise flere detaljer om filmen.

Tjek at den er instrueret af "Thomas Vinterberg" og at der er en synlig filmplakat.

### Oprettelse af filmkassen "Danske film"

Test at du kan oprette en bruger som kan oprette en filmkasse "Danske film"

Tjek at du kan søge efter filmen "Jagten" og tilføje den til filmkassen "Danske film"

Tjek at du kan se detaljerne om "Jagten" ved at klikke på "Jagten" i filmkassen "Danske film"





