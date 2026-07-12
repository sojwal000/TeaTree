

## Abstract

Wild tea tree monitoring requires the coordinated management of morphology, environmental conditions, geographic location, health observations, and scientific analysis outputs. In practice, these data are often distributed across spreadsheets, maps, image folders, manual reports, and isolated analytics tools, making it difficult to maintain a coherent research workflow. This paper presents the design and implementation of the Wild Tea Tree Big Data Visualization Platform, a full-stack ecological intelligence system built with FastAPI, MongoDB, and a lightweight HTML/JavaScript frontend. The platform integrates authenticated tree record management, environmental logging, geospatial visualization, statistical analytics, image-based health analysis, climate intelligence, satellite-derived vegetation monitoring, report generation, and automated alerts into a single operational environment.

The system is structured as a modular monolith in which each major capability is exposed through a dedicated backend route family and rendered through a specialized frontend page. This architecture improves maintainability while preserving a unified data model centered on tree identifiers and location metadata. The analytics layer provides correlation analysis, linear regression, one-way ANOVA, distribution summaries, age estimation, and scatter-matrix payload generation. The health monitoring layer applies transparent image feature extraction to produce score-based tree health assessments, while the climate and satellite layers enrich local observations using Open-Meteo and NASA POWER data services. A dashboard and reporting workflow allow users to interpret trends, compare locations, and generate research-ready summaries.

Because the implementation is a software system paper rather than a controlled field experiment, the evaluation emphasized functionality, integration quality, and operational completeness instead of benchmark comparison against external datasets. The result is a practical, extensible platform that demonstrates how ecological monitoring, scientific analytics, and web-based decision support can be unified in a compact and reproducible architecture.

**Index Terms**: ecological informatics, tea tree monitoring, FastAPI, MongoDB, geospatial visualization, statistical analytics, satellite monitoring, environmental intelligence, health prediction, web application.

---

## I. Introduction

Wild tea trees are valuable ecological and agricultural assets whose monitoring requires more than static record keeping. Researchers and field teams must track spatial location, physical measurements, environmental context, canopy condition, and response to weather and seasonal changes. In many real deployments, these observations are distributed across disconnected tools that do not share a common data model. The result is data fragmentation, duplicated entry, slower analysis, and weaker situational awareness.

The Wild Tea Tree Big Data Visualization Platform addresses this challenge by centralizing the operational workflow in a single web application. The platform is designed to support day-to-day research activities such as registering trees, recording measurements, logging environmental variables, reviewing map-based distributions, analyzing statistical relationships, and producing reports for scientific communication. Instead of treating collection, analysis, and visualization as separate tasks, the system links them through a shared backend and a consistent frontend experience.

This paper describes the implemented system as an engineering artifact. It focuses on the architecture, data flow, analysis modules, external API integration, and practical value of the software. The emphasis is not on proposing a new theoretical algorithm, but on presenting a complete and coherent platform for ecological data operations that can support research, field inspection, and future machine learning expansion.

### A. Objectives

The project was developed with the following objectives:

1. Create a secure web-based platform for tree record management and authenticated access.
2. Support structured storage of tree, environmental, alert, and report data in MongoDB.
3. Provide interactive geospatial and statistical visualization tools for ecological interpretation.
4. Integrate image-based health scoring and external climate and satellite intelligence.
5. Generate professional research reports and operational summaries from stored data.
6. Deliver a responsive interface suitable for both desktop and mobile field use.

### B. Contributions

The main contributions of the implemented platform are:

1. A modular FastAPI backend that separates authentication, tree management, analytics, map services, climate intelligence, satellite monitoring, reports, and alerts into distinct route groups.
2. A practical ecological data model that links each record family through shared tree identifiers and location metadata.
3. A lightweight frontend architecture that avoids build complexity while still delivering rich dashboards, maps, charts, and workflows.
4. A combined analytical stack that includes Pearson correlation, linear regression, ANOVA, distribution analysis, and age estimation.
5. External data enrichment through Open-Meteo and NASA POWER, enabling contextual weather and vegetation insight.

---

## II. Related Work and Problem Context

Ecological monitoring systems typically fall into one of three categories: data entry tools, visualization tools, or analytics tools. Data entry tools are useful for field capture but often provide weak analysis. Visualization tools may display maps or charts but lack persistent operational records. Analytics tools can be powerful but often require exporting data into separate environments. The central problem is integration.

