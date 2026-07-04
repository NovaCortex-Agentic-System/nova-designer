# Onboarding

Rulează la primul boot sau când utilizatorul spune "run onboarding".

---

## Pași

### 1. Salut și context

```bash
cortextos bus send-user 'Bună! Sunt NOVA Designer 🎨 — producătorul vizual al flotei. Înainte să încep să generez, am nevoie să înțeleg cu ce brand lucrez.'
```

### 2. Identificare brand / client

Întreabă:
- Cu ce brand sau client lucrezi?
- Există deja materiale de brand (logo, culori, fonturi, guidelines PDF sau URL website)?

### 3. Construire / import KB brand

**Dacă există materiale:**
- Rulează `brand-visual-identity` (robOS) pe materialele furnizate
- Salvează output în `knowledge/brand-{client}.md`

**Dacă nu există materiale:**
- Ghidează utilizatorul prin întrebări minime: industrie, ton vizual dorit, culori preferate, exemple de branduri admirate
- Construiește un `knowledge/brand-{client}.md` minimal pe baza răspunsurilor
- Notează că e un draft care va fi rafinat în timp

### 4. Verificare dependențe

```bash
# Verifică KIE_API_KEY
[[ -n "$KIE_API_KEY" ]] && echo "KIE OK" || echo "LIPSĂ: KIE_API_KEY"

# Verifică imagemagick
which magick && echo "ImageMagick OK" || echo "LIPSĂ: imagemagick"
```

Dacă lipsesc chei sau tool-uri, creează un task [HUMAN] cu instrucțiuni exacte.

### 5. Marchează onboarding complet

```bash
mkdir -p "${CTX_ROOT}/state/${CTX_AGENT_NAME}"
touch "${CTX_ROOT}/state/${CTX_AGENT_NAME}/.onboarded"
cortextos bus send-user 'Gata! KB-ul de brand e salvat și sunt pregătit să produc. Trimite-mi primul brief.'
```
