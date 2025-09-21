# MitSMK
En webapp der kan bruges til at søge efter kunstværker via SMK's api og gruppere dem i samlinger skabt af brugere.

Features er beskrevet i FEATURES.md

Teknik er beskrevet i FULLSTACK.md .

BEMÆRK: SMK API'et tager imod søgestrengen i "keys" attributten.
BEMÆRK: DET ER VIGTIGT at du kan vise billeder.

## Brug af .env fil
Løsningen antager at der placeret en .env fil tilgængelig med flg indstillinger:

POSTGRES_DB=filmkassen
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres


## Accept tests 

### Docker services

Alle docker services skal køre. Der må ikke fremgå fejl i log fra backend,frontend og database services i docker.


### E2E tests

Før at du melder at løsningen virker skal du vise mig at disse tests virker.

### Søgning efter "Amager"
Test at du kan søge efter filmen "Amager" og se at der er mindst 1 resultat med 1 billede tilknyttet. 

BEMÆRK: Du har fejlet , hvis der står "Intet billede" på samtlige søgeresultater. Det er vigtigt at du kan vise billeder.


### Oprettelse af filmkassen "Amagerkana"

Test at du kan oprette en bruger som kan oprette en samling "Amagerkana"

Tjek at du kan søge efter "Amager" og tilføje det første billede til samlingen "Amagerkana". Tjek at billedet kan vises.

Tjek at du kan se detaljerne om det første billede i samlingen "Amagerkana"