The present platform is informed by common patterns in environmental information systems, geographic dashboards, and applied scientific web applications. Rather than splitting features across multiple products, the system consolidates them into one application layer so that users can move from collection to analysis without leaving the platform. This design is especially useful for tree-based ecological studies where the same entity must be reviewed from multiple perspectives: morphology, geography, climate, image condition, and historical trend.

The project also reflects the practical realities of applied research software. Many ecological systems rely on lightweight, explainable logic instead of opaque models because users need to understand why a tree is flagged, why a region is highlighted, or why a health grade changes. For that reason, the implementation favors transparent statistical methods and rule-based decision logic before introducing heavier learning-based approaches.

### A. Problem Statement

The primary problem addressed by the platform is the lack of a unified environment for wild tea tree monitoring. Specific pain points include:

1. Fragmented data storage across spreadsheets, photos, maps, and manual notes.
2. Limited ability to compare location-level patterns across a large tree population.
3. Difficulty generating repeatable statistical summaries and research reports.
4. Weak early-warning capability for health decline and unusual weather conditions.
5. A mismatch between field collection workflows and analytical workflows.

### B. Design Response

The platform responds to these issues through three design choices. First, it uses a shared entity model so that every major feature can reference the same tree identity. Second, it exposes each function through a dedicated API family so the frontend can remain organized. Third, it integrates external climate and satellite services to extend the local dataset with broader environmental context.

---

## III. System Architecture

The platform follows a modular monolith architecture. This means the backend is deployed as a single FastAPI application, but the code is organized into feature-specific modules that behave like bounded services. The frontend consists of multiple static pages that communicate with the backend through REST endpoints.

### A. High-Level Structure

The implementation consists of four major layers:

1. Presentation layer: HTML pages, CSS styles, and browser-side JavaScript.
2. Application layer: FastAPI routes for authentication, tree records, environmental data, analytics, maps, health, climate, satellite, reports, and alerts.
3. Data layer: MongoDB collections for persistent storage.
4. Integration layer: Open-Meteo and NASA POWER APIs for external climate and vegetation intelligence.

### B. Backend Organization

The backend is split into dedicated route modules under backend/routes. This structure allows the system to evolve without turning the main application file into a monolithic controller. Each route module owns a specific domain:

1. Authentication and user profile management.
2. Tree CRUD, bulk upload, filtering, and image upload.
3. Environmental record storage and summarization.
4. Statistical analytics and modeling endpoints.
5. Map point, cluster, and heatmap generation.
6. Image-based tree health assessment.
7. Climate retrieval from Open-Meteo.
8. Vegetation and satellite proxy analysis.
9. Search and report generation.
10. Alert creation, resolution, and summary logic.

### C. Frontend Organization

The frontend uses a page-per-feature structure. This keeps the user experience direct and reduces the cognitive load of a single overloaded dashboard. Separate pages exist for login, registration, dashboard, tree management, tree detail inspection, map exploration, analytics, satellite monitoring, reports, alerts, and uploads. Shared assets are centralized in styles.css and app.js.

### D. Data Flow

The end-to-end flow is straightforward:

1. A user signs in and receives a JWT token.
2. The browser stores and reuses the token for protected requests.
3. Frontend pages fetch data from feature-specific API endpoints.
4. The backend validates input and reads or writes MongoDB documents.
5. Analytics modules compute derived values on demand.
6. External APIs enrich the response where needed.
7. The frontend renders tables, charts, maps, and summaries.

This architecture is effective because it keeps the UI thin while concentrating business logic in the backend.

---

## IV. Data Model

The data model is centered on the tree entity. Additional collections record operational and analytical information linked to the same underlying subject.

### A. Core Entities

1. Users: authentication records with email, password hash, name, and timestamps.
2. Trees: morphological and spatial records including height, diameter, ring count, elevation, latitude, longitude, and location name.
3. Environmental records: time-stamped measurements such as temperature, humidity, wind speed, and carbon dioxide level.
4. Health records: image-derived outputs including health score, status, detected issues, recommendations, and supporting metrics.
5. Alerts: risk and anomaly notifications with severity, status, type, and resolution metadata.
6. Reports: generated summaries and historical report outputs.

### B. Data Modeling Principles

The data model emphasizes consistency and traceability. Tree identifiers provide the anchor for record linkage, while location metadata enables aggregation across sites. This design supports both micro-level inspection of a single tree and macro-level analysis across locations or regions.

### C. Operational Benefits

The schema layout provides several advantages:

