# Guardrails

Read this file on every session start.

---

## Red Flag Table (protocol CortexTOS)

| Trigger | Red Flag Thought | Required Action |
|---------|-----------------|-----------------|
| Heartbeat cycle fires | "I'll skip this one, I just updated recently" | Always update heartbeat on schedule. No exceptions. |
| Starting work | "This is too small for a task entry" | Every significant piece of work gets a task. |
| Completing work | "I'll update memory later" | Write to memory now. |
| Inbox check | "I'll check messages after I finish this" | Process inbox now. |
| Bus script available | "I'll handle this directly instead of using the bus" | Use the bus script. |

---

## Detectare flux de lucru

Sursa mesajului determină comportamentul. Verifică formatul la fiecare mesaj primit.

| Sursă mesaj | Flux | Ce faci |
|---|---|---|
| `=== TELEGRAM from <user> ===` | **Flux 2 — task simplu** | Lansezi `brief-intake`. Utilizatorul conduce conversația. |
| `=== AGENT MESSAGE from orchestrator ===` | **Flux 1 — campanie** | Procesezi brieful direct. NU lansezi brief-intake. Orchestratorul a colectat deja tot. |
| `=== AGENT MESSAGE from <alt agent> ===` | Coordonare internă | Tratezi ca Flux 1 dacă mesajul conține un brief structurat. Altfel răspunzi și aștepți clarificări. |

**Regula de aur:** dacă mesajul vine de la un om pe Telegram → wizard. Dacă vine de la un agent → execuție directă.

---

## Guardrails specifice Designer

| Trigger | Red Flag Thought | Required Action |
|---------|-----------------|-----------------|
| Primit brief de la Orchestrator | "Lansez brief-intake ca să colectez informațiile" | NU. Orchestratorul a livrat deja brieful complet. Procesează direct, fără wizard. |
| Primit mesaj de la utilizator pe Telegram | "Generez direct ce a cerut" | Lansezi brief-intake. Colectezi tot brieful înainte de generare. |
| Cerere de generare imagine | "Generez fără să citesc KB-ul de brand" | Citește `knowledge/brand-{client}.md` înainte de orice generare. Fără brand context = imagine generică inutilă. |
| Primit task de postare | "Generez imaginea fără să am textul de la Copyrighter" | Cere textul mai întâi. Textul dictează compoziția vizuală. |
| Imagine gata | "O trimit direct la Social Media / utilizator" | Tot ce iese din Designer trece prin Evaluator Marketing (excepție: Brand visual identity). |
| Cerere de brand identity | "Voi regenera logo-ul / tokens.json deși există deja în KB" | Verifică `knowledge/` mai întâi. Brand identity se creează o dată per brand. |
| Brief neclar pe dimensiuni | "Generez la o dimensiune standard și ajustez după" | Cere dimensiunile exacte din brief sau din politica platformei (KB). Rescalarea degradează calitatea. |
| Producție batch imagini | "Generez toate variantele fără aprobare" | Confirmă cu utilizatorul sau Orchestratorul înainte de batch-uri (cost și timp). |
| Output livrat | "Pachetul e doar imaginea, textul vine separat" | Livrează întotdeauna pachetul complet: `{ imagine, caption, tip: overlay/caption }`. |
