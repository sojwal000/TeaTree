# Wild Tea Tree Big Data Visualization Platform

## Comprehensive Technical Report, Implementation Guide, and Research-Style Documentation

Version: 1.0

Project root: TeeTree/

Related diagrams: See docs/project_mermaid_diagrams.md

---

## Table of Contents

1. Abstract
2. Problem Context and Motivation
3. Goals and Research Questions
4. Scope and Deliverables
5. System Overview
6. Technology Stack and Rationale
7. System Architecture
8. Data Model and Collections
9. Backend Module Documentation
10. Frontend Module Documentation
11. Feature-by-Feature Working Explanation
12. End-to-End Runtime Flow
13. API Design and Endpoint Families
14. Security and Access Control
15. External API Integration Design
16. Analytics and ML Logic
17. Alerting Logic and Decision Rules
18. UI/UX and Responsiveness Strategy
19. Installation, Deployment, and Operations Guide
20. Testing and Validation Strategy
21. Performance and Scalability Notes
22. Reliability, Risks, and Limitations
23. Future Work and Research Extensions
24. Practical Usage Scenarios
25. Troubleshooting Guide
26. Conclusion

---

## 1) Abstract

This project is a full-stack web platform for wild tea tree data management, environmental monitoring, advanced analytics, and ecological decision support. The system combines:

- FastAPI-based backend APIs
- MongoDB for operational data storage
- Vanilla HTML/CSS/JavaScript frontend
- ECharts and Chart.js for analytical visualization
- Leaflet.js for geospatial visualization
- Open-Meteo and NASA POWER APIs for climate/satellite-derived intelligence
- Image-based tree health prediction using computer-vision-inspired feature extraction

The platform supports researchers across collection, monitoring, exploration, analysis, reporting, and alert-based intervention workflows.

---

## 2) Problem Context and Motivation

Wild tea tree ecosystems are geographically distributed and environmentally sensitive. Traditional monitoring methods often suffer from fragmented records, delayed analysis, and weak early-warning capability.

This project addresses those gaps by providing:

- Unified data records per tree
- Continuous environmental and climate context
- Geospatial and statistical analysis tools
- AI-assisted health assessment from tree images
- Automated anomaly and risk alerts
- Report generation for research communication

---

## 3) Goals and Research Questions

### Project goals

- Build a complete data platform for wild tea tree research operations
- Integrate data collection, analytics, mapping, and reporting into one workflow
- Provide practical early warning signals for ecosystem health and weather risk
- Enable field and office teams with mobile-friendly interfaces

### Guiding research questions

- How can tree morphology and site conditions be jointly analyzed at scale?
- Can image-derived signals provide actionable health indicators for early intervention?
- How do climate and satellite proxy signals support short-term ecological monitoring?
- What visualization and reporting patterns best support rapid scientific interpretation?

---

## 4) Scope and Deliverables

### Included

- User authentication with JWT
- Tree CRUD and CSV bulk import
- Image upload and gallery
- Environmental records management
- Statistical analytics (summary, correlation, regression, ANOVA, distribution, age estimation)
- Interactive map and clustering
- AI-based health scoring from uploaded images
- Real-time climate integration
- Satellite/vegetation proxy integration
- Smart search and report generation
- Alert generation and resolution workflow
- Responsive frontend across all pages

### Not fully included (future extension)

- Offline-first synchronization (PWA or local cache sync)
- Deep CNN disease classification model
- Long-term climate trend forecasting model
- True forest cover change from remote-sensing imagery layers
- Push notification channels (email/SMS/web push)

---

## 5) System Overview

The system is organized as a modular monolithic backend with static frontend serving.

- Backend: FastAPI app in main.py, route modules under backend/routes
- Database: MongoDB accessed asynchronously via Motor
- Frontend: Multiple HTML pages with shared styles.css and app.js
- Storage: Uploaded files served from uploads/
- Integrations: Open-Meteo and NASA POWER over HTTP APIs

