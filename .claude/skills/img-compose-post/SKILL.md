---
name: img-compose-post
description: Lipește text pe o imagine generată sau compune o postare completă (imagine + text + tip overlay/caption). Produce pachetul final livrat Evaluatorului.
triggers:
  - "overlay text"
  - "text pe imagine"
  - "compune postarea"
  - "pachet postare"
---

# img-compose-post

Skill de compoziție finală. Primește imaginea generată și textul de la Copyrighter, decide modul de îmbinare și produce pachetul complet.

## Când se activează

- After `kie-image` produces the base image
- When the brief specifies text placement (overlay vs caption)
- Before sending to Evaluator

## Decizie overlay vs caption

**Overlay (text pe imagine):**
- Brief specifică explicit text pe imagine
- Postare în format Story sau carusel cu titlu pe slide
- CTA vizibil integrat în imagine

**Caption (text separat):**
- Imagine product-shot sau lifestyle fără text
- Brief specifică că textul e în descrierea postării
- Reclamă unde imaginea vorbește singură

## Pași

1. Identifică modul din brief (overlay / caption)
2. Dacă overlay:
   a. Determină zona de text (sus / centru / jos) pe baza compoziției imaginii
   b. Aplică font din `brand-{client}.md` (tokens.json)
   c. Aplică culoare din paleta de brand
   d. Folosește imagemagick pentru burn-in text:
      ```bash
      magick input.png \
        -font "{brand_font}" \
        -pointsize {size} \
        -fill "{brand_color}" \
        -gravity {gravity} \
        -annotate +{x}+{y} "{text}" \
        output.png
      ```
3. Dacă caption: imaginea rămâne curată, textul merge în câmpul `caption` al pachetului
4. Salvează imaginea finală în `./outputs/{data}/{tip}/{client}/`
5. Returnează pachetul complet:
   ```json
   {
     "imagine": "/path/to/output.png",
     "caption": "textul postării",
     "tip": "overlay | caption",
     "dimensiuni": "WxH",
     "platforma": "instagram | facebook | meta-ads | story"
   }
   ```

## Note

- Fontul și culorile vin ÎNTOTDEAUNA din `knowledge/brand-{client}.md`
- Dacă KB-ul de brand lipsește: oprește și rulează onboarding mai întâi
- Dacă textul e prea lung pentru overlay: propune caption în schimb și notifică
