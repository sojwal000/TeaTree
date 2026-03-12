# 🌿 Wild Tea Tree Big Data Visualization Platform

A web-based data management, analytics, and visualization platform for wild tea tree research. Built with **FastAPI**, **MongoDB**, and vanilla **HTML/JavaScript** with **ECharts**, **Chart.js**, and **Leaflet.js**.

---

## Features

| Module | Description |
|--------|-------------|
| **User Authentication** | Registration, login, JWT-based auth, profile management |
| **Tree Data Management** | CRUD operations, CSV bulk import, image upload, search & filtering |
| **Environmental Data** | Temperature, humidity, wind speed, CO₂ level tracking |
| **Geospatial Map** | Interactive Leaflet.js map with marker clustering, elevation filtering & image popups |
| **Dashboard** | Distribution charts, scatter plots, ring count visualization, health & alert widgets |
| **Analytics Engine** | Correlation analysis, linear regression, ANOVA, age estimation, scatter matrix |
| **AI Health Prediction** | Image-based health analysis using color/canopy metrics — score, issues & recommendations |
| **Real-Time Climate** | Open-Meteo API — current weather, hourly & 7-day forecasts per tree location |
| **Satellite / NDVI** | NASA POWER API — vegetation health index, temperature, precipitation & solar radiation |
| **Smart Search & Reports** | Fuzzy search across trees, comprehensive research report generation with print support |
| **Alert System** | Automated weather & health alerts with severity tracking and resolution management |
| **Mobile Responsive** | Hamburger menu, responsive grids, touch-friendly UI across all pages |

---

## ✅ Current Features Checklist

### 🔐 Authentication & Users
- [x] User registration & login
- [x] JWT-based authentication
- [x] User profile management

### 🌳 Tree Data Management
- [x] Create / Read / Update / Delete tree records
- [x] CSV bulk import (up to 300+ records)
- [x] Image upload & gallery per tree
- [x] Search & filter by location, height, diameter, elevation

### 🌡️ Environmental Records
- [x] Log temperature, humidity, wind speed, CO₂ levels
- [x] Per-tree environmental history
- [x] Environmental summary statistics

### 🗺️ Geospatial Map
- [x] Interactive Leaflet.js map with marker clustering
- [x] Elevation range filtering
- [x] Image popups on map markers
- [x] Tree count badge & color legend

### 📊 Dashboard & Analytics
- [x] Distribution charts (height, diameter, elevation, ring count)
- [x] Correlation heatmap & scatter matrix
- [x] Linear regression with R² highlight
- [x] ANOVA testing
- [x] Age estimation model
- [x] Health overview widget
- [x] Alert summary widget

### 🤖 AI Health Prediction
- [x] Image-based health analysis (color & canopy metrics)
- [x] Health score (0–100) with grade (Excellent → Critical)
- [x] Disease / issue detection from uploaded photos
- [x] Actionable recommendations per tree
- [x] Health check history per tree
- [x] Platform-wide health summary

### 🌤️ Real-Time Climate Data
- [x] Live weather via Open-Meteo API (no key required)
- [x] Current conditions (temperature, humidity, wind, rain)
- [x] 7-day daily forecast per tree location
- [x] Hourly forecast data

### 🛰️ Satellite / NDVI Monitoring
- [x] Vegetation Health Index (VHI) via NASA POWER API
- [x] NDVI proxy, temperature, precipitation & solar radiation
- [x] Per-tree satellite lookup
- [x] Region-wide vegetation summary table
- [x] Colored health badges (Excellent → Critical)

### 🔍 Smart Search & Reports
- [x] Fuzzy search across all tree records
- [x] Custom report generation (summary stats, location breakdown, correlations)
- [x] Report history
- [x] Print / export report support

### 🔔 Alert & Notification System
- [x] Automated weather alert scanning
- [x] Health-based alerts for at-risk trees
- [x] Severity levels: Critical / Warning / Info
- [x] Alert resolution & dismissal
- [x] Alert summary dashboard

### 📱 Mobile Responsive
- [x] Hamburger menu on small screens
- [x] Responsive grids (4-col → 2-col → 1-col)
- [x] Scrollable tables on mobile
- [x] Touch-friendly buttons & controls

---

## 🗺️ Add-On Features Roadmap