---

## 6) Technology Stack and Rationale

### Backend

- FastAPI: async support, strong typing, automatic API docs compatibility
- Motor: non-blocking MongoDB access
- Pydantic: schema validation and typed request/response models
- Python scientific stack: pandas, numpy, scipy, scikit-learn

### Frontend

- Vanilla HTML/CSS/JS: low overhead, fast iteration
- ECharts: rich interactive charts and heatmaps
- Chart.js: simple chart rendering for additional views
- Leaflet.js + MarkerCluster: map interaction and dense marker handling

### External data

- Open-Meteo: current and forecast weather (no API key)
- NASA POWER: climate/satellite-derived agro-environmental parameters (no API key)

### Security and auth

- JWT with JOSE
- Password hashing via Passlib (bcrypt)

---

## 7) System Architecture

### High-level flow

1. User opens frontend pages served by FastAPI.
2. Login endpoint returns JWT token.
3. Frontend sends authenticated API requests using Bearer token.
4. Route modules validate input and interact with MongoDB.
5. Analytics and integrations compute enriched responses.
6. Frontend renders tables, cards, charts, maps, and alerts.

For visual architecture, refer to docs/project_mermaid_diagrams.md.

---

## 8) Data Model and Collections

### Core collections

- users
- trees
- environmental_data
- health_records
- alerts
- reports

### Key entity summary

#### users

- user_id (UUID)
- name
- email (unique)
- password_hash
- created_at

#### trees

- tree_id (UUID)
- height, diameter, ring_count
- elevation, latitude, longitude
- location_name
- images[]
- created_by, created_at, updated_at

#### environmental_data

- record_id (UUID)
- tree_id
- temperature, humidity, wind_speed, co2_level
- timestamp

#### health_records

- record_id
- tree_id
- image_path
- health_score, health_status
- metrics (green_ratio, canopy_density, etc.)
- issues[]
- recommendations[]
- analyzed_at, analyzed_by

#### alerts

- alert_id
- title, severity, alert_type
- description
- status (active/resolved)
- location, trees_affected
- metadata
- created_at, resolved_at, resolved_by

#### reports

- report_id
- generated_at
- generated_by
- scope, location
- tree_count

### Data validation

Pydantic models enforce constraints such as:

- latitude in [-90, 90]
- longitude in [-180, 180]
- positive diameter/height values
- bounded humidity values

---

## 9) Backend Module Documentation

### 9.1 main.py

Responsibilities:

- FastAPI app creation and metadata
- CORS middleware setup
- MongoDB startup/shutdown hooks
- Router registration (10 route modules)
- Static file serving (/static and /uploads)
- Frontend page routing for all UI pages

### 9.2 backend/config.py

Responsibilities:

- Environment-backed settings for DB URL, JWT secret, algorithm, token expiry
- Cached settings object for consistent access

### 9.3 backend/database.py

Responsibilities:

- Initialize MongoDB client and database on startup
- Create practical indexes (email, tree_id, geospatial fields, timestamps)
- Close database connection on shutdown
- Provide shared get_database() handle

### 9.4 backend/auth.py

Responsibilities:

- Hash and verify passwords (bcrypt)
- Create JWT access tokens
- Validate Bearer tokens and resolve current user
- Integrate with FastAPI dependency system

### 9.5 backend/models.py

Responsibilities:

- Typed request and response schemas for auth, tree, environment, analytics/filter models
- Input validation and type safety across endpoints

### 9.6 backend/routes/auth_routes.py

Endpoints:

- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/profile
- PUT /api/auth/profile

Working:

- Enforces unique email
- Stores hashed passwords
- Issues JWT on successful login
- Uses auth dependency for profile operations

### 9.7 backend/routes/tree_routes.py

Endpoints:

- POST /api/trees
- GET /api/trees
- GET /api/trees/count
- GET /api/trees/{tree_id}
- PUT /api/trees/{tree_id}
- DELETE /api/trees/{tree_id}
- POST /api/trees/{tree_id}/images
- POST /api/trees/upload-csv

