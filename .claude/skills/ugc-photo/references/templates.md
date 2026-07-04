# UGC Worked Templates (kie.ai)

Trei tipuri comune, fiecare folosind aceleasi 4 layere. Variabilele se schimba, structura nu. Prompt-urile sunt deja despletite in limbaj natural (fara sintaxa Midjourney). `aspect_ratio` se pune ca parametru kie, nu in text.

---

## 1. Gym mirror selfie

**Model:** `nano-banana-2` · **aspect_ratio:** `9:16`

```
A 24-year-old woman in a gray sports bra and black leggings, mid-turn mirror selfie at a crowded commercial gym, phone covering half her face, locker room mirror smudged with sticker residue and fingerprints, shot on iPhone 12 mini front camera, harsh overhead fluorescent lighting washing out the highlights, slight motion blur on her free arm, mild lens distortion at the frame edges, JPEG compression visible in the shadows, slightly green color cast from the overhead bulbs, casual unposed body language, gym equipment visible in soft background, no filter
```

---

## 2. Car selfie at a gas station (night)

**Model:** `nano-banana-2` · **aspect_ratio:** `9:16`

```
A 31-year-old man, brown stubble, faded baseball cap, sitting in the driver's seat of a Honda Civic at night, dim ambient light from a Shell gas station sign through the windshield, mid-bite of a fast food wrap, half-eaten wrapper resting on his lap, phone held in his left hand just below eye level, dome light visible at the top of the frame, shot on iPhone 13 front camera, slight chromatic aberration around the gas station sign, low-light noise in the shadows, slightly warm color cast from the dome bulb, unposed expression mid-chew, no filter
```

---

## 3. Café food photo (no person)

**Model:** `nano-banana-2` · **aspect_ratio:** `4:5`

```
An iced matcha latte in a plastic cup on a marble café table, half-eaten chocolate croissant on a small white plate beside it, a phone face-down on the table, a wrinkled napkin under the croissant, shot from a slight high angle on iPhone 14 front camera, harsh window light from camera-left blowing out the marble surface, slight haze and lens smudge in the lower-right corner, ice cubes melting and condensation on the cup, soft motion blur where a hand was just removed from frame, no filter
```

---

## 4. Product testimonial in hand (eticheta lizibila)

**Model:** `gpt-image-2` (label legibility) · **aspect_ratio:** `4:5`

```
A 29-year-old man in a wrinkled navy t-shirt holding a {PRODUCT} can at chest height, label facing the camera and clearly legible, slightly oversized fit, sitting on a worn couch in a lived-in apartment, shot on iPhone 13 front camera held just above eye level, mixed lighting from a warm ceiling bulb and cool daylight through a window behind him creating conflicting color temperatures, slight lens smudge in the corner, low-light noise in the shadow areas, slightly crushed blacks, JPEG compression visible in the darker regions, unposed half-distracted expression, no filter
```

Inlocuieste `{PRODUCT}` cu produsul real. Pentru text pe eticheta foloseste `gpt-image-2`; daca eticheta iese ilizibila, re-genereaza cu descrierea exacta a textului in prompt.

---

## Pattern de variante

Variaza UN singur layer intre apeluri — nu regenera tot prompt-ul:
- **Varianta A** — prompt exact.
- **Varianta B** — schimba Layer 3 (lumina: fluorescent → window light).
- **Varianta C** — schimba Layer 2 (device: iPhone 12 → iPhone 14 Pro back camera).
- **Varianta D** — schimba Layer 1 (subiect: alta varsta / haine).
