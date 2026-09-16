#!/usr/bin/env python3
"""
Generates the technical-approach diagrams for the ResQ Byte / SetuNER
(SIH26002) repository as standalone SVG files.

Outputs (next to this script):
    01-system-architecture.svg   - end-to-end layered architecture
    02-technical-approaches.svg  - the technical methods used, at a glance

Run:  python3 docs/diagrams/make_diagrams.py
"""

import os
from html import escape

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "DejaVu Sans, Segoe UI, Helvetica, Arial, sans-serif"

# ---------------------------------------------------------------- palette
BG = "#0B1220"
PANEL = "#101B2E"
PANEL2 = "#0E1729"
STROKE = "#22334D"
INK = "#E6EDF7"
MUTED = "#93A5BF"
DIM = "#6B7F9C"
CYAN = "#22D3EE"
BLUE = "#3B82F6"
PURPLE = "#A855F7"
GREEN = "#10B981"
AMBER = "#F59E0B"
RED = "#EF4444"
PINK = "#EC4899"


# ---------------------------------------------------------------- helpers
def esc(t):
    return escape(str(t), quote=True)


def txt(x, y, s, size=13, fill=INK, weight="normal", anchor="start", op=1.0, ls=0):
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
        f'opacity="{op}" letter-spacing="{ls}">{esc(s)}</text>'
    )


def rect(x, y, w, h, fill=PANEL, stroke=STROKE, rx=12, sw=1.2, op=1.0):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'
    )


def accent_bar(x, y, w, h, color, rx=12):
    """Left accent bar clipped to a rounded card."""
    return (
        f'<path d="M{x + rx},{y} h{w - rx} a{rx},{rx} 0 0 1 {rx},{rx} v{h - 2 * rx} '
        f'a{rx},{rx} 0 0 1 -{rx},{rx} h-{w - rx} z" fill="{color}" opacity="0.95"/>'
    )


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if len(cand) <= max_chars:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bullets(x, y, items, max_chars, size=12.5, lh=19, fill=MUTED, dot=CYAN, dot_size=4):
    """Bulleted multi-line text block. Returns the y after the block."""
    out, cy = [], y
    for it in items:
        wrapped = wrap(it, max_chars)
        cx = x
        out.append(f'<circle cx="{cx + 3}" cy="{cy - 4}" r="{dot_size}" fill="{dot}"/>')
        for i, ln in enumerate(wrapped):
            out.append(txt(cx + 14, cy, ln, size=size, fill=fill))
            cy += lh
        cy += 2
    return "\n".join(out), cy


def chip(x, y, label, color, size=11, pad_x=10, h=22, fill=None, bold=False):
    """Small rounded label. Returns (svg, width)."""
    w = len(label) * size * 0.58 + pad_x * 2
    f = fill if fill else "#16233A"
    svg = (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{f}" '
        f'stroke="{color}" stroke-width="1" opacity="0.95"/>'
        + txt(x + w / 2, y + h / 2 + size * 0.36, label, size=size,
              fill=color, anchor="middle", weight="bold" if bold else "normal")
    )
    return svg, w


def chip_row(x, y, labels, color, size=11, gap=8, h=22):
    out, cx = [], x
    for lb in labels:
        s, w = chip(cx, y, lb, color, size=size, h=h)
        out.append(s)
        cx += w + gap
    return "\n".join(out), cx - x


def down_arrow(cx, y1, y2, color=CYAN, label=None):
    svg = (
        f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2 - 9}" stroke="{color}" '
        f'stroke-width="2" opacity="0.75"/>'
        f'<path d="M{cx - 6},{y2 - 11} L{cx},{y2} L{cx + 6},{y2 - 11} Z" fill="{color}" opacity="0.85"/>'
    )
    if label:
        svg += txt(cx + 12, (y1 + y2) / 2 + 4, label, size=10.5, fill=DIM)
    return svg


