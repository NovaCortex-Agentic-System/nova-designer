# Story System — reguli de brand & vizual

Sistemul de reguli pentru Instagram Stories 1080x1920 (brand premium/feminin/wellness,
ex. Constanta Mei Rosu — produse Forever). Default-uri folosite cand brand files lipsesc.

---

## Principiul-cheie

Doua joburi separate, niciodata amestecate:
- **VIZUAL** — fundalul (generat sau editat din poza reala) → kie.ai.
- **TEXT** — hook + CTA, ca overlay layer → PIL (lizibilitate + diacritice RO garantate).

Pe poza reala: **editeaza, nu regenera.** Editarea pastreaza chipul; generarea il schimba.

---

## Safe zones (pixeli, canvas 1080x1920)

- **Top reserved: 0-250px** (avatar + buton close) → fara text, fara fete importante
- **Bottom reserved: 1610-1920px** (caption, reply bar, link sticker) → fara text
- **Lateral: 64px** stanga/dreapta
- **Safe area text: y = 250-1610, x = 64-1016**
- Hook dominant: ideal treimea centrala (y ≈ 700-1100)

---

## Stil vizual (anchors concrete, nu adjective)

Vibe: cinematic, premium, feminin, wellness elegant. Operationalizat in prompt:
- **Lumina**: golden hour / soft window light, key cald ~3200-3600K, umbre fine
- **Profunzime**: depth of field redus (f1.8-f2.8 feel), fundal usor blurat
- **Compozitie**: rule of thirds, multa negative space unde vine textul, subiect off-center
- **Grading**: warm highlights, lifted soft shadows, fara saturatie agresiva
- **Texturi**: naturale (lemn, in, piele, lumina naturala), nu plastic/3D artificial
- Directia privirii: daca subiectul priveste intr-o parte, textul curge spre acea directie

Evita (negative): neon, glow excesiv, umbre artificiale, fete deformate, degete in plus,
text gibberish, watermark, ten plastic, fundal duplicat la outpaint.

---

## Paleta (lock in hex)

- Auriu accent: `#C8921A`
- Alb: `#FFFFFF`
- Crem: `#F4ECDD`
- Bej premium: `#D9C4A9`
- Text inchis (pe fundal deschis): `#2B2218`

---

## Overlay de contrast

- Gradient soft DOAR sub zona de text (nu peste toata poza)
- Opacitate 25-45%, dinspre margine spre centru
- Scop: contrast pentru text, nu intunecarea imaginii

---

## Tipografie & text

- Premium, modern, feminin, usor cinematic
- Hook: poate fi majuscule pentru accent, o singura linie
- O singura idee per story; fara text inghesuit; fara ALL CAPS excesiv pe body

---

## CTA — reguli de folosire

| CTA | Cand | Mecanica |
|-----|------|----------|
| CURIOASA | teaser, starnesti interes | reply sticker / "trimite mesaj" |
| INFO | userul vrea detalii produs | link sticker / DM |
| START | onboarding, program, challenge | link sticker |
| VREAU | intentie de cumparare directa | DM / link shop |
| POT | obiectie "pot si eu?" depasita | reply sticker |

CTA-ul sta in bottom-safe, ideal ca sticker (nu baked in imagine).

---

## Compliance (health claims — risc real)

Produsele Forever = wellness reglementat (ANPC, politici Instagram).
- Fara claim-uri medicale ("vindeca", "trateaza", "slabesti garantat X kg").
- Beneficii formulate ca experienta / stil de viata, nu promisiune medicala.
- La orice claim de sanatate → flag in manifest, intreaba userul daca nu esti sigur.

---

## Mapare model kie.ai

| Situatie | Model | De ce |
|----------|-------|-------|
| Poza reala — extinde fundal, pastreaza fata | `flux-kontext-pro` | editare context-aware |
| Carusel 4:5 → story 9:16 (outpaint) | `flux-kontext-pro` | extinde pastrand compozitia |
| Fundal din zero — calitate | `nano-banana-2` | 4K, fotorealist |
| Fundal din zero — volum/rapid | `seedream-v5-lite` | 4K mai ieftin pe iteratii |

Cost indicativ: ~$0.04-0.12 / imagine. Confirma promptul inainte de generare.
