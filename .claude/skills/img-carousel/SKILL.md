---
name: img-carousel
description: Construiește un carusel multi-slide cu identitate vizuală consistentă. Fiecare slide are imagine + text pozitionat. Output: fișiere individuale + preview combinat.
triggers:
  - "carusel"
  - "carousel"
  - "multi-slide"
  - "slides"
---

# img-carousel

Produce carusele pentru Instagram, Facebook sau LinkedIn. Fiecare slide urmează identitatea vizuală a brandului, cu text poziționat consistent.

## Inputuri necesare

- Text structurat per slide (titlu + body) — de la Copyrighter
- Număr de slide-uri
- Platformă (Instagram: 1080×1080 sau 1080×1350, LinkedIn: 1080×1080)
- Brief vizual: stil, fundal, referințe

## Structura unui carusel

- **Slide 1 (cover):** titlu principal + element vizual puternic, fără text dens
- **Slide-uri intermediare:** un punct per slide, font mai mic, mai mult spațiu respirație
- **Slide final (CTA):** call-to-action clar, logo brand, contact sau link

## Pași

1. Citește brand tokens din `knowledge/brand-{client}.md` — fonturi, culori, spațieri
2. Generează fundalul / stilul vizual comun pentru toate slide-urile — skill: `kie-image` (prompt cu "consistent style across slides")
3. Pentru fiecare slide în ordine:
   a. Aplică fundalul sau varianta de fundal per slide
   b. Poziționează textul conform token-urilor (titlu: heading font, body: body font)
   c. Burn-in text cu imagemagick
   d. Salvează ca `slide-{N}.png`
4. Generează preview combinat (strip orizontal al tuturor slide-urilor):
   ```bash
   magick slide-1.png slide-2.png slide-3.png +append preview-carusel.png
   ```
5. Returnează pachetul:
   ```json
   {
     "slides": ["/path/slide-1.png", "/path/slide-2.png", "..."],
     "preview": "/path/preview-carusel.png",
     "caption": "textul postării (din Copyrighter)",
     "tip": "carusel",
     "platforma": "instagram | facebook | linkedin",
     "numar_slides": N
   }
   ```

## Note

- Consistența vizuală între slide-uri e obligatorie: același font, aceeași paletă, același stil de fundal
- Maxim 10 slide-uri per carusel (Instagram limit)
- Slide-urile cu text dens (>50 cuvinte) = flag pentru revizuire înainte de trimitere la Evaluator
