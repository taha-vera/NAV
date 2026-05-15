# NAV — Noeud d'Aggrégation VERA

**VERA aggregation node** — manages ANCRE windows lifecycle (H6)

## Composants

- AggregationWindow — Fenêtre H6 avec validation temporelle
- NAVBuffer — Buffer non-volatile avec chaînage cryptographique

## Utilisation

```python
from nav_window import AggregationWindow
from nav_buffer import NAVBuffer

win = AggregationWindow()
win.open_window()
from datetime import datetime
win.add_point(datetime.now(), 42.0)
data = win.close_window()

buffer = NAVBuffer()
buffer.commit_window(data)
```

## Intégrité

- Hash SHA256 par fenêtre
- Chaînage séquentiel
- Validation temporelle H6 stricte

## VERA Compliance

- Format compatible avec transmission ANCRE → VERA
- Support des requêtes de vérification
- Export complet de chaîne
# NAV v0.1