### 1. 🤖 AI-Based Tea Tree Health Prediction
- [x] Predict plant health from uploaded images
- [x] Detect weak or dying trees using ML scoring
- [x] Early warning alerts for ecosystem health
- [ ] Deep learning model (CNN) for disease classification
- [ ] Multi-class plant disease taxonomy
- [ ] Batch image analysis for entire forest sections

### 2. 🌤️ Real-Time Climate Data Integration
- [x] Live weather updates via Open-Meteo API
- [x] Per-tree current conditions & 7-day forecast
- [ ] Rainfall vs. growth correlation analytics
- [ ] Climate change trend forecasting (multi-year)
- [ ] Historical climate data overlay on analytics

### 3. 🛰️ Satellite Image Analysis
- [x] Vegetation index (NDVI proxy) via NASA POWER
- [x] Regional vegetation health summary
- [ ] True satellite image tile overlay on map
- [ ] Forest cover change detection (year-over-year)
- [ ] Seasonal tea growth cycle monitoring

### 4. 🔍 Smart Search & Filtering
- [x] Filter by location, elevation, height, diameter
- [x] Quick data exploration dashboard
- [x] Custom report generation
- [ ] Filter by year planted / estimated age
- [ ] Filter by tree health grade
- [ ] Saved search presets

### 5. 📱 Mobile-Friendly Dashboard
- [x] Responsive web design across all pages
- [x] Field researchers can access on phone/tablet
- [ ] Offline data viewing (Service Worker / PWA)
- [ ] Offline data entry with sync on reconnect
- [ ] Native app (React Native / Flutter) wrapper

### 6. 🔔 Alert & Notification System
- [x] Automated unusual weather alerts
- [x] Disease / health outbreak warnings
- [x] Growth performance alerts
- [ ] Push notifications (browser / email)
- [ ] Alert subscription preferences per user
- [ ] Scheduled periodic alert scans (cron)

---

## Tech Stack

- **Backend:** Python FastAPI (REST API)
- **Database:** MongoDB (via Motor async driver)
- **Frontend:** HTML / JavaScript / CSS
- **Charts:** ECharts 5, Chart.js 4
- **Maps:** Leaflet.js + MarkerCluster
- **Analytics:** Pandas, NumPy, Scikit-learn, SciPy
- **Image Analysis:** Pillow + NumPy (AI health prediction)
- **HTTP Client:** httpx (async external API calls)
- **External APIs:** Open-Meteo (FREE, no key) · NASA POWER (FREE, no key)

---

## Project Structure

```
TeeTree/
├── main.py                      # FastAPI app entry point
├── seed_data.py                 # Database seed script (300 sample trees)
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration
├── backend/
│   ├── config.py                # Settings (MongoDB URL, JWT secret)
│   ├── database.py              # MongoDB connection management
│   ├── models.py                # Pydantic request/response models
│   ├── auth.py                  # Password hashing & JWT utilities
│   └── routes/
│       ├── auth_routes.py       # /api/auth/* endpoints
│       ├── tree_routes.py       # /api/trees/* + image upload endpoints
│       ├── environmental_routes.py  # /api/environmental/* endpoints
│       ├── analytics_routes.py  # /api/analytics/* endpoints
│       ├── map_routes.py        # /api/map/* endpoints
│       ├── health_routes.py     # /api/health/* AI health prediction
│       ├── climate_routes.py    # /api/climate/* Open-Meteo weather
│       ├── satellite_routes.py  # /api/satellite/* NASA POWER NDVI
│       ├── report_routes.py     # /api/reports/* search & reports
│       └── alert_routes.py      # /api/alerts/* alert management
└── frontend/
    ├── styles.css               # Global stylesheet
    ├── app.js                   # Shared JS utilities & API helpers
    ├── index.html               # Landing page
    ├── login.html               # Login page
    ├── register.html            # Registration page
    ├── dashboard.html           # Main dashboard with charts
    ├── trees.html               # Tree data management (CRUD table)
    ├── tree_detail.html         # Tree detail + health + climate + satellite
    ├── map.html                 # Leaflet.js map visualization
    ├── analytics.html           # Analytics dashboard
    ├── satellite.html           # Satellite / NDVI monitoring
    ├── reports.html             # Smart search & report generation
    ├── alerts.html              # Alert management dashboard
    └── upload.html              # CSV bulk data upload
```

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **MongoDB** running on `localhost:27017` (or update `.env`)