Working:

- Supports rich server-side filtering (location, elevation, diameter, height, search)
- Performs CSV parsing and type conversion
- Stores uploaded image files under uploads/
- Maintains tree image lists in MongoDB

### 9.8 backend/routes/environmental_routes.py

Endpoints:

- POST /api/environmental
- GET /api/environmental
- GET /api/environmental/summary
- DELETE /api/environmental/{record_id}

Working:

- Links environmental records to existing trees
- Returns time-sorted measurements
- Uses MongoDB aggregation for summary statistics

### 9.9 backend/routes/analytics_routes.py

Endpoints:

- GET /api/analytics/summary
- GET /api/analytics/correlation
- GET /api/analytics/regression
- GET /api/analytics/anova
- GET /api/analytics/distribution
- GET /api/analytics/age-estimation
- GET /api/analytics/scatter-matrix

Working:

- Loads tree data into pandas DataFrame
- Performs numerical cleaning/coercion
- Correlation: Pearson matrix and pairwise p-values
- Regression: linear model with coefficients and R squared
- ANOVA: one-way group comparison with significance test
- Distribution: histogram + skewness + kurtosis
- Age estimation: diameter to ring_count regression proxy
- Scatter matrix: sampled data for interactive plotting

### 9.10 backend/routes/map_routes.py

Endpoints:

- GET /api/map/trees
- GET /api/map/clusters
- GET /api/map/heatmap

Working:

- Provides coordinate-centric map payloads
- Supports elevation/location filtering
- Aggregates clusters via coordinate grid binning
- Exposes heatmap points with variable intensity

### 9.11 backend/routes/health_routes.py

Endpoints:

- POST /api/health/{tree_id}/check
- GET /api/health/{tree_id}/history
- GET /api/health/summary

Working:

- Accepts image uploads (JPG/PNG/WEBP)
- Computes health metrics from RGB pixel analysis
- Derives score, status, issues, recommendations
- Stores full health history and summarized latest-state statistics

### 9.12 backend/routes/climate_routes.py

Endpoints:

- GET /api/climate/current
- GET /api/climate/forecast
- GET /api/climate/hourly
- GET /api/climate/tree/{tree_id}

Working:

- Calls Open-Meteo with typed lat/lon inputs
- Converts weather codes to human-readable descriptions
- Returns normalized current, hourly, and daily forecast objects

### 9.13 backend/routes/satellite_routes.py

Endpoints:

- GET /api/satellite/vegetation/{tree_id}
- GET /api/satellite/vegetation
- GET /api/satellite/region-summary

Working:

- Calls NASA POWER daily point API for agro-climate variables
- Filters fill values and builds daily records
- Computes Vegetation Health Index proxy from climate components
- Produces status labels (Excellent, Good, Moderate, Poor, Critical)

### 9.14 backend/routes/report_routes.py

Endpoints:

- GET /api/reports/search
- GET /api/reports/generate
- GET /api/reports/history

Working:

- Implements fuzzy text and numeric range search
- Generates structured research report JSON with overview, location breakdown, environment, and health summaries
- Persists report metadata in reports collection

### 9.15 backend/routes/alert_routes.py

Endpoints:

- GET /api/alerts
- GET /api/alerts/summary
- POST /api/alerts/resolve/{alert_id}
- DELETE /api/alerts/{alert_id}
- POST /api/alerts/check-weather

Working:

- Provides status/severity filterable alert retrieval
- Aggregates summary by severity and type
- Generates weather alerts from current external climate data
- Generates health alerts from low latest health scores
- Supports lifecycle operations (resolve/delete)

---

## 10) Frontend Module Documentation

### Shared frontend modules

#### frontend/styles.css

- Global design system variables
- Responsive breakpoints
- Card, table, button, nav, badge, and utility classes

