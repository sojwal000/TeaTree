# Mahatma Education Society's

## Pillai HOC College of Engineering & Technology, Rasayani (Autonomous)

### Department of Computer Application (MCA)

## Mini-Project / Research Project

**Academic Year:** ESAY 2025-2026  
**Semester:** ____  
**Group No.:** ____

## Project Title

# Big Data Visualization Platform for Wild Tea Trees

## Updated Module Development Timeline

This document describes the modules currently implemented in the project. The application uses FastAPI and MongoDB rather than Flask and SQLite/PostgreSQL. External services are used only where listed in the API Requirements column.

| Sr. No. | Module | Problem | Solution | Tech Stack | API Requirements | Signature of Guide (After Module Development) with date |
|---:|---|---|---|---|---|---|
| 1 | **Frontend and User Interface** | - No interactive visualization for wild tea tree data<br>- Difficult to view geographic distribution of trees<br>- No user-friendly dashboard for monitoring health<br>- Complex raw data is difficult to interpret visually | - Responsive web interface for dashboards, tree records, maps, analytics, alerts, reports, satellite data, soil health, citizen submissions, regional comparison, climate scenarios, and tree passports<br>- Interactive charts using ECharts and Chart.js<br>- Interactive geographic visualization using Leaflet.js<br>- Shared authentication and API utilities in `frontend/app.js`<br>- Mobile-responsive navigation, grids, tables, forms, and controls | HTML5, CSS3, JavaScript, ECharts 5, Chart.js 4, Leaflet.js, Leaflet MarkerCluster | Internal REST APIs served by FastAPI<br>Leaflet tile provider<br>Open-Meteo and NASA POWER data displayed through backend APIs | ____ |
| 2 | **Backend Core Logic, Authentication, and API** | - No centralized API for tea tree research data<br>- No secure user authentication<br>- Unstructured routes for different data types<br>- Frontend and database operations are not connected through a common service layer | - FastAPI application in `main.py` with registered route modules<br>- JWT-based registration, login, profile retrieval, and profile update<br>- Pydantic models for request and response validation<br>- Central configuration in `backend/config.py`<br>- Shared database connection and indexes in `backend/database.py`<br>- Password hashing and token utilities in `backend/auth.py` | Python, FastAPI, Uvicorn, Pydantic, Pydantic Settings, Motor, PyMongo, `python-jose`, Passlib, `python-dotenv` | `POST /api/auth/register`<br>`POST /api/auth/login`<br>`GET /api/auth/profile`<br>`PUT /api/auth/profile` | ____ |
| 3 | **Tree Data Management and Data Import** | - Tree information is difficult to manage as scattered records<br>- No CRUD workflow for research observations<br>- Manual entry of large datasets is time-consuming<br>- Tree images are not linked to records | - Create, read, update, and delete tree records<br>- Search and filter by location, height, diameter, elevation, and other tree attributes<br>- CSV bulk upload for structured datasets<br>- Multiple image uploads per tree<br>- Sample data initialization through `seed_data.py` and India-focused data through `india_seed_data.py` | Python, FastAPI, MongoDB, Motor, Pydantic, Python multipart uploads, HTML/JavaScript | `POST /api/trees`<br>`GET /api/trees`<br>`GET /api/trees/{tree_id}`<br>`PUT /api/trees/{tree_id}`<br>`DELETE /api/trees/{tree_id}`<br>`POST /api/trees/upload-csv`<br>`POST /api/trees/{tree_id}/images` | ____ |
| 4 | **Environmental Data Management** | - Temperature, humidity, wind speed, and CO2 observations are difficult to organize<br>- No per-tree environmental history<br>- No summary statistics for environmental conditions | - Store environmental records associated with individual trees<br>- Display environmental history in tree detail views<br>- Calculate summary statistics for monitoring and analysis<br>- Feed environmental data into ecosystem health and analytics views | Python, FastAPI, MongoDB, Motor, Pandas, NumPy, HTML/JavaScript | `POST /api/environmental`<br>`GET /api/environmental`<br>`GET /api/environmental/summary`<br>`DELETE /api/environmental/{record_id}` | ____ |
| 5 | **Analytics and Statistical Processing** | - Raw tree data does not show relationships or trends clearly<br>- No correlation or regression analysis<br>- No statistical comparison between groups<br>- Tree age cannot be estimated from available measurements | - Distribution histograms for tree variables<br>- Correlation analysis and heatmap data<br>- Linear regression with model statistics and R-squared value<br>- ANOVA testing<br>- Ring-based age estimation<br>- Scatter matrix data for multivariable exploration | Python, Pandas, NumPy, SciPy, Scikit-learn, FastAPI, ECharts, Chart.js | `GET /api/analytics/summary`<br>`GET /api/analytics/distribution`<br>`GET /api/analytics/correlation`<br>`GET /api/analytics/regression`<br>`GET /api/analytics/anova`<br>`GET /api/analytics/age-estimation`<br>`GET /api/analytics/scatter-matrix` | ____ |
| 6 | **Geospatial Mapping and Spatial Visualization** | - Geographic distribution of trees is difficult to inspect in tabular data<br>- Researchers cannot easily identify clusters or high-density regions<br>- Tree locations, images, and environmental context are separated | - Interactive Leaflet map with tree markers<br>- Marker clustering for dense areas<br>- Elevation filtering and tree count indicators<br>- Heatmap data for spatial density<br>- Popups combining tree information, images, weather, soil, satellite, and alert information<br>- Citizen sightings and conservation anomalies can be displayed with map context | Python, FastAPI, MongoDB, Leaflet.js, Leaflet MarkerCluster, JavaScript | `GET /api/map/trees`<br>`GET /api/map/clusters`<br>`GET /api/map/heatmap`<br>`GET /api/citizen/sightings`<br>`GET /api/conservation/anomalies` | ____ |
| 7 | **AI-Assisted Tree Health Prediction** | - Manual health assessment is slow and inconsistent<br>- Weak or damaged trees may not be identified early<br>- No health score, issue list, or recommendation workflow | - Analyze uploaded tree images using Pillow and NumPy-based color and canopy metrics<br>- Generate a health score from 0 to 100<br>- Assign health grades from Excellent to Critical<br>- Identify possible visual issues<br>- Provide recommendations<br>- Store health check history and produce platform-wide health summaries | Python, FastAPI, Pillow, NumPy, MongoDB, image upload handling, JavaScript | `POST /api/health/{tree_id}/check`<br>`GET /api/health/{tree_id}/history`<br>`GET /api/health/summary` | ____ |
| 8 | **Real-Time Climate and Climate Scenario Monitoring** | - Current weather conditions are not available alongside tree records<br>- Researchers cannot compare tree locations with forecast conditions<br>- Possible temperature and rainfall changes are difficult to explore | - Retrieve current weather for a coordinate<br>- Display hourly weather information and a seven-day forecast<br>- Provide tree-specific climate views<br>- Simulate temperature and rainfall changes by region through the climate scenario page | Python, FastAPI, httpx, Open-Meteo API, MongoDB, JavaScript | `GET /api/climate/current`<br>`GET /api/climate/forecast`<br>`GET /api/climate/hourly`<br>`GET /api/climate/tree/{tree_id}`<br>`GET /api/climate/scenario`<br>`POST /api/climate/scenario` | ____ |
| 9 | **Satellite and Vegetation Health Monitoring** | - No vegetation health monitoring based on environmental satellite data<br>- No per-tree or regional vegetation summary<br>- NASA POWER measurements are difficult to compare visually | - Retrieve NASA POWER temperature, precipitation, and solar radiation data<br>- Calculate a vegetation health index proxy and status label<br>- Show regional vegetation summaries<br>- Provide per-tree analysis over a selected time window from 7 to 365 days<br>- Display VHI distribution, temperature versus precipitation, and solar radiation charts | Python, FastAPI, httpx, Pandas, NumPy, Chart.js, JavaScript | NASA POWER Daily Point API<br>`GET /api/satellite/vegetation/{tree_id}`<br>`GET /api/satellite/vegetation`<br>`GET /api/satellite/region-summary` | ____ |
| 10 | **Smart Search, Reports, and Research Export** | - Finding a particular tree in a large dataset is difficult<br>- Researchers need a consolidated view of statistics and locations<br>- Report preparation is repetitive and manual | - Fuzzy search across tree records<br>- Generate reports containing summary statistics, location breakdowns, and correlations<br>- Store report history<br>- Provide print-friendly report output for research documentation | Python, FastAPI, MongoDB, Pandas, NumPy, JavaScript, browser print support | `GET /api/reports/search`<br>`GET /api/reports/generate`<br>`GET /api/reports/history` | ____ |
| 11 | **Alerts and Conservation Anomaly Detection** | - No centralized alert system for unhealthy trees or unusual weather<br>- Conservation risks may remain unnoticed<br>- Manual review of environmental and tree observations is slow | - Generate weather alerts and health-based alerts<br>- Track Critical, Warning, and Info severity levels<br>- Resolve or delete alerts<br>- Detect low-health tree clusters, regional observation gaps, and critical conservation conditions<br>- Track conservation anomaly status as pending review, reviewed, or resolved | Python, FastAPI, MongoDB, Motor, Pydantic, JavaScript | `GET /api/alerts`<br>`GET /api/alerts/summary`<br>`POST /api/alerts/check-weather`<br>`POST /api/alerts/resolve/{alert_id}`<br>`DELETE /api/alerts/{alert_id}`<br>`GET /api/conservation/anomalies`<br>`POST /api/conservation/anomalies/check`<br>`PATCH /api/conservation/anomalies/{anomaly_id}/status` | ____ |
| 12 | **Soil Health and Tea Tree Suitability Prediction** | - Soil conditions are not available in the tree monitoring workflow<br>- Researchers cannot easily assess whether a location is suitable for tea tree growth<br>- Soil properties from external data sources may be unavailable or slow | - Retrieve pH, nitrogen, soil organic carbon, cation exchange capacity, clay, silt, and sand values<br>- Use the ISRIC SoilGrids API for real soil properties<br>- Use a deterministic spatial fallback model if the external service is unavailable<br>- Compare soil values with tea tree growth thresholds and display a soil health card and suitability prediction | Python, FastAPI, httpx, mathematical scoring, MongoDB, JavaScript | ISRIC SoilGrids API<br>`GET /api/soil/tree/{tree_id}`<br>`GET /api/soil/predict` | ____ |
| 13 | **Ecosystem Health and Regional Comparison** | - Platform data is focused on individual trees and does not provide enough regional context<br>- Researchers cannot compare regions consistently<br>- Overall ecosystem condition is difficult to summarize | - Calculate an ecosystem health overview from tree health, environmental conditions, alerts, and regional observations<br>- Provide region-level ecosystem health details<br>- List regions and compare selected regions using aggregated tree and health indicators<br>- Support cross-region research comparisons through the dedicated region comparison interface | Python, FastAPI, MongoDB, Pandas, NumPy, JavaScript | `GET /api/ecosystem/health`<br>`GET /api/ecosystem/health/{region_id}`<br>`GET /api/regions`<br>`GET /api/regions/compare`<br>`GET /api/regions/{region_id}/summary` | ____ |
| 14 | **Citizen Science and Community Data Collection** | - Researchers have limited access to observations from field visitors and local communities<br>- New sightings may not follow a consistent format<br>- Submitted observations need validation before being used as research data | - Accept GPS coordinates, location name, notes, optional tree measurements, and a photograph<br>- Validate coordinate ranges, note length, image type, and maximum image size<br>- Store submissions with pending, validated, or rejected status<br>- Allow reviewers to inspect and update sighting status | Python, FastAPI, MongoDB, Pydantic, multipart file upload, JavaScript | `POST /api/citizen/sightings`<br>`GET /api/citizen/sightings`<br>`GET /api/citizen/sightings/{sighting_id}`<br>`PATCH /api/citizen/sightings/{sighting_id}/status` | ____ |
| 15 | **Digital Tree Passport and Individual Tree Profile** | - Important information about one tree is spread across separate screens and collections<br>- Researchers need a consolidated identity record for field study and review<br>- Tree history, health, environment, climate, satellite, and alerts are difficult to view together | - Provide a digital passport view for an individual tree<br>- Display identity, location, measurements, environmental indicators, health information, and supporting observations<br>- Link the passport with tree detail, health checks, climate, satellite, and alert data<br>- Support tree routes such as `/trees/{tree_id}` and `/passport/{tree_id}` | HTML, CSS, JavaScript, FastAPI, MongoDB, ECharts/Chart.js where applicable | `GET /api/trees/{tree_id}`<br>`GET /api/environmental` and tree-specific records<br>`GET /api/health/{tree_id}/history`<br>`GET /api/climate/tree/{tree_id}`<br>`GET /api/satellite/vegetation/{tree_id}`<br>`GET /api/alerts/tree/{tree_id}` | ____ |