1. It supports independent growth of each module without breaking common references.
2. It enables historical analysis because records are time stamped.
3. It simplifies reporting because each module can query by tree_id or location_name.
4. It supports alert generation and follow-up actions through explicit status fields.

---

## V. Implementation Methodology

The implementation follows a progressive enrichment strategy. Core data management is implemented first, then contextual and analytical layers are added on top.

### A. Authentication and Access Control

The platform uses JWT-based authentication to protect private routes. Passwords are hashed using a secure password hashing library, and protected API endpoints verify the token before returning data. This allows researchers to use the platform in a multi-user environment while preserving access control.

### B. Tree Data Management

Tree management is the operational center of the platform. Users can create, edit, view, delete, filter, and bulk import tree records. Image uploads support richer inspection and downstream health analysis. By keeping tree records standardized, the system ensures the analytics and monitoring modules can operate on clean, consistent data.

### C. Environmental Monitoring

Environmental observations are stored as separate records linked to a tree. This enables repeated measurements over time without duplicating the tree entry. The environmental module also supports summary statistics, helping users inspect trends in temperature, humidity, wind speed, and CO2 levels.

### D. Analytics Module

The analytics layer exposes several statistical endpoints:

1. Summary statistics for major tree variables.
2. Pearson correlation analysis with significance information.
3. Linear regression for predictive relationships.
4. One-way ANOVA for group comparison.
5. Distribution outputs for variable inspection.
6. Age estimation based on observed tree features.
7. Scatter-matrix payload generation for exploratory visualization.

The design goal is not to replace a statistical package, but to make core scientific operations directly accessible in the browser.

### E. Health Prediction Logic

The health module performs image-based assessment using transparent feature extraction. The system derives color and canopy-related metrics from uploaded images and converts them into a health score and a qualitative health grade. It also returns issue hints and recommendations. The method is intentionally explainable, making it easier for users to understand the basis of each result.

### F. Climate and Satellite Intelligence

The climate module queries Open-Meteo for current conditions and forecasts. The satellite module queries NASA POWER for vegetation-related proxies and atmospheric variables. Together, these modules provide external context that complements local observations, especially when assessing stress conditions or comparing regions.

### G. Reporting and Search

The report module supports fuzzy search and research report generation. This is particularly valuable when a user needs to synthesize information from multiple records into a publishable or printable summary. Search helps users locate records even when partial or inconsistent naming is present.

### H. Alerts and Notifications

Alerts are generated from weather or health conditions and stored with severity labels and status fields. The alert system supports review, resolution, dismissal, and summary display. This converts raw monitoring signals into actionable operational information.

---

## VI. User Interface and Visualization Strategy

The frontend is intentionally lightweight but feature-rich. Instead of relying on a heavy client framework, the system uses plain HTML, CSS, and JavaScript. This reduces deployment overhead and keeps the user interface close to the API design.

### A. Dashboard Experience

The dashboard consolidates key metrics and visual summaries. It is designed to give users a fast overview of the state of the dataset, including tree distributions, health indicators, and alert counts.

### B. Map Experience

The map page uses Leaflet-based visualization to present tree locations, clustered markers, and spatial filtering behavior. This is important for field researchers because location patterns are often easier to understand spatially than in tabular form.

### C. Analytics Experience

The analytics page is a statistical workbench. It presents charts, summaries, and comparison views that help users move from raw records to scientific interpretation. The interface supports iterative investigation rather than forcing a linear report flow.

### D. Mobile Responsiveness

The interface includes mobile-friendly layouts, responsive cards, scrollable tables, and compact navigation behavior. This matters because ecological work is often performed in the field using phones or tablets.

---

## VII. External API Integration

The platform enriches local records with external data from two services.

### A. Open-Meteo

Open-Meteo provides current weather, hourly data, and multi-day forecasts without requiring an API key. The system uses this service to contextualize tree locations with temperature, humidity, rain, and wind information. This is useful for identifying short-term environmental stress.

### B. NASA POWER

NASA POWER provides climate and radiation variables that can be used as proxies for vegetation and environmental conditions. The platform uses these data to calculate vegetation-health-style summaries and regional comparisons.

### C. Integration Benefits

External APIs extend the value of the platform in three ways:

1. They add operational context without requiring manual data entry.
2. They help compare local observations against broader climate conditions.
3. They improve alerting and reporting by adding richer environmental signals.

---

## VIII. Analytical and Decision Support Methods

The analytical modules transform stored data into interpretive outputs that support research questions.

### A. Correlation Analysis

