
# Introduktion

Dette repo indeholder mine eksperimenter med Vibe coding til Hack4DK 2025.

Mit vigtigste take-away fra eksperimenterne er at det er VIGTIGT at være skarp på formulere features og tekniske regler før at du går igang.

Jeg har i dette repo prøvet at finindstille en fullstack agent i agents/FULLSTACK.md . Det ser ud til at den er god til lave samlingsapplikationer .. men den har det med at gå i selvsving.

Se mine eksempler apps i apps/. Prøv dem gerne af og fortæl mig hvad du synes.

brug promptet "Implementer hvad der er beskrevet i README.md filen og de tilknyttede filer"


Du er velkommen til at kopiere alt her og bruge det til det du har lyst til. 


## Kedelige notater fra september 2025:

- Resultatet bliver anderledes ved genkørsel af promptet. Jeg ved ikke lige om det er et problem.
- Næsten hver eneste gang jeg har kørt agenten , så har den ignoreret et eller flere test krav.
- Mine lokale kørsler varierer fra 5 til 20 minutter her. Resultaterne kan blive meget forskellige fra gang til gang.
- Når tests fejler i Cursor, så kan den stå og vente på at du afbryder testen. Hold øje med testen, hvis der står "press CTRL+C to cancel"  så afbryd testen.
- nogle gange kører Cursor i selvsving. Den stopper sig selv efter 200 tool kald i streg. Men hold lige øje mens den kører. Især hvis du kører en dyr model (GPT5)


# Installation af software

Da jeg kørte disse eksperimenter brugte jeg Cursor på Macos og docker. 

## Installation af Docker
Du kan læse mere om hvordan man installerer docker her :https://www.docker.com

## Installation af Cursor 
Jeg bruger cursor her . Du kan læse mere om hvordan du installer  Cursor her : https://cursor.com/

