# Tools

Index rapid al tool-urilor disponibile. Încarcă skill-ul complet când ai nevoie de documentație detaliată.

---

## Skill-uri proprii

| Skill | Comandă rapidă | Când |
|-------|---------------|------|
| `brief-intake` | `/brief`, `vreau o postare`, `vreau un carusel` | Wizard interactiv de colectare brief — punct de intrare Flux 2 |
| `img-compose-post` | `/img-compose-post` | Overlay text pe imagine sau compoziție postare completă |
| `img-carousel` | `/img-carousel` | Construcție carusel multi-slide |
| `img-brand-identity` | `/img-brand-identity` | Aplicare identitate vizuală din tokens.json |
| `onboarding` | `/onboarding` | Setup inițial agent sau onboarding brand nou |

## Skill-uri din robOS (instalate)

| Skill | Când |
|-------|------|
| `brand-visual-identity` | Extrage identitate vizuală din PDF/URL/screenshot, produce tokens.json + brand bible |
| `ugc-photo` | Fotografii UGC fotorealiste cu defecte naturale |
| `content-meta-image-ad` | Reclame statice Meta din 37 template-uri validate |
| `viz-instagram-story` | Instagram Story 1080×1920 |

## CLI Tools

| Tool | Când |
|------|------|
| `imagemagick` | Resize, compresie, conversie formate imagini local |

## API-uri

| API | Modele disponibile | Când |
|-----|--------------------|------|
| `kie.ai` | GPT Image 2, Flux Kontext, nano-banana-2, seedream | Generare imagini AI |

## CortexTOS Bus

```bash
# Trimite mesaj utilizatorului
cortextos bus send-user '<mesaj>'

# Trimite mesaj alt agent
cortextos bus send-message <agent> normal '<mesaj>'

# Creare task
cortextos bus create-task "<titlu>" --desc "<descriere>"

# Completare task
cortextos bus complete-task <task_id> --result "<rezumat>"

# Update heartbeat
cortextos bus update-heartbeat "online"

# Query KB brand
cortextos bus kb-query "<întrebare>" --org $CTX_ORG --agent $CTX_AGENT_NAME

# Ingest în KB
cortextos bus kb-ingest /path/to/file --org $CTX_ORG --agent $CTX_AGENT_NAME --scope private
```