Correlation analysis helps identify variables that vary together, such as relationships among elevation, diameter, height, and ring count. The result is useful for forming hypotheses about ecological growth conditions.

### B. Regression Analysis

Regression is used to estimate linear relationships between selected variables. The implementation returns coefficients, intercepts, and $R^2$ values, giving users a clear sense of model fit. This is helpful for quick exploratory prediction, especially when comparing physical tree characteristics.

### C. ANOVA Testing

ANOVA supports group comparison across locations or other categorical groupings. This is especially relevant when researchers want to determine whether differences between regions are statistically meaningful.

### D. Age Estimation

The age estimation module offers an interpretable proxy model based on available tree features. While not a substitute for dendrochronological measurement, it provides a practical comparative estimate for operational use.

### E. Decision Support Value

These methods are valuable because they are transparent, computationally lightweight, and directly usable in a browser workflow. They support interpretation without requiring the user to export data to an external statistics environment.

---

## IX. Evaluation and Discussion

Because this work is a software implementation paper, the evaluation emphasis is on functional completeness and architecture quality rather than on a controlled benchmark study. The platform demonstrates the following strengths:

1. Strong modular separation of concerns.
2. Unified handling of data, analytics, and visualization.
3. Clear support for both operational and research workflows.
4. Effective enrichment of local data with climate and vegetation proxies.
5. Explainable analytical and health scoring outputs.

From a practical standpoint, the system reduces the need to move between multiple tools. A user can register a tree, inspect its location, review its environmental history, run analytics, inspect a health score, and generate a report in one environment. This lowers workflow friction and improves consistency.

There are also important limitations. The health prediction method is rule-based rather than deep learning based, which means it is interpretable but not as powerful as a trained vision model. The analytics module is focused on classical statistical methods and does not yet include more advanced forecasting or non-linear modeling. External data quality also depends on the availability and fidelity of third-party APIs.

Nevertheless, the platform is already valuable as a research-support system because it demonstrates a full stack integration pattern that is practical, maintainable, and expandable.

---

## X. Limitations and Future Work

The current implementation establishes a strong baseline but leaves room for future improvement.

### A. Current Limitations

1. Health analysis is based on transparent feature rules rather than deep learning classification.
2. Climate and vegetation insights depend on third-party API availability.
3. Predictive analytics are largely linear and exploratory.
4. No offline-first synchronization is implemented.
5. Advanced notifications such as push or email alerts are not yet fully implemented.

### B. Future Research Directions

1. Train a CNN-based disease and stress classifier using labeled tea tree imagery.
2. Add time-series climate trend forecasting for longer-range ecological monitoring.
3. Introduce offline data entry and sync for field operation resilience.
4. Expand report generation into publication-ready exports with richer formatting.
5. Incorporate spatial clustering and anomaly detection at the landscape level.
6. Add subscription-based alert delivery through email or browser push notifications.

These directions would move the platform from a capable operational system toward a more advanced ecological decision-support environment.

---

## XI. Conclusion

This paper presented the Wild Tea Tree Big Data Visualization Platform as a complete web-based ecological intelligence system for monitoring, analysis, and reporting. The implemented platform integrates authentication, tree data management, environmental records, statistical analytics, image-based health assessment, climate intelligence, satellite-derived proxies, search, reporting, and alerts into a single coherent workflow. Its modular FastAPI backend, MongoDB persistence layer, and responsive frontend together form a maintainable and extensible architecture.

The main significance of the system is not merely that it stores data, but that it turns tree monitoring into an integrated research workflow. Users can move from collection to interpretation without changing tools, which improves consistency and lowers operational friction. The platform therefore serves as a practical foundation for ecological informatics, field inspection, and future machine learning-based expansion.

---

## References

[1] FastAPI Documentation. Available: https://fastapi.tiangolo.com/

[2] MongoDB Manual. Available: https://www.mongodb.com/docs/

[3] Motor Async Python Driver Documentation. Available: https://motor.readthedocs.io/

[4] Open-Meteo API Documentation. Available: https://open-meteo.com/

[5] NASA POWER Project Documentation. Available: https://power.larc.nasa.gov/

[6] SciPy Documentation. Available: https://docs.scipy.org/

[7] scikit-learn Documentation. Available: https://scikit-learn.org/

[8] Leaflet Documentation. Available: https://leafletjs.com/

[9] Chart.js Documentation. Available: https://www.chartjs.org/

[10] Apache ECharts Documentation. Available: https://echarts.apache.org/

---
