---
name: content-meta-image-ad
version: 1.0.0
category: content
description: "Genereaza creative statice de reclama Meta (Facebook/Instagram) pornind dintr-o biblioteca de 37 de template-uri validate (editorial article, comparison table, fake search, native UI mimic, flatlay, testimonial etc.). Umple variabilele brand, ataseaza 3 safety-suffixes anti-chrome/edge-safe/glyph, randeaza via kie.ai (gpt-image-2 pentru typography-heavy, nano-banana-2 pentru fotoreal). Portat din arcads-claude-code (MIT)."
capability: "Reclame statice Meta din 37 template-uri (layout-uri de ad dovedite) randate cu kie.ai. Pentru publish vezi content-meta-ad-publish."
triggers:
  - "reclama meta"
  - "reclama facebook"
  - "reclama instagram"
  - "creative static"
  - "static ad"
  - "meta image ad"
  - "facebook ad image"
  - "instagram ad image"
  - "ad din template"
  - "fa o reclama statica"
  - "ad creative"
  - "comparison ad"
  - "native ad"
negative_triggers:
  - "video"
  - "ugc photo"
  - "poza ugc"
  - "publica reclama"
  - "deploy ad"
  - "blog"
  - "slide deck"
context_loads:
  - context/learnings.md (section content-meta-image-ad)
  - skills/content-meta-image-ad/references/OVERVIEW.md
  - skills/content-meta-image-ad/references/prompt-library.md
  - skills/content-meta-image-ad/references/safety-suffixes.md
  - skills/content-meta-image-ad/references/template-format.md
  - brand/voice.md (optional — copy din ad)
inputs:
  - intent (required: ce produs/oferta + ce unghi de ad)
  - template (optional: numele unui template din biblioteca; altfel il aleg eu)
  - aspect_ratio (optional: 1:1 feed | 4:5 feed | 9:16 stories, default 1:1)
  - brand_vars (optional: name, color_primary, color_accent, headline, subcopy, cta)
  - reference (optional: poza produs locala — urcata via kie_upload)
  - variants (optional: cate variante, default 1)
outputs:
  - projects/content-meta-image-ad/{date}/{slug}/ad-{N}.png (descarcat de kie MCP)
  - projects/content-meta-image-ad/{date}/{slug}/manifest.json (template, brand_vars, prompt final, model)
secrets_required:
  - KIE_API_KEY
optional_skills:
  - content-meta-ad-publish
  - content-ad-clone
  - viz-image-gen
tier: content-creator
---

# content-meta-image-ad — Reclame statice Meta din biblioteca de 37 template-uri

Construieste creative statice de Facebook/Instagram pornind de la **layout-uri de reclama dovedite**, nu de la zero. Biblioteca (`references/prompt-library.md`) are 37+ template-uri parameterizabile: editorial article, comparison table, fake search results, native UI mimic, product flatlay, testimonial, checklist, "as seen on" etc. Fiecare e un prompt cu variabile `{brand.*}` / `{ad.*}`. Randarea se face prin **kie.ai** (acelasi gateway ca restul robOS), nu prin Arcads.

> Sursa: portat din `krusemediallc/arcads-claude-code` (MIT). Prompt-urile, schema de variabile si safety-suffixes sunt vendor-agnostic; partea Arcads-API (auth, endpoint, productId) a fost inlocuita cu kie.ai.

## Preconditie
`KIE_API_KEY` in `.env` + MCP `kie` aprobat. Fara cheie → spune explicit, nu improviza alt backend (vezi `tool-kie-mcp`).

## Workflow

### Step 1 — Read learnings
Citeste `context/learnings.md` → `## content-meta-image-ad` (daca exista) pentru feedback anterior.

### Step 2 — Alege template-ul
Citeste `references/OVERVIEW.md` (arborele de decizie) + scaneaza `references/prompt-library.md`. Daca user-ul a dat un nume de template, foloseste-l. Altfel alege dupa unghiul de ad cerut (comparativ → comparison table; dovada sociala → "as seen on" / testimonial; nativ feed → native UI mimic etc.) si confirma scurt alegerea cu user-ul.

