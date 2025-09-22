
# Features

## Design

Brug designet fra SMK's hjemmeside her https://www.smk.dk .

Sørg for at det er nemt at læse hvad der står på skærmen. Tænk på at teksten skal fremstå tydeligt foran baggrunden.

Søg altid for at hele billeder af malerier vises. Tillad flere forskellige størrelsere af resultatkort.


## Brug af API

Brug DFI apiet som beskrevet her : https://api.smk.dk/api/v1/docs/#/artworks/searchArt 


Tag udgangspunkt i eksemplerne her først:

Find al data på kunstværket med inventarnummeret KMS1:
https://api.smk.dk/api/v1/art/?object_number=kms1

Find al data på alle kunstværker der indeholder key "amager", spring ingen over og vis de første 100:
https://api.smk.dk/api/v1/art/search/?keys=amager&offset=0&rows=100

Find titler på alle kunstværker, som har foto, som er malerier og som er i public domain, spring ingen over og vis de første 30:
https://api.smk.dk/api/v1/art/search/?keys=*&fields=titles&filters=[has_image:true],[object_names:maleri],[public_domain:true]&offset=0&rows=30

BEMÆRK: Søgningen fra søgeformen på skærmen skal mappes til attributten"keys" i SMK API 

BEMÆRK: SMK API'et bruger image_thumbnail og image_iiif_id som attributter for billeder.

## Forside

Forsiden starter med at en søgeform, hvor der kan søges efter en kunst. Bemærk at søgeformen kun skal være der 1 gang.  Når der er blevet søgt , så skal der vises søgeresultater.  Det skal være muligt at køre en ny søgning som overskriver gamle søgeresultater.

Ved tryk på et søgeresultat skal der vises yderligere detaljer om kunstværket.

## Søgning efter kunst 

Brugeren kan søge efter kunst uden at være logget ind.

Medtag kun titlen i søgefeltet og en knap hvor der står søg. Der skal ikke være andre knapper i søgeformen. 

Når der vises resultater skal der vises en titel, et årstal, en billede og kunstnerens navn. 

Hvis du ikke kan finde kunstneren så skal du ikke skrive noget

Når der klikkes på søgeresultatet skal der åbnes en side med flere detaljer om kunstværket (se "Vis kunstværk"). 

Prøv at tage højde for at billederne kan være af forskellige størrelse.  Find en god balance , sådan at de største billeder ikke bliver alt for store.

BEMÆRK: Det er vigtigt at du kan vise billeder her. Skip resultater uden billeder.

BEMÆRK: Kunstneren er kendt for de fleste værker . Hvis du slet ikke kan finde nogen , så har du lavet noget galt.

BEMÆRK: Du skal teste at du kan søge efter "Amager" og se mindst et resultat, hvor der er mindst et billede.  


## Vis kunstværk 

Vis følgende detaljer:

 - Titel
 - Årstal
 - Kunstner
 - Billede 

Tilbyd en knap så brugeren kan downloaded billedet i en højere opløsning hvis muligt.
 
BEMÆRK: DET ER VIGTIGT AT DU KAN VISE BILLEDET HER.

Husk at url encode inventar nummeret.

Hvis du ikke kan finde kunstneren så skal du ikke skrive noget - lad være med a skrive "Unknown".

## Søgning efter kunstner

Medtag søgning efter kunstner.

På resultatsiden for kunstneren skal der desuden medtages hvilke malerier han eller hun har malet.

## login 
En bruger skal kunne  logge ind . 

Det skal være muligt at oprette en ny konto.

Hvis der skal oprettes en ny konto, så skal det foregå på en anden side end login siden.

## Samlinger
Efer at være logget ind kan brugeren oprette en eller flere samlinger , hvor han kan gruppere kunst i.  Tillad brugeren at gemme et værk i en samling med en note tilknyttet.

Når et maleri vises i en samling, så skal der ikke være info eller knapper om samlingen på selve maleriet.

Samlingerne skal vises i en accordion.  Vis billeder fra den samling der er valgt.


Tillad at brugeren kan slette et maleri fra en samling igen.