def header(w, title, subtitle, badges, height=104):
    out = [
        rect(0, 0, w, height, fill="#0D1729", stroke="none", rx=0),
        f'<line x1="0" y1="{height}" x2="{w}" y2="{height}" stroke="{STROKE}" stroke-width="1"/>',
        txt(38, 46, title, size=26, weight="bold", fill=INK),
        txt(38, 74, subtitle, size=13, fill=MUTED),
    ]
    # right-aligned badges
    cx = w - 38
    for lb in reversed(badges):
        cw = len(lb) * 11.5 * 0.58 + 22
        cx -= cw
        out.append(rect(cx, 30, cw, 26, fill="#14243C", stroke="#2A3D5C", rx=13))
        out.append(txt(cx + cw / 2, 47, lb, size=11.5, fill=CYAN, anchor="middle"))
        cx -= 10
    return "\n".join(out)


def footer(w, h, text):
    lines = text.split("\n")
    top = h - 20 - 18 * len(lines)
    out = [f'<line x1="38" y1="{top}" x2="{w - 38}" y2="{top}" stroke="{STROKE}" stroke-width="1"/>']
    for i, ln in enumerate(lines):
        out.append(txt(38, top + 22 + i * 18, ln, size=11.5, fill=DIM))
    return "\n".join(out)


