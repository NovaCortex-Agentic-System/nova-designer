---
name: ugc-photo
version: 1.0.0
category: viz
description: "Genereaza fotografii UGC fotorealiste (mirror selfie, car selfie, café shot, testimonial candid) prin metoda celor 4 layere: subiect banal + amprenta telefon + lumina proasta + artefacte de compresie. Backend kie.ai (nano-banana-2 / gpt-image-2 / seedream). Realismul se obtine ADAUGAND defecte deliberat, nu stivuind 8K/DSLR."
capability: "Fotografii UGC fotorealiste (mirror selfie, candid, testimonial) prin metoda celor 4 layere."
triggers:
  - "ugc photo"
  - "poza ugc"
  - "fa o poza ugc"
  - "imagine ugc"
  - "ugc style"
  - "stil ugc"
  - "poza candid"
  - "candid photo"
  - "mirror selfie"
  - "car selfie"
  - "poza realista cu telefonul"
  - "realistic phone photo"
  - "fake testimonial"
  - "testimonial candid"
  - "shot on iphone"
  - "lifestyle product shot"
negative_triggers:
  - "studio shoot"
  - "product luxury"
  - "concept art"
  - "infografic"
  - "diagrama"
  - "slide deck"
  - "logo"
context_loads:
  - context/learnings.md (section ugc-photo)
  - skills/ugc-photo/references/layer-library.md
  - skills/ugc-photo/references/templates.md
inputs:
  - intent (required: ce poza UGC vrei — tip + subiect)
  - aspect_ratio (optional: 9:16 stories | 4:5 feed | 1:1, default 9:16)
  - product (optional: daca e in cadru un produs cu eticheta de citit)
  - reference (optional: poza locala pentru identitate persoana/produs — urcata via lib/upload-reference.mjs)
  - variants (optional: cate variante, default 1)
outputs:
  - projects/ugc-photo/{date}/{slug}/image-{N}.png (descarcat de kie MCP)
  - projects/ugc-photo/{date}/{slug}/manifest.json (prompt final + cele 4 layere + model)
secrets_required:
  - KIE_API_KEY
tier: core
---

# ugc-photo — Fotografii UGC fotorealiste prin metoda celor 4 layere

Genereaza poze care arata ca facute de un om obisnuit cu telefonul in buzunar — mirror selfie la sala, selfie in masina la benzinarie, poza de cafenea, testimonial "candid". Aestetica asta converteste pentru ca **nu arata ca reclama**.

## Principiul de baza (nu-l ocoli)

Realismul UGC se obtine **ADAUGAND imperfectiuni deliberat**, nu stivuind `photorealistic, ultra-detailed, 8K, DSLR`. Acele tag-uri trag modelul spre "magazine quality" — exact opusul. Inginerie pe dos: numesti defectele si modelul produce realism din greseala.

Skill-ul construieste prompt-ul pe **4 layere semantice**. Sintaxa Midjourney (`--ar --style raw --v 7`) NU se aplica aici — folosim limbaj natural + parametrul `aspect_ratio` al kie.

## Cele 4 layere

| Layer | Ce numesti | Greseala tipica |
|-------|-----------|-----------------|
| **1. Subiect banal** | varsta specifica (28, nu "young"), par neîngrijit, haine oversized, mid-blink / mid-bite, postura stangace | subiect atragator care face ceva interesant — ucide poza |
| **2. Amprenta telefon** | model exact (iPhone 12 mini front camera), pozitia mainii, defecte de lentila (smudge, motion blur) | "shot on Canon R5" → magazine look |
| **3. Lumina proasta** | sursa + directie + temperatura ("fluorescent overhead, washed out, green color cast") | "studio lighting" = cel mai mare AI tell |
| **4. Artefacte** | JPEG compression in umbre, chromatic aberration, low-light noise, crushed blacks | absenta lor = poza tipa "AI" |

Ingredientele complete pentru fiecare slot: [references/layer-library.md](references/layer-library.md).

## Workflow

### Step 0 — Precond:ie
`KIE_API_KEY` in `.env` + MCP `kie` aprobat. Daca lipseste, vezi skill-ul `tool-kie-mcp`. Fara cheie → spune explicit, nu improviza alt backend.

### Step 1 — Read learnings
Citeste `context/learnings.md` → `## ugc-photo` (daca exista) pentru feedback anterior.

