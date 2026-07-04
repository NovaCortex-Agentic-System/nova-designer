# UGC 4-Layer Ingredient Library

Biblioteca de ingrediente pentru cele 4 layere. Alegi 1-3 din fiecare slot si le stitch-uiesti intr-un paragraf de limbaj natural. Specificitatea bate cantitatea — un detaliu concret ("frizzy brown hair, slight greasy") bate trei adjective vagi.

---

## Layer 1 — Subiect banal

Regula: subiectul arata ca omul de langa tine in autobuz. Niciodata cadrul perfect — cadrul cu 0.3s inainte/dupa cel perfect.

- **Varsta** — numar specific: `27`, `31`, `38`. Niciodata "young" / "in her 20s".
- **Par** — `frizzy`, `flyaways`, `slightly greasy`, `hat-head`, `messy bun with loose strands`.
- **Haine** — `oversized gray hoodie`, `wrinkled t-shirt`, `mismatched socks visible`, `slightly unflattering fit`.
- **Limbaj corporal** — `slumped`, `mid-motion`, `awkward angle`, `weight on one hip`.
- **Expresie** — `mid-talk`, `half-blink`, `mid-bite`, `distracted`, `looking off-frame`.

Exemplu linie subiect:
> A 28-year-old woman with frizzy brown hair in a slightly oversized gray hoodie, mid-bite of a microwave burrito, half-distracted expression

---

## Layer 2 — Amprenta telefonului

Regula: numesti device-ul, pozitia si **defectele** lentilei. Defectele mai ales. Generatiile de iPhone produc semnaturi vizuale diferite (MEDIUM confidence — efect puternic pe modele Gemini/MJ, mai slab pe altele).

- **Device** — `iPhone 12 mini`, `iPhone 13`, `iPhone 14 Pro`. Front camera pentru selfie, back camera pentru shot-uri de zi.
- **Pozitie mana** — `phone held just below chin level`, `phone above eye level`, `phone at waist`, `hand visible at frame edge`.
- **Defecte lentila** — `slight motion blur on her right arm`, `faint lens smudge in the lower-right corner`, `dirty front glass`, `dome light reflection on the lens`.

Exemplu linie camera:
> shot on iPhone 12 mini front camera, phone held just below chin level, slight motion blur on her right arm, faint lens smudge in the lower-right corner

---

## Layer 3 — Lumina proasta

Regula: lumina prost numita cu **specificitate**. Nu "harsh lighting" — care sursa, din care directie, la ce temperatura. `color cast` singur valoreaza mai mult decat "realistic lighting" stivuit de 5 ori.

- **Sursa** — `overhead fluorescent`, `dome light`, `gas station signage`, `refrigerator interior light`, `phone screen glow`.
- **Directie** — `overhead`, `side-key`, `from below`, `from behind`.
- **Calitate** — `harsh direct`, `washed out`, `partially blocked`.
- **Color cast** — `green from fluorescent`, `warm from sodium street lamp`, `blue from a phone screen`.
- **Conflict** — `mixed temperatures`, `source visible in frame`.

Exemplu linie lighting:
> harsh overhead fluorescent washing out her forehead, slight green color cast in the highlights, ceiling tile reflection visible at top of frame

---

## Layer 4 — Artefacte (cel mai skippat, cel mai important)

Regula: pozele reale de telefon au artefacte. Sunt invizibile pana dispar — si cand dispar, poza tipa "AI". Adauga-le chiar cand "n-ar trebui sa fie acolo". Mai ales atunci.

- **Compresie** — `visible JPEG compression in the shadow areas`, `banding in gradients`.
- **Zgomot** — `low-light noise in the darker corners`, `ISO grain`.
- **Sharpness** — `slight chromatic aberration on the window frame`, `soft focus on edges`.
- **Culoare** — `slightly desaturated`, `blown highlights`, `slightly crushed blacks`.
- **Format hints** — `no filter`, `unedited`, `HDR off`.

Exemplu linie artefacte:
> visible JPEG compression in the shadow areas, slight chromatic aberration on the window frame, low-light noise in the darker corners, slightly crushed blacks

---

## Disciplina negativa — cuvinte de sters din prompt-ul pozitiv

Acestea trag modelul atat de tare spre "professional photography" incat nicio imperfectiune nu salveaza poza. Sterge-le din prompt-ul pozitiv. Pe modelele care suporta `negative_prompt` in `input` (ex. flux-kontext), listeaza-le si acolo.

```
professional photography
studio lighting
high resolution, 8K, 4K
sharp focus
perfectly posed
DSLR, mirrorless, Canon, Sony
bokeh, shallow depth of field
beautiful, stunning
cinematic
magazine quality
portrait mode
```

Regula generala: orice ar pune un fotograf pe site-ul lui de portofoliu → sterge. Orice suna a meniu de setari telefon (`HDR off`, `front-facing`) sau a raport de criminalistica (device specific, defect de lentila specific, sursa de lumina specifica) → ajuta.

---

## Skeleton master

```
[Layer 1: Subiect + Actiune] [Layer 2: Camera + Device + Pozitie mana]
[Layer 3: Lumina + Directie + Color cast] [Layer 4: Artefacte] [no filter]
```

Aspect ratio se pune ca parametru kie (`aspect_ratio`), nu in text:
- `9:16` — stories / reels (default UGC)
- `4:5` — feed Instagram
- `1:1` — grid / generic