### Step 3 — Umple variabilele
Inlocuieste fiecare `{brand.*}` / `{ad.*}` din template cu valori reale (din `brand_vars`, din `brand/voice.md`, sau intreband user-ul ce lipseste — NU inventa nume de brand, cifre sau claim-uri; vezi regula anti-halucinare globala). Vocabular standard: `{brand.name}`, `{brand.color_primary}`, `{brand.color_accent}`, `{brand.product_image_description}`, `{ad.headline}`, `{ad.subcopy}`, `{ad.body}`, `{ad.cta_phrase}`. Detalii: `references/template-format.md`.

### Step 4 — Ataseaza cele 3 safety-suffixes (obligatoriu)
Din `references/safety-suffixes.md`, lipeste la sfarsitul prompt-ului toate cele 3:
- **NO_CHROME** — randeaza doar creative-ul standalone, fara device/platform chrome.
- **EDGE_SAFE** — tot textul + subiectele-cheie in centrul 84% al panzei.
- **GLYPH_SAFETY** — fara emoji/unicode in blocuri de text dens; numar exact de elemente.

Acestea repara cele mai frecvente esecuri de randare; nu le omite.

### Step 5 — Alege modelul kie
| Caz | Model kie | De ce |
|-----|-----------|-------|
| Typography-heavy, UI-mimicry, fake search, comparison table, text dens | `gpt-image-2` | reda textul corect |
| Fotoreal, lifestyle, flatlay, multi-reference (produs real) | `nano-banana-2` | realism + accepta pana la 14 referinte |
| Batch ieftin de variante | `seedream-v5-lite` | cost mic |

### Step 5.5 — Referinta produs (optional)
Daca templateul are slot de produs si user-ul da o poza locala: urc-o intai (`kie_upload` → URL public), apoi pune URL-ul in `image_input: ["<url>"]`. `kie_image.image_input` accepta DOAR URL-uri http(s).

### Step 6 — Genereaza prin kie MCP
```
Tool: kie_image
Args: {
  "model": "gpt-image-2",
  "input": { "prompt": "{template umplut + 3 suffixes}", "aspect_ratio": "1:1" }
}
```
Confirma prompt-ul cu user-ul inainte (cost real per call). Tool-ul asteapta + descarca local; muta asset-ul in `projects/content-meta-image-ad/{date}/{slug}/ad-{N}.png`.

> Nota params: daca kie raspunde `422` pe un param (ex. `aspect_ratio` pe un model care nu-l accepta), verifica `kie_models` si reincearca. Param-handling per model se valideaza de server (Zod).

### Step 7 — Variante (la cerere)
Re-apeleaza variind UN element (headline / paleta / model), nu tot prompt-ul. Salveaza `ad-2.png`, `ad-3.png`.

### Step 8 — Manifest
`projects/content-meta-image-ad/{date}/{slug}/manifest.json`:
```json
{
  "template": "comparison-table",
  "brand_vars": { "name": "...", "headline": "...", "cta_phrase": "..." },
  "suffixes": ["no_chrome", "edge_safe", "glyph_safety"],
  "prompt_final": "...",
  "model": "gpt-image-2",
  "aspect_ratio": "1:1",
  "variants": ["ad-1.png"],
  "timestamp": "{date}"
}
```

### Step 9 — Handoff (optional)
Daca user-ul vrea sa publice: paseaza calea creative-ului la `content-meta-ad-publish` (publica ca reclama PAUSED in Meta).

## Reguli
- **Mereu cele 3 safety-suffixes** la final — sunt cea mai mare sursa de fix.
- **Nu inventa** nume de brand, cifre, claim-uri sau "as seen on" publicatii — cere user-ului sau ia din `brand/`.
- **Typography-heavy → gpt-image-2** (nano poate ilizibiliza textul).
- **Confirma prompt-ul** inainte de kie_image (cost real).
- **Template-ul e punct de plecare**, nu camasa de forta — adapteaza layout-ul la oferta.

## Self-Update
Daca user-ul flag-eaza issue (template gresit, model gresit, text ilizibil, chrome randat) → adauga regula in `# Reguli` + nota in `context/learnings.md` la `## content-meta-image-ad`.

## Cross-references
- Publish: `content-meta-ad-publish`
- Adauga template nou dintr-o reclama existenta: `content-ad-clone`
- Imagine generica (non-ad): `viz-image-gen`; UGC photo: `ugc-photo`
