
# Features

## Design

Brug designet fra DFI's hjemmeside her https://www.dfi.dk .

Sørg for at det er nemt at læse hvad der står på skærmen. Tænk på at teksten skal fremstå tydeligt foran baggrunden.


## Brug af API

Brug DFI apiet som beskrevet her : https://api.dfi.dk/documentation/dfiapi.pdf

Tag udgangspunkt i eksemplerne her først:

Hent detaljer om en film med id = 74245
https://api.dfi.dk/v1/film/74245

Søg efter film der starter med  "Jagten":
https://api.dfi.dk/v1/film?Title=jagten

Hvis der står noget andet i pdf'en skal du bruge eksemplerne først.


## Forside

Forsiden starter med at en søgeform, hvor der kan søges efter en film. Bemærk at søgeformen kun skal være der 1 gang.  Når der er blevet søgt , så skal der vises søgeresultater.  Det skal være muligt at køre en ny søgning som overskriver gamle søgeresultater.

Ved tryk på et søgeresultat skal der vises yderligere detaljer om filmen.

## Søgning efter film

Brugeren kan søge efter film uden at være logget ind.

Medtag kun titlen i søgefeltet og en knap hvor der står søg. Der skal ikke være andre knapper i søgeformen.

Når der vises resultater skal der vises en titel, et årstal, en filmplakat og instruktøren.

Når der klikkes på søgeresultatet skal der åbnes en side med flere detaljer om filmen (se "Hent Film Detaljer"). 

BEMÆRK: DET ER VIGTIGT AT DU KAN VISE ET BILLEDE FOR FILMEN.

BEMÆRK: Hvis du ikke kan finde en filmplakat , så prøv at finde et andet billede i fildetaljerne som du kan vise istedet.

BEMÆRK: Du skal teste at du kan søge efter filmen "Jagten" og se mindst et resultat med en film plakat.  

## Hent Film detaljer

Vis følgende detaljer:

 - Titel
 - Årstal
 - Filmplakat (vigtig)
 - Instruktør 
 - Medvirkende
 - Klip (billeder fra filmen) 
 - Konstruer et link til videoteket , hvis filmen er i videoteket
 
Filmplakaten skal være i øverste venstre hjørne.

Lav et link på instruktøren der kan bruges til at søge efter film af  instruktøren.

BEMÆRK: BILLEDERNE ER VIGTIGE. Hvis du ikke kan finde en filmplakat , så prøv at finde et andet billede.

## Søgning efter instruktør

Medtag søgning efter instruktør.

På resultatsiden for instruktøren skal der desuden medtages hvilke film han eller hun har instrueret.

## login 
En bruger skal kunne  logge ind . 

Det skal være muligt at oprette en ny konto.

Hvis der skal oprettes en ny konto, så skal det foregå på en anden side end login siden.

Efter at brugeren er registeret skal brugeren eksplicit logge ind. Lad være med at forsøge på autologin.

## Filmkasser
Efer at være logget ind kan brugeren oprette en eller flere filmkasser , hvor han kan gruppere film i.  Tillad brugeren at gemme en film i en filmkasse med en note tilknyttet.

Når en film vises i en filmkasse, så skal der ikke være info eller knapper om filmkassen på selve filmen.

Filmkassen skal vises som en accordion. Få den til at ligne en DVD opbevarings kasse.

Tillad at brugeren kan slette en film fra en filmkasse igen.

Når filmen allerede er i en filmkasse , så skriv hvilken filmkasse eller filmkasser den er i.  Tillad at den også kan tilføje til en anden en.