## Common Technology Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** MongoDB using Motor and PyMongo
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Visualization:** ECharts, Chart.js, Leaflet.js, Leaflet MarkerCluster
- **Data processing:** Pandas, NumPy, SciPy, Scikit-learn
- **Image analysis:** Pillow and NumPy
- **Authentication:** JWT using `python-jose`, password hashing with Passlib and bcrypt
- **File handling:** `python-multipart` and `aiofiles`
- **HTTP client:** httpx for external API requests
- **Configuration:** `.env` file using Pydantic Settings

## External API Services

The implemented project uses these external services:

- **Open-Meteo API:** Current weather, hourly data, forecasts, and climate scenario inputs
- **NASA POWER Daily Point API:** Temperature, precipitation, solar radiation, and vegetation health calculations
- **ISRIC SoilGrids API:** Soil pH, nitrogen, organic carbon, CEC, clay, silt, and sand data
- **Leaflet tile provider:** Map tiles displayed by the frontend

No Google Maps API, GBIF API, Google Earth Engine API, Polygon RPC, Twilio, SMTP, or APScheduler integration is included in the current implementation.

## Main User-Facing Pages

| Page | Purpose |
|---|---|
| `/` | Landing page |
| `/login` and `/register` | Authentication |
| `/dashboard` | Summary charts, health, ecosystem, anomalies, and alerts |
| `/trees` | Tree CRUD and filtering |
| `/tree/{id}` | Individual tree details and monitoring |
| `/passport/{id}` | Digital tree passport |
| `/map` | Interactive tree, sighting, and anomaly map |
| `/analytics` | Statistical analysis and charts |
| `/soil` | Soil health and suitability prediction |
| `/satellite` | Satellite and vegetation monitoring |
| `/reports` | Search and research report generation |
| `/alerts` | Alert and conservation anomaly management |
| `/citizen` | Citizen science tree sighting submission and review |
| `/climate-scenarios` | Climate scenario simulation |
| `/regions` | Cross-region comparison |
| `/upload` | CSV bulk upload |

## Module Completion Record

| Module | Development completed on | Guide signature |
|---|---|---|
| Frontend and User Interface | ____ | ____ |
| Backend Core Logic, Authentication, and API | ____ | ____ |
| Tree Data Management and Data Import | ____ | ____ |
| Environmental Data Management | ____ | ____ |
| Analytics and Statistical Processing | ____ | ____ |
| Geospatial Mapping and Spatial Visualization | ____ | ____ |
| AI-Assisted Tree Health Prediction | ____ | ____ |
| Real-Time Climate and Climate Scenario Monitoring | ____ | ____ |
| Satellite and Vegetation Health Monitoring | ____ | ____ |
| Smart Search, Reports, and Research Export | ____ | ____ |
| Alerts and Conservation Anomaly Detection | ____ | ____ |
| Soil Health and Tea Tree Suitability Prediction | ____ | ____ |
| Ecosystem Health and Regional Comparison | ____ | ____ |
| Citizen Science and Community Data Collection | ____ | ____ |
| Digital Tree Passport and Individual Tree Profile | ____ | ____ |
