---
name: viz-instagram-story
version: 1.0.0
category: viz
description: "Instagram Story 1080x1920 builder. Separa generarea vizualului de plasarea textului: pe poza reala EDITEAZA (nu regenereaza) prin Flux Kontext, fundal din zero prin Nano Banana / Seedream, iar textul (hook + CTA) se pune ca overlay layer cu PIL pentru lizibilitate garantata si diacritice RO. Backend EXCLUSIV kie.ai (MCP). Stil brand premium/feminin/wellness."
triggers:
  - "fa un story"
  - "story instagram"
  - "instagram story"
  - "creeaza un story"
  - "transforma in story"
  - "carusel in story"
  - "story 1080"
  - "story vertical"
  - "make an instagram story"
  - "turn this into a story"
  - "story pentru"
context_loads:
  - brand/voice.md
  - brand/audience.md
  - skills/viz-instagram-story/references/story-system.md
inputs:
  - mode (auto-detect: real-photo | from-scratch | carousel-to-story)
  - source_image (optional: poza reala sau caruselul de transformat)
  - message (required: ideea unica a story-ului)
  - product (optional: produs Forever / alt subiect)
  - cta (optional: CURIOASA | INFO | START | VREAU | POT)
outputs:
  - projects/viz-instagram-story/{date}/{slug}/visual.png (fundal kie.ai)
  - projects/viz-instagram-story/{date}/{slug}/story-final.png (cu text overlay)
  - projects/viz-instagram-story/{date}/{slug}/manifest.json
secrets_required:
  - KIE_API_KEY
runtime_dependencies:
  - python: ">=3.11"
tier: content-creator
---

# Instagram Story Builder (kie.ai)

Construieste Instagram Stories 1080x1920 premium. **Principiul-cheie**: genereaza
vizualul (kie.ai) si pune textul SEPARAT ca overlay layer (PIL). NU cere modelului
sa randeze text in imagine — il mazgaleste, mai ales diacriticele RO.

Sistemul complet de reguli (safe zones, paleta, CTA, stil, compliance) e in
[references/story-system.md](references/story-system.md). Citeste-l la prima rulare.

# Backend: EXCLUSIV kie.ai via MCP

Tot ce inseamna generare/editare de imagine trece prin MCP `kie` — niciun alt
backend (nu GPT/Gemini direct, nu Replicate). Tool-uri: `kie_upload`, `kie_image`,
`kie_wait`, `kie_cost_report`. Verifica disponibilitatea cu `kie_health` daca esuezi.

# Step 0: Protocol de interactiune

Inainte de orice generare, confirma in max 3 intrebari (sari peste ce userul a dat deja):
1. **Sursa vizualului**: poza reala atasata, carusel de transformat, sau generez din zero?
2. **Mesajul**: ideea unica a story-ului (o singura propozitie).
3. **Produs / CTA**: e despre un produs Forever anume? Ce CTA (CURIOASA/INFO/START/VREAU/POT)?

Detecteaza `mode` din raspuns:
- poza reala a unei persoane → `real-photo`
- imagine de carusel 1080x1350 → `carousel-to-story`
- doar tema/text → `from-scratch`

# Step 1: Citeste contextul

- `brand/voice.md` + `brand/audience.md` (daca exista) pentru ton.
- `references/story-system.md` pentru reguli vizuale + paleta + safe zones.
- `context/learnings.md` → sectiunea `viz-instagram-story` (feedback anterior), daca exista.