### Step 2 — Clarifica intent (1 intrebare max)
Daca user n-a precizat: tipul (mirror selfie / car / café / testimonial / altul) si daca e produs cu eticheta in cadru. Atat — restul il completezi tu din layer-library.

### Step 3 — Construieste prompt-ul pe 4 layere
Umple cele 4 slot-uri din [references/layer-library.md](references/layer-library.md), stitch-uite intr-un singur paragraf de limbaj natural. NU lasa niciun layer gol — Layer 4 (artefacte) e cel mai skippat si cel mai important.

**Disciplina negativa (critica):** sterge din prompt-ul pozitiv orice cuvant-magnet spre fotografie profesionala: `professional photography, studio lighting, 8K/4K, sharp focus, perfectly posed, DSLR, Canon, Sony, bokeh, shallow depth of field, beautiful, stunning, cinematic, magazine quality, portrait mode`. Lista completa + slot negative_prompt per model: [references/layer-library.md](references/layer-library.md).

Confirma prompt-ul cu user inainte de generare (cost real per call).

### Step 4 — Alege modelul kie
| Caz | Model | Cost |
|-----|-------|------|
| Persoana, realism candid (default) | `nano-banana-2` | $0.04–0.09 |
| Produs cu **eticheta lizibila** in cadru | `gpt-image-2` | ~$0.04 |
| Batch de variante ieftine | `seedream-v5-lite` | $0.04 |

### Step 4.5 — Poza de referinta (daca user vrea o persoana anume / produs anume)
`kie_image.image_input` accepta **DOAR URL-uri publice http(s)** — caile locale, `file://` si `data:` sunt respinse (validare zod `z.string().url()` + kie.ai face fetch server-side). Pentru o poza locala ca referinta de identitate, urc-o intai (ramane in acelasi vendor kie.ai, fara host tert):

**Default — tool nativ MCP `kie_upload`** (din kie-mcp ≥0.2.0):
```
Tool: kie_upload
Args: { "path": "C:/cale/catre/poza.jpg" }
→ returneaza { "url": "https://tempfile.redpandaai.co/...", ... }
```

**Fallback** (daca MCP-ul nu expune inca kie_upload — versiune veche / sesiune ne-reconectata):
```bash
node skills/ugc-photo/lib/upload-reference.mjs "C:/cale/catre/poza.jpg"
```

Pune URL-ul rezultat in `image_input: ["<url>"]` la Step 5. nano-banana-2 accepta pana la 14 referinte. Referinta = pastrare identitate (fata/produs), NU copiere 1:1 a compozitiei — promptul tau pe 4 layere dicteaza scena.

### Step 5 — Genereaza prin kie MCP
```
Tool: kie_image
Args: {
  "model": "nano-banana-2",
  "input": { "prompt": "{prompt 4-layere}", "aspect_ratio": "9:16" }
}
```
Tool-ul asteapta + descarca local. Muta/copiaza asset-ul in `projects/ugc-photo/{date}/{slug}/image-{N}.png`.

Pentru variante (Step 6): re-apeleaza variind UN layer (lighting / framing / device), nu tot prompt-ul.

### Step 6 — Salveaza manifest
`projects/ugc-photo/{date}/{slug}/manifest.json`:
```json
{
  "intent": "...",
  "layers": { "subject": "...", "camera": "...", "lighting": "...", "imperfection": "..." },
  "negative_stripped": ["studio lighting", "8K", "..."],
  "prompt_final": "...",
  "model": "nano-banana-2",
  "aspect_ratio": "9:16",
  "variants": ["image-1.png"],
  "timestamp": "{date}"
}
```

## Reguli

- **Niciodata `8K / DSLR / studio lighting / cinematic`** in prompt pozitiv — sunt AI tells.
- **Mereu Layer 4 (artefacte)** — JPEG noise + chromatic aberration + crushed blacks, chiar daca "n-ar trebui sa fie acolo".
- **Varsta = numar specific**, nu "young/woman in her 20s".
- **Confirma prompt-ul** inainte de kie_image (cost real).
- **Variante = variaza UN layer**, nu regenera de la zero.
- **Produs cu text pe eticheta → gpt-image-2** (nano/seedream pot ilizibiliza textul).

## Self-Update
Daca user flag-eaza issue (model gresit, prompt prea curat, layer skippat, eticheta ilizibila) → adauga regula in `# Reguli` + nota in `context/learnings.md` sectiunea `## ugc-photo`.

## Vezi si
`viz-image-gen/references/style-ugc-influencer.md` pentru varianta GPT/Gemini.