# ================================================================ DIAGRAM 1
def build_architecture():
    W = 1700
    M = 38                      # page margin
    LABEL_W = 252               # layer label column
    GAP = 16
    CONTENT_X = M + LABEL_W + GAP
    CONTENT_W = W - M - CONTENT_X

    layers = []

    def layer(title, tag, color, cards, height, note=None):
        layers.append(dict(title=title, tag=tag, color=color, cards=cards,
                           height=height, note=note))

    # ---------------------------------------------------- 1. data sources
    layer("DATA SOURCES", "01", CYAN, [
        ("IMD Rainfall", ["daily rainfall at state level (CSV)", "monsoon seasonality, Jun–Sep peak"]),
        ("GSI / NLSM inventory", ["2,834 landslide events, 2015-16 → 2023-24", "type, trigger, volume, runout, losses"]),
        ("OpenStreetMap roads", ["OSMnx 'drive' graph for NER corridors", "saved as ner_roads.gpkg (GeoPackage)"]),
        ("PWD / BRO / NHIDCL logs", ["2,303 road-closure records", "duration + essential-cargo impact"]),
        ("Real geography base", ["9 states · 50 districts · 19 NH corridors", "2011 Census population, elevations"]),
    ], 152)

    # ---------------------------------------------------- 2. data engineering
    layer("DATA ENGINEERING", "02", BLUE, [
        ("generate.py", ["seeded (random.seed(42)) → reproducible", "districts, roads, weather, vehicles, alerts"]),
        ("generate_hazard.py", ["landslide inventory + LSI zonation", "disruption events with durations"]),
        ("make_sql.py / make_hazard_sql.py", ["emits PostGIS DDL + INSERT seed data", "47 schema · 12,030 seed statements"]),
        ("Delivery artifacts", ["GeoJSON / JSON → map-ready layers", "CSV → 8,520 risk + 2,303 duration rows",
                                "schema.sql + seed.sql → PostgreSQL/PostGIS"]),
    ], 168)

    # ---------------------------------------------------- 3. AI / ML
    layer("AI / ML LAYER", "03", PURPLE, [
        ("1 · Risk classifier", ["RandomForest(n_estimators=200, max_depth=10,", "class_weight='balanced') on 16 features",
                                 "→ label low / medium / high"]),
        ("2 · Duration regressor", ["RandomForest(n_estimators=300, max_depth=14)", "target log1p(duration_hours)",
                                    "→ how long a closure will last"]),
        ("3 · Susceptibility zonation", ["NLSM-style weighted-overlay LSI:", "slope 0.26 · rainfall 0.16 · lithology · land use",
                                         "→ every segment classified"]),
        ("4 · Feature engineering", ["rolling 24h / 72h / 7d rainfall windows", "terrain, slope, elevation, soil, surface,",
                                     "bridge count, past-incident history"]),
    ], 196)

    # ---------------------------------------------------- 4. backend
    layer("BACKEND / API", "04", GREEN, [
        ("FastAPI application", ["main.py · Pydantic v2 validation · CORS", "incidents, vehicle GPS, /api/health,",
                                 "/api/db-test, /api/risk/predict"]),
        ("Routers + pluggable services", ["/api/routes · /api/routes/evaluate · /api/sync", "ml_service / gis_service / integration_service",
                                          "hooks: load_model() · connect_engine()"]),
        ("PostgreSQL + PostGIS", ["SQLAlchemy 2 ORM, session per request", "GEOGRAPHY(4326) columns + GIST indexes",
                                  "tables auto-created on boot; migrations script"]),
        ("Reference API (Node/Express)", ["server.js: 39 endpoints over generated JSON", "risk-aware Dijkstra routing engine",
                                          "runs with zero database setup"]),
    ], 196)

    # ---------------------------------------------------- 5. frontend
    layer("FRONTEND / PRESENTATION", "05", AMBER, [
        ("React 18 SPA", ["Vite 5 build · Tailwind CSS 3 · lucide-react", "role-based routing: user vs admin",
                          "11 operator pages + 8 admin pages"]),
        ("Maps & analytics", ["Leaflet + react-leaflet live map:", "vehicles, incidents, facilities, layers",
                              "Recharts KPI / hazard-trend charts"]),
        ("State & device hooks", ["AuthContext + AppContext", "useGPS (simulated or navigator.geolocation)",
                                  "useNetworkStatus · useOfflineSync"]),
        ("Axios service layer", ["vehicleService · incidentService · routeService", "riskService · healthService · accessibilityService",
                                 "VITE_DEMO_MODE → mock data fallback"]),
    ], 190)

    # ---------------------------------------------------- 6. outcomes
    layer("USERS & OUTCOMES", "06", PINK, [
        ("Fleet operators / drivers", ["offline GPS capture, incident reports"]),
        ("Control-room admins", ["fleet, GIS data, ML + system-health views"]),
        ("Planners (MDoNER / PWD)", ["hazard trend, segment burden ranking"]),
        ("Citizens & responders", ["access to hospitals, warehouses, fuel, bridges"]),
    ], 118)

    # ---------------------------------------------------- geometry
    top = 130
    total_h = sum(l["height"] for l in layers) + 26 * (len(layers) - 1)
    H = top + total_h + 120

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    svg.append(header(
        W,
        "ResQ Byte · NER Smart Logistics Platform — System Architecture",
        "AI-Based Smart Logistics & Accessibility Intelligence for North East India · SIH26002 · end-to-end technical flow",
        ["React + Leaflet", "FastAPI + Pydantic", "PostgreSQL / PostGIS", "scikit-learn", "OSMnx"],
    ))

    y = top
    for i, L in enumerate(layers):
        c = L["color"]
        svg.append(rect(M, y, W - 2 * M, L["height"], fill=PANEL2, stroke="#1B2A42", rx=16))
        # label column
        svg.append(rect(M, y, LABEL_W, L["height"], fill="#0F1B2D", stroke="#1B2A42", rx=16))
        svg.append(f'<rect x="{M}" y="{y}" width="5" height="{L["height"]}" fill="{c}" opacity="0.9"/>')
        svg.append(txt(M + 22, y + 42, L["tag"], size=22, weight="bold", fill=c, op=0.55))
        lsize = min(15, max(10.5, (LABEL_W - 40) / (len(L["title"]) * 0.72)))  # caps are wide
        svg.append(txt(M + 22, y + 74, L["title"], size=lsize, weight="bold", fill=INK))

        # cards
        cards = L["cards"]
        n = len(cards)
        cw = (CONTENT_W - (n - 1) * 12) / n
        cy = y + 16
        ch = L["height"] - 32
        for j, (title, body) in enumerate(cards):
            cx = CONTENT_X + j * (cw + 12)
            svg.append(rect(cx, cy, cw, ch, fill="#131F35", stroke="#243553", rx=11))
            svg.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="3.5" rx="1.75" fill="{c}" opacity="0.75"/>')
            svg.append(txt(cx + 14, cy + 28, title, size=13.5, weight="bold", fill=c))
            max_chars = int((cw - 40) / (12 * 0.575))
            blk, _ = bullets(cx + 14, cy + 52, body, max_chars=max_chars, size=12, lh=17.5, dot=c)
            svg.append(blk)

        if i < len(layers) - 1:
            svg.append(down_arrow(M + LABEL_W / 2, y + L["height"] + 2, y + L["height"] + 24, color=c))
        y += L["height"] + 26

    note_y = y + 2
    svg.append(rect(M, note_y, W - 2 * M, 62, fill="#0F1B2D", stroke="#1B2A42", rx=12))
    svg.append(txt(M + 20, note_y + 26,
                   "Data flow: real-world sources  →  seeded Python generation  →  ML + GIS models  →  REST API  →  React GIS dashboard  →  logistics decisions.",
                   size=12.5, fill=MUTED))
    svg.append(txt(M + 20, note_y + 47,
                   "Synthetic layers (weather, incidents, GPS, closures) are labelled as such and swap 1-for-1 with IMD / GSI-NLSM / PWD-BRO feeds — the schema and API contracts do not change.",
                   size=12.5, fill=DIM))

    svg.append(footer(W, H, "ResQ Byte · AI-Based-Logistics-in-NER · architecture generated from the repository source (docs/diagrams/make_diagrams.py)"))
    svg.append("</svg>")
    return "\n".join(svg)


