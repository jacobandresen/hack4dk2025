
# Features

Brug DFI apiet som beskrevet her : https://api.smk.dk/api/v1/docs/#/artworks/searchArt 

## Søg efter kunstværk

Brug følgende eksempel

Find al data på alle kunstværker der indeholder key "amager", spring ingen over og vis de første 100:
https://api.smk.dk/api/v1/art/search/?keys=amager&offset=0&rows=100

BEMÆRK: Søgningen fra søgeformen på skærmen skal mappes til attributten"keys" i SMK API 


## Detaljer om et kunstværk

Vis følgende detaljer:

 - Titel
 - Årstal
 - Kunstner
 - Billede 

Tilbyd en knap så brugeren kan downloaded billedet i en højere opløsning hvis muligt.
 
