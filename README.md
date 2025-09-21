
# Introduktion

Dette repo indeholder mine eksperimenter med Vibe coding til Hack4DK 2025.

Mit vigtigste take-away fra eksperimenterne er at det er VIGTIGT at være skarp på formulere features og tekniske regler før at du går igang.

Jeg har i dette repo prøvet at finindstille en agent i AGENTS.md . Det ser ud til at den er god til lave samlingsapplikationer .. men den har det med at gå i selvsving.

Se mine MitSMK og Filmkassen der bruger  AGENTS.md. Prøv dem gerne af og fortæl mig hvad du synes.

Du er velkommen til at kopiere alt her og bruge det til det du har lyst til. 


## Kedelige notater fra september 2025:

- Mine lokale kørsler varierer fra 5 til 20 minutter her. Resultaterne kan blive meget forskellige fra gang til gang.
- Når tests fejler i Cursor, så kan den stå og vente på at du afbryder testen. Hold øje med testen, hvis der står "press CTRL+C to cancel"  så afbryd testen.
- nogle gange kører Cursor i selvsving. Den stopper sig selv efter 200 tool kald i streg. Men hold lige øje mens den kører. Især hvis du kører en dyr model (GPT5)



# Apps

## MitSMK (med API fra Statens museum for kunst)

En app hvor du kan gruppere kunst fra Statents museum for kunst vha af deres API.


1) Start en ny agent i cursor

2) Skriv følgende "Implementer Webapp'en som beskrevet i README.md" og kør agenten.


## Filmkassen (med API fra Det danske filminstitut)

En app hvor du kan gruppere film fra Det danske film institut vha af deres API

1) Få fat på et brugernavn og kode fra DFI:
For at løsningen skal virke , så skal du have indlognings info som beskrevet her : https://api.dfi.dk/documentation/dfiapi.pdf

Jeg har beskrevet yderligere i README filen for Filmkassen.

2) Start en ny agent i cursor

3) Skriv følgende "Implementer webapp'en beskrevet i README.md" og kør agenten



# Installation af software

Da jeg kørte disse eksperimenter brugte jeg Cursor på Macos og docker. 

## Installation af Docker
Du kan læse mere om hvordan man installerer docker her :https://www.docker.com

## Installation af Cursor 
Jeg bruger cursor her . Du kan læse mere om hvordan du installer  Cursor her : https://cursor.com/

