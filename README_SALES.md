
# FoodCost – Sales & Margin Integration

> **Added July 23 2025** – automatic import z Papu.io + zakładka *Sprzedaż*.

## Nowe features
| Moduł | Co robi |
|-------|---------|
| **`app/sales/models_sales.py`** | tabele `orders`, `order_items`, `order_aliases` |
| **`app/sales/ingestor_rest.py`** | pobiera zamówienia REST-em (co 5 min) |
| **`app/sales/scheduler.py`** | pętla background w FastAPI |
| **`app/sales/router.py`** | `/api/sales/*` – live dane + mapowanie aliasów |
| **`/backend/requirements.txt`** | + `requests` |

### Endpointy
```http
GET /api/sales/live?hours=24
GET /api/sales/aliases/unmapped
POST /api/sales/aliases/{alias_id}/map/{recipe_id}
```

### Env‑vars
```bash
export PAPU_API_TOKEN="xxx"
export PAPU_LOCATION_ID=801
```

### Uruchomienie
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