Daca brand files lipsesc, foloseste default-urile din story-system.md (premium/feminin/
wellness, paleta auriu #C8921A). Noteaza ce ar imbunatati output-ul.

# Step 2: Ruteaza modelul kie.ai dupa mode

| mode | model kie | de ce |
|------|-----------|-------|
| `real-photo` (extinde fundal, pastreaza fata) | `flux-kontext-pro` | editare context-aware — pastreaza subiectul real, extinde fundalul. NU regenera fata. |
| `carousel-to-story` (4:5 → 9:16 outpaint) | `flux-kontext-pro` | outpainting top+bottom pastrand compozitia originala. |
| `from-scratch` (fundal nou, calitate) | `nano-banana-2` | 4K, fotorealist, control bun pe lumina/compozitie. |
| `from-scratch` (volum / rapid) | `seedream-v5-lite` | 4K mai ieftin pentru iteratii multiple. |

**REGULA DE AUR**: pe `real-photo` NU folosi un model de generare pura cerand "pastreaza
fata". Editarea (`flux-kontext-pro`) pastreaza chipul; generarea il schimba. Daca userul
insista pe generare pura a unei persoane reale, avertizeaza-l explicit ca fata se va schimba.

# Step 3: Pregateste referinta (real-photo / carousel-to-story)

`kie_image.input.image_input` accepta DOAR URL-uri publice. Urca poza locala intai:

```
Tool: kie_upload
Args: { "path": "C:/cale/catre/poza.jpg" }
→ returneaza { "url": "https://..." }
```

# Step 4: Construieste prompt-ul vizual (FARA text in imagine)

Promptul descrie DOAR vizualul: subiect, lumina, compozitie, grading, negative space
unde va veni textul. NU include hook-ul/CTA-ul in prompt (alea vin ca overlay).

Anchors din story-system.md (concrete, nu adjective): golden hour / soft window light,
~3200-3600K key cald, depth of field redus, rule of thirds, negative space in treimea
unde pui textul, warm highlights / lifted shadows, texturi naturale.

Negative: fete deformate, degete in plus, text gibberish, watermark, ten plastic,
fundal duplicat la outpaint.

Confirma promptul cu userul inainte de generare (cost real ~$0.04-0.12/imagine).

# Step 5: Genereaza vizualul prin kie

```
Tool: kie_image
Args: {
  "model": "flux-kontext-pro",        // sau nano-banana-2 / seedream-v5-lite per Step 2
  "input": {
    "prompt": "{prompt vizual, fara text}",
    "image_input": ["https://...url_din_upload..."],   // doar la real-photo / carousel
    "aspect_ratio": "9:16"
  },
  "wait": true
}
→ returneaza asset_paths (descarcat local in ~/.kie-mcp/assets)
```

Copiaza asset-ul in `projects/viz-instagram-story/{date}/{slug}/visual.png`.

# Step 6: Pune textul ca overlay layer (PIL — lizibilitate garantata)

Textul, safe zones, gradientul de contrast si diacriticele RO se pun cu scriptul local,
NU prin kie. Asta garanteaza text vizibil corect (modelele mazgalesc diacriticele).

```bash
python skills/viz-instagram-story/lib/overlay_text.py \
  --image projects/viz-instagram-story/{date}/{slug}/visual.png \
  --hook "{hook scurt, max o linie}" \
  --cta "{CURIOASA|INFO|START|VREAU|POT}" \
  --output projects/viz-instagram-story/{date}/{slug}/story-final.png
```

Optiuni utile: `--hook-pos top|center|bottom` (default center, in safe area),
`--accent "#C8921A"`, `--no-overlay` (fara gradient). Vezi `--help`.

Pe `carousel-to-story` cu text original: re-pune textul ca overlay (NU-l lasa regenerat).

# Step 7: Salveaza manifest

```json
{
  "mode": "real-photo|from-scratch|carousel-to-story",
  "model": "flux-kontext-pro",
  "prompt_visual": "...",
  "hook": "...",
  "cta": "...",
  "source_image": "... sau null",
  "visual": "visual.png",
  "final": "story-final.png",
  "timestamp": "..."
}
```

Optional: ruleaza `kie_cost_report` si noteaza costul real in manifest.

# Rules

- **Backend = numai kie.ai (MCP).** Niciun GPT/Gemini/Replicate direct.
- **Vizual si text sunt joburi separate.** kie face fundalul; PIL face textul. Niciodata text baked in generare.
- **real-photo → EDITEAZA (flux-kontext), nu regenera.** Generarea schimba fata.
- **Confirma promptul inainte de kie_image** — cost real.
- **Safe zones in pixeli** (top 0-250, bottom 1610-1920, lateral 64) — vezi story-system.md.
- **Compliance health claims**: produse Forever = wellness reglementat. Fara claim-uri medicale; flag in manifest daca textul atinge sanatate.

# Self-Update

Daca userul flag-eaza issue (model gresit, fata schimbata, text mazgalit, safe zone gresit),
actualizeaza `# Rules` sau `references/story-system.md` si noteaza in `context/learnings.md`.