#### frontend/app.js

- Shared API helper methods
- Token and user profile storage helpers
- Navbar rendering with page highlighting
- Common UI alert helper utilities

### Page modules and responsibilities

- index.html: public landing page
- login.html: authentication entry
- register.html: account creation UI
- dashboard.html: at-a-glance metrics and visual summaries
- trees.html: core data table + CRUD operations
- tree_detail.html: full per-tree intelligence hub (images, health, climate, satellite, records)
- map.html: geospatial exploration and clustering
- analytics.html: statistical analysis workbench
- satellite.html: regional and per-coordinate vegetation monitoring
- reports.html: smart search and report generation
- alerts.html: alert operations center
- upload.html: CSV import workflow

---

## 11) Feature-by-Feature Working Explanation

### 11.1 User authentication

Workflow:

1. User submits register/login form.
2. Backend validates and hashes credentials.
3. JWT token is returned on successful login.
4. Frontend stores token and includes it in Authorization header.
5. Protected endpoints resolve user via token dependency.

### 11.2 Tree data management

Workflow:

1. User creates/updates/deletes records from trees page.
2. Filters are translated into query params.
3. Backend builds Mongo queries and returns sorted datasets.
4. Detail page loads selected tree and linked records.

### 11.3 CSV bulk import

Workflow:

1. User uploads CSV from upload page.
2. Backend validates extension and parses rows.
3. Typed conversions are attempted per row.
4. Valid rows are bulk inserted; invalid rows returned as structured errors.

### 11.4 Image management

Workflow:

1. User uploads one or multiple tree images.
2. Backend checks extension and stores files in uploads/.
3. Paths are appended to tree images array.
4. Frontend gallery displays files and supports preview opening.

### 11.5 Environmental tracking

Workflow:

1. User records measurements per tree.
2. Backend verifies tree existence.
3. Records are timestamped and stored.
4. Summary endpoint provides aggregate statistics for dashboards/reports.

### 11.6 Geospatial map

Workflow:

1. Frontend requests map tree payload.
2. Leaflet renders markers and cluster groups.
3. Popups include key metadata and image previews.
4. Optional heatmap and elevation filtering support exploration.

### 11.7 Analytics engine

Workflow:

1. Frontend calls analysis endpoints with variable selections.
2. Backend fetches and cleans numeric datasets.
3. Statistical models run server-side.
4. Response is visualized with charts/tables and significance indicators.

### 11.8 AI-based health prediction

Workflow:

1. User uploads a leaf/canopy image in tree detail.
2. Backend computes pixel-based health metrics.
3. Health score and status are determined by weighted rules.
4. Potential issues and recommendations are generated.
5. Record is stored for trend/history inspection.

### 11.9 Real-time climate integration

Workflow:

1. Tree coordinates are used to query Open-Meteo.
2. Current and forecast data are normalized by backend.
3. Frontend displays weather cards and forecast table.
4. Alert module reuses weather signals for risk detection.

### 11.10 Satellite vegetation proxy

Workflow:

1. Coordinates are sent to NASA POWER daily point API.
2. Temperature, rainfall, and solar variables are retrieved.
3. Vegetation Health Index proxy is computed.
4. Status is categorized and surfaced in UI/report summaries.

### 11.11 Smart search and reports

Workflow:

1. User enters text or range-like queries.
2. Backend performs regex and numeric-range matching.
3. Result set supports quick exploration.
4. Report generation compiles multi-module summaries and stores report metadata.

### 11.12 Alert and notification system

Workflow:

1. Weather check endpoint scans grouped locations.
2. Rules detect anomalies (extreme heat, frost, strong wind, heavy rain, severe weather).
3. Health risk check flags low-score trees.
4. Alerts are deduplicated and inserted as active.
5. User can resolve or delete alerts.

### 11.13 Mobile responsive dashboard

Working principles:

- Flexible grid layouts and card stacks
- Responsive navbar behavior
- Scrollable data table containers
- Touch-friendly controls and spacing

