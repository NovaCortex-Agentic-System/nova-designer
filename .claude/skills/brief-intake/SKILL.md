---
name: brief-intake
description: Wizard interactiv de colectare brief. Detectează tipul de output cerut și pune întrebările necesare câte una, apoi lansează skill-ul de generare corespunzător.
triggers:
  - "vreau o postare"
  - "vreau un carusel"
  - "fă o imagine"
  - "fă o poză"
  - "vreau un story"
  - "vreau un meta ad"
  - "vreau o reclamă"
  - "fă un carusel"
  - "fă un story"
  - "brief"
  - "start"
  - "să facem"
  - "want a post"
  - "make a carousel"
  - "make an ad"
---

# brief-intake — Wizard de briefing interactiv

Colectează tot ce e necesar pentru generare, câte o întrebare pe rând via Telegram. Nu pune niciodată două întrebări în același mesaj.

## Regula de bază

Una câte una. Trimiți întrebarea, aștepți răspunsul, trimiți următoarea. Nu grăbi, nu combina.

---

## Pasul 1 — Detectare tip

Identifică tipul din mesajul utilizatorului:

| Detectat | Tip |
|---|---|
| postare, imagine, poză, post | `postare` |
| carusel, carousel, slides, multi-slide | `carusel` |
| story, stories, reels | `story` |
| ugc, candid, selfie, fotorealist, lifestyle | `ugc` |
| meta ad, reclamă, ad, publicitate | `meta-ad` |

Dacă tipul nu e clar, trimite:
```
cortextos bus send-user 'Ce vrem să facem?
1. Postare simplă (imagine + caption)
2. Carusel multi-slide
3. Story vertical
4. Foto UGC fotorealist
5. Meta ad (reclamă plătită)'
```
Așteaptă selecția, apoi continuă cu setul de întrebări al tipului ales.

---

## Pasul 2 — Întrebări per tip

### TIP: postare

```
Q1: cortextos bus send-user 'Platformă? Instagram feed / Facebook / LinkedIn'
Q2: cortextos bus send-user 'Avem textul postării (de la Copywriter) sau îl scriem acum?'
  → Dacă DA: 'Trimite-mi textul.'
  → Dacă NU: 'Despre ce e postarea? Spune-mi mesajul principal în 1-2 propoziții.'
Q3: cortextos bus send-user 'Stil vizual: fotorealist / grafic / UGC / minimalist / altul?'
Q4: cortextos bus send-user 'Textul merge pe imagine (overlay) sau doar în descrierea postării (caption)?'
```

Brief final:
```json
{
  "tip": "postare",
  "platforma": "...",
  "text": "...",
  "stil": "...",
  "mod_text": "overlay | caption"
}
```
Lansează: `img-compose-post`

---

### TIP: carusel

```
Q1: cortextos bus send-user 'Platformă? Instagram / LinkedIn / Facebook'
Q2: cortextos bus send-user 'Care e subiectul caruselului? (ex: 3 greșeli pe care le faci, 5 pași pentru X)'
Q3: cortextos bus send-user 'Câte slide-uri? (max 10, recomand 5-7)'
Q4: cortextos bus send-user 'Avem textul per slide de la Copywriter sau îl scriem acum?'
  → Dacă DA: 'Trimite-mi textele — câte un slide per mesaj sau toate odată.'
  → Dacă NU: 'Dă-mi punctele principale, unul per slide. Le formulez eu.'
Q5: cortextos bus send-user 'Stil vizual: grafic bold / minimalist / fotografie fundal / abstract?'
```

Brief final:
```json
{
  "tip": "carusel",
  "platforma": "...",
  "subiect": "...",
  "numar_slide-uri": N,
  "slide-uri": ["text slide 1", "text slide 2", "..."],
  "stil": "..."
}
```
Lansează: `img-carousel`

---

### TIP: story

```
Q1: cortextos bus send-user 'Platformă? Instagram / Facebook'
Q2: cortextos bus send-user 'Scopul story-ului: awareness / ofertă / CTA / conținut educativ?'
Q3: cortextos bus send-user 'Avem textul sau îl scriem acum?'
  → Dacă DA: 'Trimite-mi textul.'
  → Dacă NU: 'Ce mesaj principal vrem să transmitem?'
Q4: cortextos bus send-user 'Element vizual principal: produs / persoană / text mare pe fundal / abstract?'
```

Brief final:
```json
{
  "tip": "story",
  "platforma": "...",
  "scop": "...",
  "text": "...",
  "element_vizual": "..."
}
```
Lansează: `viz-instagram-story` (robOS)

---

### TIP: ugc

```
Q1: cortextos bus send-user 'Tip scenă: mirror selfie / car selfie / café shot / testimonial candid / altul?'
Q2: cortextos bus send-user 'E vreun produs cu text pe etichetă în cadru? (important pentru alegerea modelului)'
  → Dacă DA: 'Ce scrie pe etichetă? (îl redau fidel cu GPT-Image-2)'
  → Dacă NU: continuă
Q3: cortextos bus send-user 'Persoana e generată sau ai o poză de referință pentru identitate?'
  → Dacă are referință: 'Trimite-mi poza — o încarc ca referință de identitate.'
Q4: cortextos bus send-user 'Format: 9:16 stories / 4:5 feed / 1:1?'
```

Brief final:
```json
{
  "tip": "ugc",
  "scena": "...",
  "produs_cu_text": true | false,
  "text_eticheta": "...",
  "referinta_identitate": "url | null",
  "format": "9:16 | 4:5 | 1:1"
}
```
Lansează: `ugc-photo` (robOS)

---

### TIP: meta-ad

```
Q1: cortextos bus send-user 'Obiectiv: awareness / conversie / retargeting?'
Q2: cortextos bus send-user 'Ce promovăm? (produs, serviciu, ofertă — în 1-2 propoziții)'
Q3: cortextos bus send-user 'Care e oferta sau CTA-ul principal? (ex: -30% doar azi, Înscrie-te gratuit)'
Q4: cortextos bus send-user 'Avem textul ad-ului de la Copywriter sau îl scriem acum?'
  → Dacă DA: 'Trimite-mi headline + textul ad.'
  → Dacă NU: 'Îl construiesc eu din ce mi-ai spus — confirm înainte de generare.'
Q5: cortextos bus send-user 'Format: imagine single / carusel?'
```

Brief final:
```json
{
  "tip": "meta-ad",
  "obiectiv": "...",
  "produs": "...",
  "cta": "...",
  "text_ad": "...",
  "format": "single | carusel"
}
```
Lansează: `content-meta-image-ad` (robOS)

---

## Pasul 3 — Confirmare brief

Înainte de generare, trimite brieful complet utilizatorului:

```
cortextos bus send-user 'Brief complet:
Tip: {tip}
Platformă: {platforma}
Text: {text}
Stil: {stil}
...

Generăm?'
```

Dacă utilizatorul modifică ceva, actualizează brieful și retrimite confirmarea. Generează doar după confirmare explicită.

---

## Pasul 4 — Lansare generare

Rulează `img-brand-identity` mai întâi (încarcă tokens din KB), apoi skill-ul țintă cu brieful complet.

Dacă KB-ul de brand lipsește pentru clientul activ:
```
cortextos bus send-user 'Nu am un KB de brand pentru acest client. Rulăm onboarding mai întâi?'
```
Nu genera fără brand identity definit.
