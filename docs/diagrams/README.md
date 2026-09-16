# Technical approach diagrams

Visual summary of how this repository is built. Everything here is generated from the
repository source by `make_diagrams.py` — no external diagram tool is required.

| File | What it shows |
|---|---|
| `03-simple-overview.svg` / `.png` | **Start here** — plain-language one-pager: DATA → BUILD → TRAIN → SERVE → SHOW → USE, plus the six ideas and headline numbers |
| `01-system-architecture.svg` / `.png` | End-to-end architecture: data sources → data engineering → AI/ML → FastAPI/PostGIS backend → React + Leaflet frontend → users |
| `02-technical-approaches.svg` / `.png` | The six technical approaches used, each with its implementation detail and measured result, plus the shared risk-score formula |
| `index.html` | Gallery view (open in a browser, or serve the folder) |

## Regenerate

```bash
python3 docs/diagrams/make_diagrams.py
```

To view the gallery locally:

```bash
python3 -m http.server 8080 --directory docs/diagrams
# open http://localhost:8080
```

## The six approaches in one paragraph

1. **Physics-informed synthetic dataset** — seeded generators (`generate.py`,
   `generate_hazard.py`, `make_sql.py`) produce cross-referenced GeoJSON / JSON / CSV /
   PostGIS SQL; one risk formula drives labels, live status and the prediction API.
2. **Two supervised ML heads** — a Random Forest classifier (risk: low/medium/high) and a
   Random Forest regressor (closure duration), with rolling 24h/72h/7d rainfall windows as
   shared train/serve features.
3. **GIS data model on a connected road graph** — OSMnx → GeoPackage, 71 segments on
   71 junctions across 19 NH corridors, PostGIS `GEOGRAPHY(4326)` + GIST indexes, and the
   disconnected-component bug fixed so all of NER is routable.
4. **Risk-aware Dijkstra routing** — edge cost = length + 0.5 × delay + a prohibitive
   penalty on blocked/high-risk segments, so routes self-divert around hazards.
5. **Pluggable service contracts** — `ml_service`, `gis_service` and `integration_service`
   expose hooks (`load_model()`, `connect_engine()`) and honest degraded states, so teams
   can work in parallel without breaking API contracts.
6. **Offline-first resilience** — client-side queue in `localStorage`, idempotent batch
   sync keyed by `client_record_id`, and mock-data fallback so the UI never breaks.

## Known gap highlighted in the diagrams

The single-page app requests `/api/ml/predict`, `/api/gis/routes` and `/api/gis/facilities`,
while FastAPI currently exposes `/api/risk/predict`, `/api/routes` and
`/api/routes/evaluate`. Adding alias routes (or updating the frontend service layer) would
connect the live data path end to end; today the frontend falls back to bundled mock data.