def _finish(parts, W, H):
    """Patch the placeholder canvas size in and close the SVG."""
    body = "\n".join(parts)
    body = body.replace(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="0" viewBox="0 0 {W} 0">',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    return body + "\n</svg>"


# ================================================================ DIAGRAM 2
def build_approaches():
    W = 1700
    M = 38
    H = 0  # set after layout

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="0" viewBox="0 0 {W} 0">']
    svg.append(header(
        W,
        "Technical Approaches Used in the Repository",
        "Six engineering methods that make up the platform — each card is a technique, its implementation, and its measured result",
        ["6 approaches", "verified metrics"], height=96,
    ))

    cards = [
        dict(tag="DATA ENGINEERING", color=CYAN, title="1 · Physics-informed synthetic dataset",
             lead="One risk formula drives training labels, live segment status and the prediction API — so the dataset cannot be self-inconsistent.",
             bullets=[
                 "Versioned generators with random.seed(42) → reproducible artifacts; every foreign key cross-resolves (0 errors)",
                 "Hazard inventory calibrated to the published NER trend: 276 events (2015-16) → 928 (2023-24), a ~236% rise",
                 "79% rainfall / 12% road-cut / 6% toe-erosion / 3% seismic trigger mix matches real GSI inventories",
                 "Monsoon-weighted, heavy-tailed volumes, state-wise wetness (Meghalaya ≈ 2.3× Manipur)",
             ],
             chips=[("8,520 risk rows", CYAN), ("2,303 duration rows", CYAN), ("0 FK errors", CYAN)]),

        dict(tag="MACHINE LEARNING", color=PURPLE, title="2 · Two supervised heads (classification + regression)",
             lead="Risk now, and recovery time after a failure — two scikit-learn Random Forest models served by two endpoints.",
             bullets=[
                 "Classifier: RandomForest(n_estimators=200, max_depth=10, class_weight='balanced') → low / medium / high",
                 "Regressor: RandomForest(n_estimators=300, max_depth=14) on log1p(duration_hours) → closure duration",
                 "Feature engineering: rolling 24h / 72h / 7d rainfall windows exposed as the SQL view v_rainfall_features (train == serve)",
                 "Target leakage removed (closure_type, severity deleted); earlier draft scored an inflated R²",
             ],
             chips=[("91.7–93.1% accuracy", PURPLE), ("R² 0.870", PURPLE), ("MAE ≈ 31 h", PURPLE)]),

        dict(tag="GEO-SPATIAL", color=GREEN, title="3 · GIS data model & connected road graph",
             lead="Real geography, PostGIS-native storage, and a network that is actually routable end to end.",
             bullets=[
                 "OSMnx drive graph → GeoPackage; NER modelled as 71 road segments on 71 town junctions across 19 NH corridors",
                 "PostgreSQL + PostGIS: GEOGRAPHY(…, 4326) columns with GIST indexes → ST_DWithin distance queries in metres",
                 "Defect found and fixed: the graph had 5 disconnected components (Sikkim, Tripura, Arunachal unreachable) — linked via Siliguri gateway, Rangpo, Karimganj, Bhalukpong → 1 component",
                 "Five analytic SQL views (district status, latest vehicle, rainfall features, hazard trend, segment burden) keep the API thin",
             ],
             chips=[("1 connected graph", GREEN), ("39/39 endpoints pass", GREEN), ("PostGIS GIST", GREEN)]),

        dict(tag="ROUTING", color=BLUE, title="4 · Risk-aware shortest path (Dijkstra)",
             lead="Routing that treats a landslide as a cost, not just a pin on a map.",
             bullets=[
                 "Dijkstra over a town-junction graph — district-level graphs silently dropped intra-district legs",
                 "Edge cost = length_km + 0.5 × estimated_delay_min + 10⁶ penalty when blocked or high-risk → the path self-diverts around hazards",
                 "Accepts a district id or a town name; returns corridor geometry (MultiLineString) with per-leg risk, delay and status",
                 "Reusable as an evaluation service: POST /api/routes/evaluate fuses GIS paths with ML risk scores",
             ],
             chips=[("avoid_risk=high|medium|low", BLUE), ("per-leg risk + delay", BLUE)]),

        dict(tag="INTEGRATION", color=AMBER, title="5 · Pluggable service contracts (parallel teams)",
             lead="Frontend → FastAPI → GIS service → ML service → unified evaluated routes, with every seam swappable.",
             bullets=[
                 "Service singletons expose hooks (load_model(), connect_engine()) so a model artifact or routing engine drops in without touching endpoints",
                 "Honest degraded states instead of fake success: MODEL_NOT_CONNECTED, GIS_NOT_CONNECTED, SERVICES_NOT_CONNECTED with per-service status",
                 "Pydantic v2 schemas validate every request (lat/long bounds, non-negative rainfall) and document the contract at /docs",
                 "Node/Express reference API decouples the demo from the database and pins the JSON response shapes",
             ],
             chips=[("drop-in model swap", AMBER), ("no API change", AMBER)]),

        dict(tag="RESILIENCE", color=RED, title="6 · Offline-first sync & graceful degradation",
             lead="Built for NER field conditions: long dead zones, intermittent 2G, and demos on a laptop with no database.",
             bullets=[
                 "Client queues GPS pings and incidents in localStorage while offline, then auto-syncs on the browser 'online' event",
                 "Idempotent batch upload: each record carries client_record_id, so retries return synced / duplicate / failed per record — no double counting",
                 "Frontend falls back to bundled mock datasets (VITE_DEMO_MODE) whenever the API is unreachable, so the UI never breaks",
                 "Health probes (/api/health, /api/db-test) drive the admin system-health page and offline banners",
             ],
             chips=[("POST /api/sync", RED), ("idempotent retries", RED), ("mock fallback", RED)]),
    ]

    # ---- 3 × 2 grid
    cols, gap = 3, 22
    cw = (W - 2 * M - (cols - 1) * gap) / cols
    ch = 386
    top = 118
    for i, c in enumerate(cards):
        col, row = i % cols, i // cols
        x = M + col * (cw + gap)
        y = top + row * (ch + 22)
        svg.append(rect(x, y, cw, ch, fill=PANEL, stroke=STROKE, rx=16))
        svg.append(f'<rect x="{x}" y="{y}" width="{cw}" height="5" rx="2.5" fill="{c["color"]}" opacity="0.85"/>')
        svg.append(txt(x + 20, y + 32, c["tag"], size=11, weight="bold", fill=c["color"], ls=1.4))
        svg.append(txt(x + 20, y + 60, c["title"], size=15.5, weight="bold", fill=INK))
        lead_lines = wrap(c["lead"], int((cw - 46) / (12.5 * 0.57)))
        yy = y + 84
        for ln in lead_lines:
            svg.append(txt(x + 20, yy, ln, size=12.5, fill="#B9C8DE"))
            yy += 18
        yy += 8
        blk, yy = bullets(x + 20, yy, c["bullets"], max_chars=int((cw - 52) / (11.5 * 0.57)),
                          size=11.5, lh=16.5, dot=c["color"], dot_size=3.2)
        svg.append(blk)
        # chips pinned to the card bottom
        cx = x + 20
        cyy = y + ch - 34
        for label, col2 in c["chips"]:
            s, w = chip(cx, cyy, label, col2, size=10.5, h=21)
            if cx + w > x + cw - 16:
                break
            svg.append(s)
            cx += w + 7

    # ---- risk formula strip
    fy = top + 2 * (ch + 22) + 6
    fh = 252
    svg.append(rect(M, fy, W - 2 * M, fh, fill=PANEL2, stroke="#1B2A42", rx=16))
    svg.append(rect(M, fy, 5, fh, fill=PINK, rx=2.5, op=0.9))
    svg.append(txt(M + 22, fy + 34, "THE RISK-SCORE FORMULA — the physics the ML models learn", size=14, weight="bold", fill=PINK))
    svg.append(txt(M + 22, fy + 57,
                   "The same weighted formula generates the training labels, the live segment status and the /api/predict-risk response, so the model learns a real signal rather than noise (labels carry σ = 0.35 noise so the task is not trivial).",
                   size=12, fill=MUTED))

    terms = [
        ("rainfall_72h ÷100 × 2.6", CYAN, "saturated soil — main trigger"),
        ("rainfall_24h ÷100 × 1.7", CYAN, "today's burst"),
        ("rainfall_7d ÷400 × 1.1", CYAN, "season-long saturation"),
        ("avg_slope ÷10 × 1.5", GREEN, "steeper slopes fail sooner"),
        ("elevation ÷1000 × 0.45", GREEN, "exposed, fragile terrain"),
        ("past_incidents × 0.55", AMBER, "history repeats"),
        ("surface_quality 0 / 0.5 / 1.2", AMBER, "poor roads degrade faster"),
        ("bridge_count × 0.10", AMBER, "more structures, more failures"),
        ("near_river < 1.5 km → +0.7", BLUE, "scour / flood exposure"),
        ("plains flood term × 1.8 − 0.8", BLUE, "plains flood, not slide"),
    ]
    tx, ty = M + 22, fy + 78
    per_row = 5
    col_w = (W - 2 * M - 44) / per_row
    for i, (term, col, why) in enumerate(terms):
        r, cidx = divmod(i, per_row)
        x = tx + cidx * col_w
        y = ty + r * 52
        svg.append(rect(x, y, col_w - 16, 42, fill="#132038", stroke="#243553", rx=9))
        svg.append(f'<circle cx="{x + 14}" cy="{y + 14}" r="4" fill="{col}"/>')
        svg.append(txt(x + 26, y + 18, term, size=11.5, weight="bold", fill=INK))
        svg.append(txt(x + 26, y + 33, why, size=10.5, fill=DIM))

    # ---- thresholds
    ty2 = fy + fh - 48
    svg.append(txt(M + 22, ty2 + 6, "Label thresholds:", size=12, weight="bold", fill=MUTED))
    bx = M + 150
    segs = [("LOW  < 6.5", GREEN, "35% of road-days"), ("MEDIUM  6.5 – 9.8", AMBER, "38% of road-days"),
            ("HIGH  ≥ 9.8", RED, "27% of road-days")]
    for label, col, share in segs:
        w = 200
        svg.append(rect(bx, ty2 - 15, w, 30, fill="#132038", stroke=col, rx=15))
        svg.append(txt(bx + 16, ty2 + 5, label, size=12, weight="bold", fill=col))
        svg.append(txt(bx + w + 12, ty2 + 5, share, size=11, fill=DIM))
        bx += w + len(share) * 7 + 40

    H = fy + fh + 84
    svg.append(footer(
        W, H,
        "Generated from the repository source · docs/diagrams/make_diagrams.py"
        "\nKnown gap worth fixing: the SPA requests /api/ml/predict, /api/gis/routes and /api/gis/facilities, while FastAPI exposes /api/risk/predict,"
        "\n/api/routes and /api/routes/evaluate — adding endpoint aliases would light up the live data path end to end."))
    return _finish(svg, W, H)




# ================================================================ DIAGRAM 3
def build_simple():
    """One-page, plain-language overview: what the platform does and why."""
    W, M = 1700, 40
    H = 1012

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>']

    def centre(cx, y, s, size=14, fill=MUTED, weight="normal"):
        return txt(cx, y, s, size=size, fill=fill, weight=weight, anchor="middle")

    # ---------------------------------------------------------------- header
    svg.append(txt(M, 62, "How ResQ Byte Works", size=32, weight="bold", fill=INK))
    svg.append(txt(M, 92, "AI-based logistics and accessibility platform for North East India — explained simply",
                   size=15, fill=MUTED))

    # ---------------------------------------------------------------- flow row
    steps = [
        ("1", "DATA", ["Real North-East map, plus", "rainfall, roads, landslide", "and road-closure records"], CYAN),
        ("2", "BUILD", ["Python scripts generate", "one consistent dataset", "(reproducible, seeded)"], BLUE),
        ("3", "TRAIN", ["Machine learning learns", "landslide risk and how", "long a road stays blocked"], PURPLE),
        ("4", "SERVE", ["FastAPI + PostgreSQL /", "PostGIS answer requests", "from the app"], GREEN),
        ("5", "SHOW", ["React dashboard with", "live maps, vehicles,", "incidents and alerts"], AMBER),
        ("6", "USE", ["Drivers, control room", "and planners choose", "safer routes and act fast"], PINK),
    ]
    gap = 26
    bw = (W - 2 * M - (len(steps) - 1) * gap) / len(steps)
    by, bh = 132, 236

    for i, (num, title, lines, col) in enumerate(steps):
        x = M + i * (bw + gap)
        svg.append(rect(x, by, bw, bh, fill=PANEL, stroke=STROKE, rx=18))
        svg.append(f'<rect x="{x}" y="{by}" width="{bw}" height="6" rx="3" fill="{col}"/>')
        cx = x + bw / 2
        svg.append(f'<circle cx="{cx}" cy="{by + 52}" r="24" fill="{col}" opacity="0.16"/>')
        svg.append(f'<circle cx="{cx}" cy="{by + 52}" r="24" fill="none" stroke="{col}" stroke-width="1.5"/>')
        svg.append(centre(cx, by + 60, num, size=21, fill=col, weight="bold"))
        svg.append(centre(cx, by + 110, title, size=21, fill=INK, weight="bold"))
        for j, ln in enumerate(lines):
            svg.append(centre(cx, by + 146 + j * 24, ln, size=14, fill=MUTED))
        if i < len(steps) - 1:
            ax = x + bw + gap / 2
            svg.append(f'<path d="M{ax - 10},{by + bh / 2 - 8} L{ax + 6},{by + bh / 2} L{ax - 10},{by + bh / 2 + 8} Z" '
                       f'fill="{col}" opacity="0.6"/>')

    # ---------------------------------------------------------------- six ideas
    iy = by + bh + 46
    svg.append(txt(M, iy, "Six simple ideas behind it", size=23, weight="bold", fill=INK))
    svg.append(txt(M, iy + 26, "Each one is a real technique in the code — no jargon needed.",
                   size=14, fill=MUTED))

    ideas = [
        (CYAN, "Physics-based dataset",
         "One risk formula creates the data, trains the model and powers the API, so all three always agree."),
        (PURPLE, "Two AI models",
         "Random Forest models predict landslide risk (91.7% accurate) and how long a closure will last (R² 0.87)."),
        (GREEN, "Real, connected road map",
         "71 highway segments across 19 corridors, joined into a single connected network stored in PostGIS."),
        (BLUE, "Risk-aware routing",
         "Routes automatically avoid blocked or high-risk roads instead of just showing the shortest path."),
        (AMBER, "Plug-in modules",
         "Machine-learning and GIS engines snap in later without changing the API, so teams can build in parallel."),
        (RED, "Works offline",
         "Field reports save on the device and sync automatically when the network returns — no duplicates."),
    ]
    cg, cw2 = 30, (W - 2 * M - 30) / 2
    chh, top2 = 108, iy + 46

    for i, (col, title, body) in enumerate(ideas):
        cx = M + (i % 2) * (cw2 + cg)
        cy = top2 + (i // 2) * (chh + 18)
        svg.append(rect(cx, cy, cw2, chh, fill=PANEL2, stroke="#1B2A42", rx=14))
        svg.append(f'<rect x="{cx}" y="{cy}" width="6" height="{chh}" rx="3" fill="{col}"/>')
        svg.append(f'<circle cx="{cx + 44}" cy="{cy + 54}" r="15" fill="{col}" opacity="0.18"/>')
        svg.append(txt(cx + 44, cy + 60, str(i + 1), size=15, weight="bold", fill=col, anchor="middle"))
        svg.append(txt(cx + 74, cy + 45, title, size=19, weight="bold", fill=INK))
        svg.append(txt(cx + 74, cy + 74, body, size=14, fill=MUTED))

    # ---------------------------------------------------------------- numbers
    ny = top2 + 3 * (chh + 18) + 14
    svg.append(rect(M, ny, W - 2 * M, 96, fill="#0F1B2D", stroke="#1B2A42", rx=16))
    stats = [("8,520", "training rows", CYAN), ("2,303", "closure records", CYAN),
             ("71", "road segments", GREEN), ("50", "districts", GREEN),
             ("91.7%", "risk accuracy", PURPLE), ("R² 0.870", "duration model", PURPLE),
             ("39", "API endpoints", AMBER)]
    sw = (W - 2 * M) / len(stats)
    for i, (big, small, col) in enumerate(stats):
        cx = M + i * sw + sw / 2
        svg.append(txt(cx, ny + 46, big, size=26, weight="bold", fill=col, anchor="middle"))
        svg.append(txt(cx, ny + 72, small, size=13, fill=MUTED, anchor="middle"))
        if i:
            svg.append(f'<line x1="{M + i * sw}" y1="{ny + 22}" x2="{M + i * sw}" y2="{ny + 74}" '
                       f'stroke="{STROKE}" stroke-width="1"/>')

    svg.append(txt(M, H - 24, "ResQ Byte · AI-Based-Logistics-in-NER · generated by docs/diagrams/make_diagrams.py",
                   size=12, fill=DIM))
    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    files = {
        "01-system-architecture.svg": build_architecture(),
        "02-technical-approaches.svg": build_approaches(),
        "03-simple-overview.svg": build_simple(),
    }
    for name, content in files.items():
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", path, f"({len(content) // 1024} KB)")
