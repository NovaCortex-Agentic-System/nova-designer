---
name: img-brand-identity
description: Aplică identitatea vizuală a brandului (din tokens.json) pe orice output vizual. Asigură consistența culorilor, fonturilor și spațierilor pe toate produsele Designer-ului.
triggers:
  - "aplică brand"
  - "identitate vizuală"
  - "tokens brand"
  - "brand consistency"
---

# img-brand-identity

Skill de aplicare a identității vizuale. Citește `knowledge/brand-{client}.md` și aplică tokens-ii pe orice imagine sau compoziție în producție.

## Când se activează

La orice generare de imagine — înainte de `kie-image` sau imagemagick — pentru a pregăti parametrii vizuali corecți.

## Ce extrage din KB

```
knowledge/brand-{client}.md conține:
- culori principale (HEX)
- culori secundare (HEX)
- font heading (nume + weight)
- font body (nume + weight)
- spațieri standard
- ton vizual (minimalist / bold / cald / rece / etc.)
- exemple de imagini de referință (opțional)
```

## Pași

1. Citește `knowledge/brand-{client}.md`
2. Extrage tokens relevanți pentru task-ul curent:
   - Pentru imagine: ton vizual, paleta de culori ca referință în prompt
   - Pentru text overlay: font heading/body, culoare text, culoare fundal text
   - Pentru carusel: toate de mai sus + spațieri
3. Construiește parametrii pentru skill-ul următor:
   ```json
   {
     "culoare_primara": "#HEX",
     "culoare_secundara": "#HEX",
     "font_heading": "NumeFontHeading",
     "font_body": "NumeFontBody",
     "ton_vizual": "descriere stil",
     "prompt_suffix": "in the visual style of {brand}, using {culori} color palette, {ton} aesthetic"
   }
   ```
4. Injectează `prompt_suffix` în promptul de generare imagine
5. Folosește fontul și culorile la orice burn-in text

## Dacă KB-ul lipsește

```bash
cortextos bus send-user 'Nu am un KB de brand pentru acest client. Rulăm onboarding mai întâi?'
```

Nu continua fără KB. Zero imagini generate fără identitate vizuală definită.
