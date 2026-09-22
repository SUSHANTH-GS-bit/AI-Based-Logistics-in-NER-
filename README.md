<div align="center">
🛣️ ResQ Byte
AI-Powered Smart Logistics & Accessibility Intelligence Platform for the North Eastern Region

Smart India Hackathon 2026 · Problem Statement SIH26002 · Ministry of Development of North Eastern Region (MDoNER)

Live Demo Show Image Show Image Show Image Show Image Show Image Show Image

Connecting Data. Predicting Risk. Enabling Safer Logistics Across NER.

Live Prototype · Problem Statement · Features · Architecture · Getting Started · Dataset

</div>
📖 Table of Contents
Problem Statement
The Vision
What ResQ Byte Does
Live Demo
System Architecture
AI / ML Intelligence
GIS & Spatial Intelligence
Offline-First & Multilingual Support
Data Foundation
Technology Stack
Repository Structure
Getting Started
Screenshots
Roadmap
Team
Acknowledgements & Data Sources
License
🎯 Problem Statement

SIH26002 — AI-Based Smart Logistics and Accessibility Intelligence Platform for the North Eastern Region (NER), sponsored by the Ministry of Development of North Eastern Region (MDoNER).

The North Eastern Region faces recurring logistics and accessibility challenges from difficult terrain, extreme weather, and frequent road disruptions caused by landslides, floods, and infrastructure gaps. Essential goods — medicines, food, fuel, construction material — routinely get delayed reaching remote districts, and no integrated platform currently exists that gives real-time logistics visibility, predictive disruption alerts, and optimized transport planning for the region.

Landslide incidents in the NER have risen ~236% over eight years — from 276 events in 2015-16 to 928 in 2023-24 — driven by heavier monsoon rainfall, steep and fragile geology, deforestation, and climate change. ResQ Byte exists to turn that rising risk into actionable, real-time intelligence.

🌏 The Vision

Build a connected intelligence layer for the NER that transforms scattered geographical and operational data into clear, actionable information for logistics, transportation, and emergency accessibility.

<div align="center">

Better Data → Smarter Decisions → Safer NER

</div>
🚀 What ResQ Byte Does
	Capability	Description
🧠	AI Road-Risk Prediction	Predicts landslide/flood disruption risk per road segment from rainfall, slope, terrain and history
🗺️	Smart & Alternative Routing	Plans routes that account for risk and disruption, not just distance
📍	GIS Risk Visualization	Interactive map of roads, risk zones, and terrain across all 8 NER states
🚚	Live Vehicle & GPS Tracking	Real-time visibility into essential-cargo vehicles moving through the region
⛰️	Landslide & Closure Intelligence	Historical landslide inventory, susceptibility zoning, and closure-duration prediction
🏥	Accessibility Mapping	Locates essential facilities — hospitals, warehouses, fuel stations, bridges, settlements
🌐	Multilingual Safety Alerts	Warnings in English, Assamese, Khasi, Mizo, Meiteilon, Nagamese, Bodo, Nepali & Bengali
📴	Offline-First Field Reporting	Collects incident reports without signal, syncs automatically once reconnected
🔗 Live Demo

Working prototype: ai-based-logistics-in-ner-7yto.vercel.app

Deployed on Vercel. Best viewed on desktop for the full map experience.

🏗️ System Architecture
Data SourcesGIS · Weather · History · GPS· Incidents
Data ProcessingCleaning & FeatureEngineering
AI / ML EngineRisk Classification +Duration Regression
PostgreSQL + PostGISSpatial Database
Backend APIsNode.js + Express
Frontend DashboardReact + Leaflet.js
Risk Alerts
Smart Routing
Accessibility Info

The system ingests geographical, weather, historical, and operational data → cleans and engineers features → runs it through the ML engine to generate road-risk predictions → stores everything in a spatial database → serves it through backend APIs → renders it on an interactive GIS frontend.

🤖 AI / ML Intelligence
ML Pipeline
Dataset
Cleaning &Validation
FeatureEngineering
ModelTraining
RiskPrediction
Low / Medium /High Classification

Two models work together:

Model	Type	Predicts	Key Features
Road-Risk Classifier	Random Forest / XGBoost	Segment risk: Low → Medium → High	72h/24h/7d rainfall, slope, elevation, terrain, past incidents, surface quality
Closure-Duration Predictor	Random Forest (regression)	How many hours a closed road stays shut	Landslide volume, material, terrain, road importance, monsoon month

Trained and validated on the SetuNER_Dataset module — see that folder's README for full methodology, feature definitions, and validation results.

🗺️ GIS & Spatial Intelligence

GIS is the geographical foundation of ResQ Byte. The platform represents:

Road networks & risk zones
Landslide locations & susceptibility zoning
Flood and accident incidents
Hospitals, warehouses, fuel stations, bridges, settlements
Live vehicle locations

GeoJSON stores the geographic datasets, PostGIS provides spatial database querying (distance, containment, nearest-neighbour), and Leaflet.js renders it all as an interactive map on the frontend.

📴 Offline-First & Multilingual Support

Connectivity is unreliable across much of the NER, so field data collection follows an offline-first flow:

Yes
No
GPS Tracking /Field Report
Local Storage
Sync Queue
InternetRestored?
AutomaticSynchronization

Alerts and warnings are delivered in the languages people in the region actually speak: English, Assamese, Khasi, Mizo, Meiteilon, Nagamese, Bodo, Nepali, and Bengali.

