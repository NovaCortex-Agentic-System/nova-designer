# System

## Paths cheie

```bash
# Rădăcina agentului (injectată de CortexTOS)
$CTX_ROOT/orgs/$CTX_ORG/agents/nova-designer/

# Knowledge base brand-uri
./knowledge/brand-{client}.md

# Memoria zilnică
./memory/$(date -u +%Y-%m-%d).md

# Logs
~/.cortextos/$CTX_INSTANCE_ID/logs/nova-designer/
```

## Dependențe externe

- **kie.ai API** — generare imagini (necesită `KIE_API_KEY`)
- **imagemagick** — prezent local, verifică: `which magick`
- **Skill-uri robOS** — instalate în `.claude/skills/` din `/Users/danmitrut/Downloads/robOS/skills/`

## Verificări la boot

```bash
# Verifică kie.ai
echo $KIE_API_KEY | head -c 8

# Verifică imagemagick
which magick && magick --version | head -1

# Verifică KB brand existent
ls knowledge/
```

## Output paths

Toate outputurile se salvează local în:
```
./outputs/{data}/{tip}/{client}/
```
Exemple:
- `./outputs/2026-07-04/imagine-single/brand-abc/postare-produs.png`
- `./outputs/2026-07-04/carusel/brand-abc/slide-{1..5}.png`
