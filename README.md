# NAV v0.1 — Noeud d'Agregation VERA

VERA aggregation node — enforces ANCRE hypotheses H1, H2, H6 as structural invariants.

## Role

NAV manages the full window lifecycle:
OPEN -> CLOSED -> AGGREGATED

Raw signals are destroyed after aggregation.
This enforces GDPR Article 25 data minimization.

## Hypotheses Enforced

| Hypothesis | Enforcement | Status |
|---|---|---|
| H1 — one signal per SIM | max_per_device=1 | [ARCHITECTURAL] |
| H2 — bounded signals [0,1] | validation at ingestion | [ARCHITECTURAL] |
| H6 — closed window before aggregate | WindowState.CLOSED | [ARCHITECTURAL] |

## Components

- nav_window.py  — window lifecycle management
- nav_buffer.py  — signal buffer with H2 enforcement
- vera_d.py      — VERA-D temporal degradation policy

## VERA-D Policy

FRESH   (0-30d)   — aggregate intact
LIGHT   (30-90d)  — noise augmentation
STRONG  (90-180d) — strong noise augmentation
INVALID (180d+)   — returns None

VERA-D is [OPERATIONAL]+[CONJECTURAL] — a governance policy,
not a formal DP extension.

## Integration

NAV feeds into ANCRE pipeline:
https://github.com/taha-vera/ancre-final

## License

MIT — Taha Houari, SAS VERA Paris