📊 Data Foundation
Data	Format	Purpose
States & Districts	GeoJSON	Geographic boundaries and locations
Road Network	GeoJSON	Roads, segments, terrain and slope information
Weather	CSV	Rainfall and environmental conditions
Road Risk	CSV	Risk scoring and classification
Incidents	GeoJSON	Landslide, flood, and accident reports
Vehicles & GPS	JSON	Vehicle movement and live locations
Alerts	JSON	Multilingual warning information
Landslide History	CSV	2,834 historical landslide records (2015–2024)
Susceptibility Zones	CSV	Road-level landslide risk zoning (NLSM method)
Road Closures	CSV	Closure duration, impact, and restoration cost

Full detail, methodology, and validation results live in SetuNER_Dataset/README.md.

🛠️ Technology Stack
<table> <tr><td><b>Languages</b></td><td>Python · JavaScript · SQL</td></tr> <tr><td><b>AI & Data</b></td><td>pandas · NumPy · scikit-learn · XGBoost</td></tr> <tr><td><b>GIS</b></td><td>GeoJSON · Leaflet.js · PostGIS</td></tr> <tr><td><b>Backend</b></td><td>Node.js · Express · FastAPI</td></tr> <tr><td><b>Database</b></td><td>PostgreSQL · PostGIS · SQLAlchemy</td></tr> <tr><td><b>Frontend</b></td><td>React · Vite · Leaflet.js</td></tr> <tr><td><b>Deployment</b></td><td>Vercel</td></tr> <tr><td><b>Development</b></td><td>Git · GitHub · VS Code · Google Colab · npm</td></tr> </table>
📁 Repository Structure
AI-Based-Logistics-in-NER-/
│
├── Frontend/                 # React + Vite web app, deployed to Vercel
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # API server
│   ├── src/
│   └── package.json
│
├── ML-ENGINEER/               # Model training notebooks
│   ├── RainFall.ipynb
│   └── Road_Data_Set.ipynb
│
├── SetuNER_Dataset/            # Full dataset: frontend JSON/GeoJSON, backend SQL, ML CSVs
│   ├── frontend/               # districts, roads, incidents, vehicles, alerts, landslides
│   ├── backend/                # schema.sql, seed.sql, server.js (reference API)
│   ├── ml/                     # training CSVs for both ML models
│   ├── docs/                   # plain-language dataset documentation
│   └── README.md               # dataset methodology & validation report
│
├── data/processed/roads/       # processed road datasets
│
├── .env.example                 # environment variable template
├── .gitignore
└── README.md                    # you are here
⚡ Getting Started
Clone the repository
bash
git clone https://github.com/SUSHANTH-GS-bit/AI-Based-Logistics-in-NER-.git
cd AI-Based-Logistics-in-NER-
Frontend setup
bash
cd Frontend
npm install
npm run dev
Backend setup

Open a separate terminal:

bash
cd backend
npm install
npm run dev
Database setup (optional — for full backend functionality)
bash
createdb resqbyte
psql -d resqbyte -c "CREATE EXTENSION postgis;"
psql -d resqbyte -f SetuNER_Dataset/backend/schema.sql
psql -d resqbyte -f SetuNER_Dataset/backend/seed.sql
Machine learning environment

Run the notebooks in ML-ENGINEER/ via Google Colab or a local Python environment:

bash
pip install pandas numpy scikit-learn xgboost
Environment variables

Copy .env.example to .env in each service folder and fill in your own values (database connection string, API keys, etc.) before running.

🖼️ Screenshots

Add screenshots of the live dashboard here — e.g. the risk map, the alerts panel, and the vehicle tracking view — to give visitors an instant sense of the product before they click through to the live demo.

docs/screenshots/
├── dashboard-overview.png
├── risk-map.png
└── vehicle-tracking.png
🔮 Roadmap
 Real-time weather and traffic feed integration (IMD, CWC)
 Satellite-based landslide detection
 Government road-closure data feed
 SMS-based emergency notifications
 Advanced route optimization (OSRM/GraphHopper)
 Additional regional languages
 Automated incident detection from field imagery
 Larger real historical dataset, replacing synthetic training data
 Deep-learning models for longer-horizon risk forecasting
👥 Team
Role	Name
Team Lead / ML	Sushanth G S (@SUSHANTH-GS-bit)
Backend Developer	add name
Frontend Developer	add name
Mobile Developer	add name
GIS / Routing	add name
Presentation / Research	add name

Built for Smart India Hackathon 2026, under the IGNITE entrepreneurship program, REVA University, Bengaluru.

🙏 Acknowledgements & Data Sources

Real-world sources this platform is designed to integrate with in production:

Rainfall & Weather — India Meteorological Department (IMD)
Landslide Records — Geological Survey of India (GSI)
Flood Forecasting — Central Water Commission (CWC)
Road Network Data — OpenStreetMap
Multilingual AI — Bhashini — Digital India
Problem Statement — Smart India Hackathon
📄 License

No license file has been added to this repository yet. For a public hackathon project, the MIT License is a common, permissive choice — add a LICENSE file to formalize this before wider distribution.

<div align="center">
ResQ Byte

Connecting Data. Predicting Risk. Enabling Safer Logistics Across NER.

🔗 Live Demo · ⭐ Star this repo

</div>
Content

PDF