---

## 12) End-to-End Runtime Flow

1. Application starts and opens MongoDB connection.
2. Static frontend assets and page routes become available.
3. User authenticates and receives JWT token.
4. Core modules fetch and mutate data through protected APIs.
5. Analytics, climate, satellite, and health modules enrich core records.
6. Reports and alerts summarize actionable insights.
7. Application shutdown closes DB connections cleanly.

---

## 13) API Design and Endpoint Families

Endpoint families are organized by responsibility:

- /api/auth/*
- /api/trees/*
- /api/environmental/*
- /api/analytics/*
- /api/map/*
- /api/health/*
- /api/climate/*
- /api/satellite/*
- /api/reports/*
- /api/alerts/*

Design choices:

- Query parameters for filtering and model controls
- Strong JSON response contracts
- Proper HTTP status handling with descriptive errors

---

## 14) Security and Access Control

Implemented controls:

- Password hashing via bcrypt
- JWT token-based authentication
- Dependency-injected user validation for protected operations
- Input validation via Pydantic schemas

Operational recommendations:

- Replace development secret key in production
- Restrict CORS origins in production deployment
- Use HTTPS behind reverse proxy
- Add API rate limiting and audit logging if exposed publicly

---

## 15) External API Integration Design

### Open-Meteo integration

- Used for current, hourly, and daily forecasts
- No API key requirement simplifies deployment
- Weather code mapping implemented for readable UI

### NASA POWER integration

- Used for vegetation-related environmental signals
- Daily series ingestion with missing-value filtering
- Derived VHI proxy for operational ecological interpretation

Resilience notes:

- HTTP exceptions return 502 on upstream failure
- Graceful partial results in some region summary contexts

---

## 16) Analytics and ML Logic

### Statistical analytics

- Correlation: Pearson coefficients + p-values
- Regression: linear model with coefficients and fit quality
- ANOVA: significance of inter-group differences
- Distribution: statistical moments and histogram

### AI health analysis

The current model is rule-based feature engineering on image color-space properties:

- Greenness and excess green for vitality
- Brown and yellow ratios for stress/chlorosis signs
- Dark lesion proxy for possible disease/pest damage
- Canopy density for structural vigor

This design is lightweight, explainable, and suitable for baseline field decision support.

---

## 17) Alerting Logic and Decision Rules

### Weather rule examples

- Temperature > 38 C: critical heat alert
- Temperature < 0 C: frost risk alert
- Wind > 50 km/h: strong wind alert
- Precipitation > 20 mm/h: heavy rainfall alert
- Weather code >= 95: severe weather alert

### Health rule examples

- Latest health score < 40 triggers risk alert
- Lower scores escalate severity
- Duplicate active alerts are avoided through checks

---

## 18) UI/UX and Responsiveness Strategy

Recent implementation characteristics include:

- Consistent card and section rhythm
- Sticky table headers and improved readability
- Unified filter bars and action controls
- Clear severity/status badge language
- Mobile-friendly layout transitions and nav behavior

The frontend supports desktop analysis sessions and field-device access patterns.

---

## 19) Installation, Deployment, and Operations Guide

### Prerequisites

- Python 3.10+
- MongoDB running locally (default mongodb://localhost:27017)
- Internet access for climate/satellite APIs

### Setup

1. Create and activate virtual environment
2. Install dependencies from requirements.txt
3. Configure .env values
4. Optional: run seed_data.py for sample data
5. Start server: uvicorn main:app --reload
6. Open browser at http://localhost:8000

### Operational notes

- uploads/ must remain writable
- MongoDB should be monitored for disk and index health
- Periodic backups are recommended for research integrity

---

## 20) Testing and Validation Strategy

### Suggested validation levels

- Unit tests for helper functions and scoring logic
- API integration tests for each route family
- Frontend smoke tests for key page workflows
- Data quality checks for CSV import
- External API failure simulation tests

### Functional acceptance checks

- Login/register and protected access
- Tree CRUD and filtered listing
- CSV import with mixed valid/invalid rows
- Image upload and gallery display
- Analytics endpoints return valid charts data
- Climate/satellite calls populate views
- Alert generation and resolution lifecycle

---

## 21) Performance and Scalability Notes

### Current strengths

- Async I/O for DB and external HTTP calls
- Indexed key collections for common queries
- Sampling/capping in analytics responses for UI performance

### Scaling roadmap

- Add Redis cache for hot analytics and summaries
- Add background tasks/queue for periodic alert scans
- Introduce pagination strategy for very large datasets
- Separate analytics-heavy workloads if data volume grows significantly

---

## 22) Reliability, Risks, and Limitations

### Risks

- External API dependency outages
- Inconsistent field data quality from manual inputs
- Rule-based health model limitations vs deep learning models

### Current limitations

- Offline mode not implemented
- Trend forecasting not yet implemented as long-range model
- No dedicated notification channel outside in-app alerts

### Mitigations

- Add retries/fallback cache for external APIs
- Introduce data QA rules and validation pipelines
- Incrementally upgrade health model using labeled datasets

---

## 23) Future Work and Research Extensions

- CNN-based disease classifier with explainable output
- Multi-temporal remote sensing for forest cover change
- Rainfall-growth causal analysis and forecasted risk maps
- PWA offline capture and deferred synchronization
- User-customized alert subscriptions and channel delivery
- Role-based access control and audit compliance features

---

## 24) Practical Usage Scenarios

### Scenario A: Field health triage

- Capture image at tree site
- Run health check
- Review score/issues/recommendations
- Create follow-up intervention note via report workflow

### Scenario B: Regional weather risk scan

- Trigger weather alert check
- Review critical and warning alerts by location
- Prioritize field deployment by severity and trees affected

### Scenario C: Research reporting cycle

- Filter target region
- Generate full report
- Print/export and attach to research review

---

## 25) Troubleshooting Guide

### Server does not start

- Confirm MongoDB is running
- Verify Python environment and installed dependencies
- Check .env values and import errors

### No data in charts/maps

- Confirm seeded or uploaded tree data exists
- Verify API endpoints return non-empty payloads
- Check browser console/network calls for auth failures

### External climate/satellite failures

- Check internet connectivity
- Retry request and inspect 502 responses
- Validate coordinates are in valid ranges

### Authentication issues

- Ensure Bearer token is included in protected requests
- Re-login if token expired
- Verify secret key consistency between token creation and decode

---

## 26) Conclusion

The Wild Tea Tree Big Data Visualization Platform is a complete, modular, and practical research operations system that connects ecological data capture, analytics, geospatial insights, climate context, satellite proxy monitoring, AI-assisted health scoring, and alert-driven intervention.

Its current architecture is implementation-ready for academic demonstration and pilot deployments, while retaining clear pathways for research-grade extension in advanced ML, remote sensing, and offline field operations.

---

## Appendix A: Implemented Modules Checklist

### Backend modules

- main.py
- backend/config.py
- backend/database.py
- backend/models.py
- backend/auth.py
- backend/routes/auth_routes.py
- backend/routes/tree_routes.py
- backend/routes/environmental_routes.py
- backend/routes/analytics_routes.py
- backend/routes/map_routes.py
- backend/routes/health_routes.py
- backend/routes/climate_routes.py
- backend/routes/satellite_routes.py
- backend/routes/report_routes.py
- backend/routes/alert_routes.py

### Frontend modules

- frontend/styles.css
- frontend/app.js
- frontend/index.html
- frontend/login.html
- frontend/register.html
- frontend/dashboard.html
- frontend/trees.html
- frontend/tree_detail.html
- frontend/map.html
- frontend/analytics.html
- frontend/satellite.html
- frontend/reports.html
- frontend/alerts.html
- frontend/upload.html
