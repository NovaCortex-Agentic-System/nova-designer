---
name: onboarding
description: Setup inițial al agentului sau onboarding brand nou. Conectează Telegram, construiește KB-ul de brand și verifică dependențele tehnice.
triggers:
  - "run onboarding"
  - "/onboarding"
  - "onboarding"
  - "setup brand nou"
---

# Onboarding

Rulează când nu există `.onboarded` flag sau când utilizatorul cere explicit.

## Flux complet

### Pasul 1 — Conectare Telegram

Verifică că agentul poate trimite și primi mesaje:
```bash
cortextos bus send-user 'Bună! Sunt NOVA Designer 🎨 — testez conexiunea Telegram.'
```

Dacă eșuează: verifică `BOT_TOKEN` și `CHAT_ID` în `.env`.

### Pasul 2 — Identificare client / brand

Trimite utilizatorului:
```
Cu ce brand sau client lucrăm? 
Ai materiale de brand existente? (logo, PDF guidelines, URL website, screenshot-uri)
```

Așteaptă răspunsul înainte de a continua.

### Pasul 3 — Construire KB brand

**Dacă există materiale → rulează `brand-visual-identity` (robOS):**
- Ingestează materialele furnizate (PDF/URL/screenshot)
- Extrage: culori, fonturi, ton vizual, logo variante
- Salvează în `knowledge/brand-{client}.md`

**Dacă nu există materiale → interviu minim:**
```
Câteva întrebări rapide:
1. Ce industrie / domeniu?
2. Ton dorit: formal / relaxat / energic / minimalist?
3. Culori preferate sau de evitat?
4. Un brand pe care îl admiri vizual (din orice industrie)?
```

Construiește `knowledge/brand-{client}.md` cu răspunsurile ca draft inițial.

### Pasul 4 — Verificare dependențe

```bash
# KIE API
[[ -n "$KIE_API_KEY" ]] && echo "✓ KIE_API_KEY" || echo "✗ LIPSĂ: KIE_API_KEY"

# kie-mcp — server MCP pentru generare imagini/video (instalare automată dacă lipsește)
if which kie-mcp > /dev/null 2>&1; then
  echo "✓ kie-mcp"
else
  echo "kie-mcp lipsește. Instalez..."
  npm i -g @ulmeanuadrian/kie-mcp@latest
  which kie-mcp > /dev/null 2>&1 && echo "✓ kie-mcp instalat" || echo "✗ kie-mcp: instalare eșuată (verifică Node.js/npm)"
fi

# ImageMagick
which magick && echo "✓ ImageMagick" || echo "✗ LIPSĂ: imagemagick (brew install imagemagick)"
```

Dacă lipsesc KIE_API_KEY sau ImageMagick: creează task [HUMAN] cu instrucțiunile de configurare.
kie-mcp se instalează automat, nu necesită intervenție umană.

### Pasul 5 — Finalizare

```bash
mkdir -p "${CTX_ROOT}/state/${CTX_AGENT_NAME}"
touch "${CTX_ROOT}/state/${CTX_AGENT_NAME}/.onboarded"

cortextos bus send-user "Gata! KB-ul pentru {client} e salvat în knowledge/brand-{client}.md. Trimite-mi primul brief: tip produs, text de la Copywriter sau specificații vizuale."
```
