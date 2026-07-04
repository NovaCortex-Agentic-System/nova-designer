# Heartbeat Protocol

Rulează la fiecare 6 ore sau când ești invocat cu "heartbeat".

## Pași obligatori (în ordine)

1. Update heartbeat status:
   ```bash
   cortextos bus update-heartbeat "online"
   ```

2. Verifică inbox:
   ```bash
   cortextos bus check-inbox
   ```
   Procesează și ACK-uiește orice mesaj neprocesat.

3. Re-indexează memoria în KB:
   ```bash
   cortextos bus kb-ingest ./MEMORY.md ./memory/$(date -u +%Y-%m-%d).md \
     --org $CTX_ORG --agent $CTX_AGENT_NAME --scope private \
     --collection memory-$CTX_AGENT_NAME --force
   ```

4. Verifică task-uri stale (in_progress > 2h fără update):
   ```bash
   cortextos bus list-tasks --status in_progress
   ```
   Actualizează sau escaladează orice task blocat.

5. Scrie entry heartbeat în memoria zilnică:
   ```bash
   cat >> "memory/$(date -u +%Y-%m-%d).md" << MEMEOF

## Heartbeat - $(date -u +%H:%M UTC)
- Current focus: [ce lucrez și de ce]
- Active threads: [ce e în progres]
- Key decisions: [decizii luate de la ultimul heartbeat]
- Context notes: [observații non-evidente]
- Next: [ce urmează]

MEMEOF
   ```

6. Log event:
   ```bash
   cortextos bus log-event action heartbeat_completed info --meta '{"agent":"'$CTX_AGENT_NAME'"}'
   ```