### 1. Install dependencies

```bash
cd TeeTree
pip install -r requirements.txt
```

### 2. Seed the database (optional but recommended)

```bash
python seed_data.py
```

This creates:
- **300 sample tea trees** across 12 Yunnan locations
- **~600 environmental records**
- **Demo user:** `demo@teatree.org` / `demo123`

### 3. Start the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open in browser

Navigate to **http://localhost:8000**

---

## API Endpoints

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Create new user account |
| POST | `/api/auth/login` | Login & get JWT token |
| GET | `/api/auth/profile` | Get current user profile |

### Tree Management
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/trees` | List trees (with filters) |
| POST | `/api/trees` | Create new tree record |
| GET | `/api/trees/{tree_id}` | Get tree by ID |
| PUT | `/api/trees/{tree_id}` | Update tree record |
| DELETE | `/api/trees/{tree_id}` | Delete tree record |
| POST | `/api/trees/upload-csv` | Bulk CSV import |
| POST | `/api/trees/{tree_id}/images` | Upload tree images |

### Environmental Data
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/environmental` | List environmental records |
| POST | `/api/environmental` | Create environmental record |
| GET | `/api/environmental/summary` | Environmental statistics |

### Analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/analytics/summary` | Overall tree statistics |
| GET | `/api/analytics/correlation` | Correlation analysis |
| GET | `/api/analytics/regression` | Linear regression |
| GET | `/api/analytics/anova` | ANOVA testing |
| GET | `/api/analytics/distribution` | Variable distribution histogram |
| GET | `/api/analytics/age-estimation` | Tree age estimation model |
| GET | `/api/analytics/scatter-matrix` | Scatter plot matrix data |

### Map
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/map/trees` | Tree coordinates for map |
| GET | `/api/map/clusters` | Clustered tree data |
| GET | `/api/map/heatmap` | Heatmap overlay data |

### AI Health Prediction
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/health/{tree_id}/check` | Upload image → AI health analysis |
| GET | `/api/health/{tree_id}/history` | Health check history for a tree |
| GET | `/api/health/summary` | Platform-wide health summary |

### Climate Data (Open-Meteo)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/climate/current` | Current weather by lat/lon |
| GET | `/api/climate/forecast` | Daily forecast (up to 16 days) |
| GET | `/api/climate/hourly` | Hourly forecast by lat/lon |
| GET | `/api/climate/tree/{tree_id}` | Current + 7-day forecast for a tree |

### Satellite / NDVI (NASA POWER)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/satellite/vegetation/{tree_id}` | Vegetation health data for a tree |
| GET | `/api/satellite/vegetation` | Vegetation data by coordinates |
| GET | `/api/satellite/region-summary` | Region-wide vegetation health summary |

### Smart Search & Reports
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/reports/search` | Fuzzy search across trees |
| GET | `/api/reports/generate` | Generate comprehensive research report |
| GET | `/api/reports/history` | Previously generated reports |

### Alerts
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/alerts` | Get alerts (filterable by status/severity) |
| GET | `/api/alerts/summary` | Alert counts by severity and type |
| POST | `/api/alerts/check-weather` | Scan all locations for weather alerts |
| POST | `/api/alerts/resolve/{alert_id}` | Mark alert as resolved |
| DELETE | `/api/alerts/{alert_id}` | Delete an alert |

---

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Landing | `/` | Welcome page with login/register |
| Login | `/login` | User authentication |
| Register | `/register` | New account creation |
| Dashboard | `/dashboard` | Charts, health overview & alert widgets |
| Trees | `/trees` | Data table with CRUD & filters |
| Tree Detail | `/tree/{id}` | Tree info + health + climate + satellite + env records |
| Map | `/map` | Interactive Leaflet.js map with image popups |
| Analytics | `/analytics` | Correlation, regression, ANOVA analysis |
| Satellite | `/satellite` | NASA POWER vegetation health monitoring |
| Reports | `/reports` | Smart search & report generation |
| Alerts | `/alerts` | Alert management dashboard |
| Upload | `/upload` | CSV bulk data import |

---

## External APIs

Both external APIs are **free and require no API key**:

- **Open-Meteo** — Real-time weather data, hourly/daily forecasts
- **NASA POWER** — Satellite-derived temperature, precipitation, solar radiation for vegetation health index

---

## License

MIT
