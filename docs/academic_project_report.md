# Abstract

The Wild Tea Tree Big Data Visualization Platform is a full-stack web system built to manage, analyze, and visualize ecological data related to wild tea trees. The implemented project combines a FastAPI backend, MongoDB data storage, and a multi-page frontend built with HTML, CSS, and JavaScript. The system supports end-to-end workflows including authenticated access, tree record management, environmental data logging, map-based exploration, statistical analytics, image-based health scoring, external climate and satellite data integration, report generation, and alert operations.

The implemented backend follows a modular route-based structure where each functional area is exposed through separate API groups. This separation improves maintainability and allows each functional domain to evolve independently while sharing a common authentication and database layer. The frontend provides dedicated pages for each operational function, and the application routes are served directly by the backend server, enabling a unified deployment model.

From a research and operational perspective, the platform solves common limitations of fragmented ecological tracking systems. Instead of separating field data, maps, analytics, and monitoring outputs into different tools, this platform centralizes all workflows around a consistent data model and shared identifiers such as tree_id and location_name. The result is a cohesive environment for researchers and technical users to inspect morphology, observe environmental conditions, run statistical analyses, evaluate health status from image content, and monitor risk via alert summaries.

The implemented analytics module provides multiple statistical outputs such as summary statistics, Pearson correlation with p-values, linear regression, one-way ANOVA, distribution statistics, age estimation based on diameter and ring count, and scatter matrix payload generation for visual interfaces. The health module applies a rule-based image analysis method using RGB-derived metrics to produce a health score, categorized status, issue hints, and recommendations. Climate and satellite routes integrate external data from Open-Meteo and NASA POWER, allowing the platform to supplement local records with broader environmental context.

The current system is production-structured at the code level but still contains roadmap features that are not implemented yet, including deep learning disease classification, offline-first operation, advanced notification channels, and some higher-level predictive analytics. Overall, the implemented version demonstrates a technically complete baseline for ecological data operations with practical extensibility for future research-grade enhancements.

# Abbreviations

- API: Application Programming Interface
- JWT: JSON Web Token
- CRUD: Create, Read, Update, Delete
- CSV: Comma-Separated Values
- CO2: Carbon Dioxide
- NDVI: Normalized Difference Vegetation Index
- VHI: Vegetation Health Index
- ANOVA: Analysis of Variance
- RGB: Red Green Blue
- HTTP: Hypertext Transfer Protocol
- CORS: Cross-Origin Resource Sharing
- JSON: JavaScript Object Notation
- UI: User Interface
- UX: User Experience

# Chapter 1: Introduction

## 1.1 Background

Monitoring wild tea tree ecosystems requires handling multiple forms of data: structural measurements such as height and trunk diameter, spatial coordinates, local environmental records, and periodic health observations. In many practical workflows, these data are collected through disconnected systems such as spreadsheets, local files, and independent mapping tools. This fragmentation creates delays in analysis, reduces consistency, and makes early risk detection difficult.

The project addresses this operational problem by building a unified web platform that integrates data management and ecological intelligence in a single environment. The implemented system supports authenticated usage, standardized storage in MongoDB, and multiple analysis modules that can be accessed through web pages. It is designed as a full-stack application where users can move from data entry to analytics and alert review without changing tools.

From a software engineering perspective, the implementation uses a modular backend where each domain capability is placed into dedicated route files. This keeps functionality organized while preserving a shared runtime context. The frontend is intentionally lightweight and framework-free, relying on plain JavaScript for API communication and rendering logic. This approach reduces build complexity and supports direct deployment through the FastAPI server.

## 1.2 Relevance

The project is relevant in both technical and domain-specific contexts.

Domain relevance:

- Wild tea tree monitoring is naturally multi-factor and geographically distributed.
- Decision-making improves when structural, environmental, health, and spatial data are analyzed together.
- Early warning for climate and health anomalies can reduce field response delays.

Technical relevance:

- Demonstrates a practical modular monolith architecture with clear route separation.
- Uses asynchronous database and HTTP handling suitable for data-heavy systems.
- Integrates scientific computing libraries into production-like API endpoints.
- Shows how lightweight image analytics and external data services can be combined in applied ecological software.

Academic relevance:

- Provides a complete case study for full-stack system design.
- Includes both operational modules and analytical modules in the same software product.
- Offers a clear base for future work in machine learning, forecasting, and ecological informatics.

## 1.3 Organization of the Report

This report is organized into nine chapters followed by future scope and sample code:

- Chapter 1 introduces context, motivation, and report flow.
- Chapter 2 discusses related conceptual work, terminology, current system background, and problem definition.
- Chapter 3 covers software and hardware requirements.
- Chapter 4 describes methodology, text-based project planning, and the proposed system concept.
- Chapter 5 provides text-only analytical interpretation of use case, class structure, activity flow, and sequence flow.
- Chapter 6 provides text-only design interpretation through data flow and execution logic.
- Chapter 7 explains the implemented architecture and module-level status.
- Chapter 8 analyzes observed outcomes based on implemented behaviors.
- Chapter 9 concludes the present system state and contributions.
- Future Scope lists currently unimplemented but identified expansion directions.
- Sample Code includes real excerpts from the existing project implementation.

# Chapter 2: Literature Survey

## 2.1 Related Work

Not implemented yet

The repository does not include formal citations, benchmark studies, or explicit comparative literature references. However, the implemented system aligns with common patterns seen in ecological information systems and applied environmental monitoring software:

- Centralized data services replacing fragmented field records.
- Geographic visualization layers combined with record-level metadata.
- Statistical analysis endpoints exposed through web APIs.
- Alert generation driven by rule-based threshold logic.
- Incremental use of image-derived indicators for health assessment.

Because no explicit references are maintained in the project content, this section cannot claim specific published methods or named systems.

## 2.2 Basic Terminologies

The following terminology is directly relevant to implemented modules:

- Tree record: A structured entity containing dimensions, location coordinates, elevation, optional ring count, and image paths.
- Environmental record: A timestamped measurement entry linked to a tree_id and containing temperature, humidity, wind speed, and CO2 level values.
- Health check record: Output generated from uploaded tree imagery, including computed metrics, health_score, health_status, and recommendation text.
- Weather alert: A generated risk notification based on threshold conditions from real-time weather data.
- Vegetation health index proxy: A computed indicator based on NASA POWER climate parameters in the satellite module.
- Correlation matrix: Pairwise Pearson relationships among numeric variables with significance p-values.
- Regression model: A linear mapping from selected feature variables to a target variable with coefficient and R-squared reporting.
- ANOVA: A one-way group comparison test to evaluate whether group means differ significantly.
- Scatter matrix data: Structured points enabling multi-variable pairwise plotting in the frontend.

## 2.3 Existing System

The implemented codebase itself can be treated as the existing system baseline. It already includes:

- Full authentication flow with registration, login, token verification, and profile retrieval/update.
- Tree management workflows including CRUD operations, filterable listing, count endpoint, CSV import, and image upload.
- Environmental module with create, list, summary, and delete operations.
- Analytics module exposing seven statistical endpoints.
- Map module exposing raw map points, clustered summaries, and heatmap intensity points.
- Health module performing image analysis and storing historical outputs.
- Climate module integrating Open-Meteo current, hourly, forecast, and per-tree queries.
- Satellite module integrating NASA POWER for per-tree and regional vegetation summaries.
- Report module supporting smart search, generated report payloads, and report history.
- Alert module supporting retrieval, summarization, weather/health checks, resolution, and deletion.

The frontend complements these backend services through dedicated pages and shared API utility logic.

## 2.4 Problem Statement

The core problem addressed by the project is the lack of an integrated operational and analytical environment for wild tea tree ecosystem monitoring.

Specific problem dimensions addressed in implementation:

- Data fragmentation: Field measurements, location data, and health observations are hard to manage when split across tools.
- Limited situational awareness: Without map and dashboard views, large collections of trees are difficult to interpret.
- Weak analytical integration: Statistical workflows are often external to data collection systems.
- Delayed risk response: Weather anomalies and deteriorating health signals require faster and centralized alerting.
- Inconsistent report generation: Manual synthesis across many data sources is slow and error-prone.

The implemented platform addresses these by unifying collection, analysis, map visualization, reporting, and alerting in one web application.

# Chapter 3: Requirement Gathering

## 3.1 Software Requirements

The software requirements can be directly extracted from the repository and startup instructions.

Core runtime software:

- Python 3.10 or higher.
- MongoDB instance reachable through the configured URL.
- Uvicorn ASGI server for local execution.
- Modern web browser for frontend pages.

Backend framework and runtime dependencies:

- fastapi
- uvicorn
- motor
- pymongo
- python-jose with cryptography
- passlib with bcrypt
- python-multipart
- pydantic with email support
- pydantic-settings
- python-dotenv
- aiofiles

Data science and analytics dependencies:

- pandas
- numpy
- scikit-learn
- scipy

Image and external API dependencies:

- Pillow
- httpx

Operational software conditions:

- Internet connectivity for Open-Meteo and NASA POWER calls.
- Writable uploads directory for image handling.
- Environment configuration through .env for deployment-specific settings.

## 3.2 Hardware Requirements

The project does not define strict hardware specifications such as processor model, RAM threshold, or disk quotas.

Not implemented yet

Logically derivable minimum capability for local execution:

- A machine capable of running Python, MongoDB, and a browser simultaneously.
- Sufficient memory and storage to hold MongoDB collections and uploaded images.
- Stable internet connection for climate and satellite API calls.

Because exact values are not provided in project content, no fixed hardware benchmark is asserted.

# Chapter 4: Plan of Project

## 4.1 Methodology

The implementation follows an incremental modular methodology where core data management is built first, followed by analytics and external intelligence modules.

Methodological characteristics visible in code structure:

- Modular route decomposition: Each capability family is isolated into a dedicated backend route file.
- Shared infrastructure layer: Authentication, database connection, and model validation are centralized.
- Progressive enrichment: Tree records are the anchor entities, then environmental, health, climate, and satellite intelligence are layered on top.
- API-first interaction: Frontend pages communicate only through REST endpoints, which enforces clear module boundaries.
- Rule-based inference first: Health and alert logic use transparent thresholds and formulae before introducing heavier machine learning complexity.

This methodology is suitable for academic and practical settings because it enables testable milestones and clear extension points.

## 4.2 Project Plan (TEXT ONLY, no Gantt)

A text representation of the implementation plan, derived from existing modules and roadmap structure, is as follows:

Phase 1: Core platform setup

- Initialize FastAPI application and static file serving.
- Configure MongoDB connection and collection indexes.
- Implement authentication primitives and protected-route dependency.

Phase 2: Core domain operations

- Implement tree CRUD, filtering, and count endpoints.
- Add environmental data storage and summary aggregation.
- Implement image upload for tree records.

Phase 3: Visualization and analytics capabilities

- Implement map payload generation for points, clusters, and heatmap.
- Implement analytics routes for summary, correlation, regression, ANOVA, distributions, age estimation, and scatter matrix.
- Build dashboard, tree list, and analytics frontend pages.

Phase 4: Intelligence and monitoring

- Add health image analysis and health history summaries.
- Integrate Open-Meteo climate endpoints.
- Integrate NASA POWER vegetation summary logic.
- Add alert creation, summarization, resolution, and deletion flows.

Phase 5: Reporting and usability refinement

- Implement smart search and report generation endpoints.
- Add report history tracking.
- Complete responsive layout behavior across pages.

Phase 6: Ongoing enhancement (roadmap)

- Deep learning disease classification.
- Offline support and advanced notification channels.
- Higher-level trend and predictive analytics.

## 4.3 Proposed System (TEXT ONLY)

The proposed system design that is now partially and largely implemented can be described as a centralized ecological intelligence platform built around the following principles:

- Every functional module should connect through unified tree identities.
- All important operations should be available through explicit APIs.
- Analytical and operational outputs should coexist in the same platform.
- Field data and external environmental context should be jointly visible.
- Alert generation should be automated where deterministic threshold logic is available.
- Frontend pages should remain task-focused rather than overloaded.

In practical terms, the proposed system acts as both a data management application and a decision-support application.

# Chapter 5: Project Analysis (TEXT ONLY)

## 5.1 Use Case Description

The implemented use cases can be analyzed textually by actor and intent.

Primary actor: Authenticated researcher or operator.

Use case 1: Account access

- User registers an account.
- User logs in and receives JWT token.
- User accesses protected operations.

Use case 2: Tree lifecycle management

- User creates tree records with structural and geographic attributes.
- User lists trees with filtering by location and numeric ranges.
- User updates and deletes selected tree records.
- User uploads images for visual documentation.

Use case 3: Environmental tracking

- User records environmental values linked to specific trees.
- User reviews environmental history and aggregate summaries.

Use case 4: Spatial exploration

- User opens map page and inspects tree coordinates.
- User applies location and elevation filters.
- User explores clustered and heatmap-like representations.

Use case 5: Statistical analysis

- User requests summary statistics and variable distributions.
- User runs correlation and regression analyses.
- User runs ANOVA grouped by location.
- User views scatter matrix payloads for visualization.

Use case 6: Health diagnostics from images

- User uploads tree image for health check.
- System returns score, status, issue hints, and recommendations.
- User reviews historical checks for the same tree.

Use case 7: Climate and satellite context

- User requests current and forecast weather by coordinates or by tree.
- User requests satellite-derived vegetation summaries.

Use case 8: Search and reporting

- User performs smart search using text or range-like input.
- User generates structured reports and reviews report history.

Use case 9: Alert operations

- User scans weather conditions across locations.
- System generates risk alerts and low-health alerts.
- User resolves or deletes alerts as needed.

## 5.2 Class Structure Explanation

The project uses Pydantic classes for request and response contracts. While not object-heavy in a domain-driven sense, the model classes form the core type system of the application.

Auth-related classes:

- UserRegister enforces name, email, and minimum password length.
- UserLogin captures login credentials.
- UserResponse defines returned user profile structure.
- Token and TokenData provide token contract and subject extraction shape.

Tree-related classes:

- TreeCreate enforces positive numeric dimensions and coordinate bounds.
- TreeUpdate supports partial updates by making fields optional.
- TreeResponse defines normalized tree payload returned by APIs.

Environmental classes:

- EnvironmentalDataCreate links metric capture to tree_id with bounded humidity and non-negative checks where applicable.
- EnvironmentalDataResponse defines output including timestamp.

Analytical and filtering classes:

- CorrelationResult, RegressionResult, and StatsSummary define analytical result shapes.
- TreeFilter represents possible filter combinations for list operations.

The route layer complements this class structure with helper functions and transformation logic. The result is a clear separation between input validation contracts and operational computation.

## 5.3 Activity Flow Explanation

A representative activity flow for typical usage is:

- Application starts and initializes database connection.
- User authenticates and stores token in local storage.
- User opens dashboard and triggers summary endpoints.
- User navigates to trees page and manages records.
- User optionally uploads CSV for bulk insertion.
- User uploads images and records environmental metrics.
- User opens analytics page to run statistical analysis.
- User inspects map, climate, and satellite views.
- User runs report generation and reviews output.
- User checks alerts and performs resolution actions.
- User logs out or session expires and login is required again.

This flow demonstrates a loop from data capture to analysis and decision action.

## 5.4 Sequence Flow Explanation

Textual sequence for protected operations:

- Frontend sends API request with Authorization Bearer token.
- FastAPI dependency extracts and validates JWT.
- User record is loaded from database using token subject.
- Route handler executes operation and accesses relevant collections.
- Response payload is returned to frontend for rendering.

Textual sequence for health check:

- Frontend submits tree_id and image file.
- Backend verifies tree existence and file constraints.
- Image is decoded and analyzed for color-based metrics.
- Health score and status are computed.
- Health record is persisted with image path and metadata.
- Frontend receives analysis payload and displays outputs.

Textual sequence for weather alert scan:

- Frontend triggers weather check endpoint.
- Backend aggregates unique locations from trees.
- Backend queries Open-Meteo per location.
- Rule engine evaluates thresholds and prepares alert objects.
- Health low-score checks run against latest health records.
- Duplicate active alerts are filtered out.
- New alerts are inserted and summary count is returned.

# Chapter 6: Project Design (TEXT ONLY)

## 6.1 Data Flow Explanation

### 6.1.1 Level 0

Level 0 text view of data movement:

- User-facing pages send requests to a single application server.
- The application server routes each request to a specific functional module.
- Functional modules interact with MongoDB collections for persistence and retrieval.
- Some modules call external weather and satellite APIs.
- Processed outputs return to frontend pages for visualization and interaction.

At this level, the system behaves as one integrated platform with shared authentication and database infrastructure.

### 6.1.2 Level 1

Level 1 text view by functional streams:

Authentication stream:

- Inputs: registration and login credentials.
- Processing: hash verification, token generation, token decoding.
- Storage: users collection.
- Outputs: user profile payload and access token.

Tree data stream:

- Inputs: tree forms, CSV files, image uploads.
- Processing: validation, conversion, filtering, file write operations.
- Storage: trees collection and uploads directory.
- Outputs: tree records and upload metadata.

Environmental stream:

- Inputs: per-tree climate metrics.
- Processing: tree existence check and timestamped insertion.
- Storage: environmental_data collection.
- Outputs: records and aggregate summary values.

Analytics stream:

- Inputs: variable selections and model parameters.
- Processing: dataframe construction, numerical cleaning, statistical computations.
- Storage: none mandatory beyond base tree data.
- Outputs: statistical result payloads for charts.

Health stream:

- Inputs: image uploads associated with tree_id.
- Processing: RGB metric extraction, weighted scoring, issue and recommendation generation.
- Storage: health_records collection and uploaded file path.
- Outputs: health score, status, metrics, and history.

Climate and satellite stream:

- Inputs: coordinates or tree_id.
- Processing: external API requests, normalization, derived index calculations.
- Storage: transient processing only in current implementation.
- Outputs: current conditions, forecasts, daily climate records, vegetation summary indicators.

Reporting and alert stream:

- Inputs: search text, report scope, alert trigger actions.
- Processing: multi-collection aggregation, risk rule evaluation, deduplication.
- Storage: reports and alerts collections.
- Outputs: report payloads, alert lists, and summary counts.

## 6.2 Flow Logic Explanation

The design logic follows a consistent pattern across modules:

- Validate input data early through typed models and query constraints.
- Resolve authentication context where operation is protected.
- Query MongoDB with explicit filtering and sorting logic.
- Apply deterministic transformations and computations.
- Return normalized JSON objects suitable for direct frontend use.

Specialized flow logic details:

- Analytics routes use in-memory DataFrame operations to simplify multi-step calculations.
- Health scoring prioritizes explainable rule-based formulas over opaque models.
- Alert generation intentionally separates weather-derived alerts and health-derived alerts before deduplication.
- Report generation composes multiple summaries in one payload while storing metadata separately.

This flow logic reduces coupling and keeps each API behavior explainable and auditable.

# Chapter 7: Implemented System

## 7.1 System Architecture

The implemented architecture is a modular monolithic web platform.

Server layer:

- One FastAPI application registers all route families.
- Startup and shutdown hooks manage MongoDB connectivity.
- Static frontend pages are served from the same server process.
- Upload files are served through a dedicated static mount.

Application layer:

- Authentication utility layer handles hashing and token logic.
- Route modules encapsulate domain operations by capability.
- Validation layer uses Pydantic models.
- Analytics and image-processing logic are implemented inside dedicated route modules.

Data layer:

- MongoDB stores operational and analytical history records.
- Collection indexes optimize common lookups.

Integration layer:

- Open-Meteo for weather data.
- NASA POWER for satellite-related agro-climate parameters.

Client layer:

- Multi-page frontend with shared API helper and navbar rendering.
- Individual pages for dashboard, trees, map, analytics, health-related tree details, reports, alerts, satellite, and upload.

## 7.2 Implementation Details

### Completed Modules

Based on route files, startup wiring, and frontend pages, the following are implemented:

- Authentication module with register, login, profile read, and profile update.
- JWT-based protected route handling.
- Tree management module with CRUD, count, filtering, search support, CSV import, and image upload.
- Environmental data module with create, list, summary, and delete.
- Analytics module with summary, correlation, regression, ANOVA, distribution, age estimation, and scatter matrix.
- Map module with point payload, grid-based cluster aggregation, and variable-based heatmap points.
- Health module with image upload, RGB-feature scoring, issue recommendation output, history retrieval, and summary statistics.
- Climate module with current, daily forecast, hourly forecast, and per-tree climate view.
- Satellite module with per-tree vegetation summary, coordinate-based lookup, and region summary.
- Reports module with fuzzy-like search, report generation, and report history.
- Alerts module with alert retrieval, summary aggregation, weather scan trigger, resolve, and delete actions.
- Frontend pages for all major modules listed in README and application routes.
- Shared frontend utility logic for token management, API calls, and navbar rendering.

### Modules In Progress

Based on explicit roadmap items in existing project documentation, the following are identified as in-progress or planned extensions:

- Deep learning disease classification using CNN.
- Multi-class disease taxonomy and large-batch image analysis.
- Rainfall versus growth correlation analytics.
- Climate trend forecasting across multi-year windows.
- Historical climate overlay integration into analytics.
- True satellite image tile overlays.
- Forest cover change analysis and seasonal tea growth cycle monitoring.
- Additional advanced filters such as year planted and health grade.
- Saved search presets.
- Offline web mode and offline data synchronization.
- Native mobile wrapper implementation.
- Push notification channels and user alert preferences.
- Scheduled periodic alert scans through background jobs.

### Not Implemented Yet

The repository does not currently provide the following as concrete implemented modules:

- Formal role-based access control beyond authenticated user checks.
- Automated test suite with unit or integration coverage committed in project files.
- Dedicated long-running scheduler service for periodic tasks.
- Documented production deployment manifests for container orchestration.
- Formal data retention and archival policies.

# Chapter 8: Result Analysis

The implemented system can be analyzed from functional completeness, analytical capability, and operational utility.

Functional completeness analysis:

- The application demonstrates broad module coverage from authentication to alerting.
- Backend route registration confirms all planned core modules are integrated in main startup.
- Frontend route serving confirms user-facing access paths are available for each major module.

Data management analysis:

- Tree CRUD and CSV import provide both granular and bulk ingestion paths.
- Environmental records are linked by tree_id, enabling per-tree and cross-tree summaries.
- Image handling supports practical documentation and health analysis inputs.

Analytical outcome analysis:

- Statistical endpoints support descriptive and inferential workflows.
- Regression and ANOVA outputs include quality or significance indicators.
- Scatter matrix and histogram payloads are structured for direct visualization.
- Age estimation provides a data-driven proxy where ring_count is partially available.

Intelligence module analysis:

- Health scoring is explainable and lightweight, suitable for rapid field screening.
- Climate integration provides real-time and forecast context that can support intervention planning.
- Satellite route provides an additional macro-environmental lens through derived vegetation indicators.

Operational monitoring analysis:

- Alert generation logic combines weather thresholds and health deterioration signals.
- Resolve and delete operations support lifecycle management.
- Summary endpoint provides quick severity and status distribution for dashboard display.

Usability analysis:

- Dedicated pages reduce cognitive load by separating tasks.
- Shared navbar and utility script help maintain interface consistency.
- Responsive behavior is listed and reflected in frontend organization.

Limitations impacting result interpretation:

- Health model is rule-based and not a learned classifier.
- External API availability can impact climate and satellite outputs.
- Long-term predictive modeling is not yet implemented.
- Formal quantitative evaluation metrics are not provided in the repository.

Overall result interpretation:

- The project succeeds as an integrated platform baseline.
- It provides actionable operational value in current form.
- It also establishes a technically sound foundation for advanced research enhancements.

# Chapter 9: Conclusion

The Wild Tea Tree Big Data Visualization Platform, as implemented in the current repository, is a comprehensive and modular ecological information system. It goes beyond simple record keeping by integrating management, statistical analytics, map-based exploration, image-based health interpretation, and alert workflows into one deployable web application.

The backend architecture is clear and scalable at module level. The frontend is practical and task-oriented. Data flow design supports both day-to-day operational needs and analytical exploration. The use of free external data services and explainable rule-based logic makes the system accessible for real deployment without immediate dependence on costly infrastructure.

From an academic and engineering perspective, the project demonstrates strong end-to-end implementation maturity. While some advanced roadmap features are pending, the existing modules already provide a substantial foundation for ecological monitoring and data-informed decision support.

# Future Scope

Future expansion directions that are explicitly present in project roadmap and documentation include:

- CNN-based image disease classification replacing or complementing rule-based scoring.
- Multi-class disease taxonomy and large-batch image processing.
- Long-horizon climate trend forecasting and causal growth analysis.
- Satellite image tile overlays and forest cover change monitoring.
- Additional smart filters and saved search presets.
- Offline-first operation with synchronization for intermittent-connectivity field work.
- Native mobile wrapping for field usability.
- Push notifications and per-user alert subscription controls.
- Scheduled periodic alert scanning through background scheduling.
- Stronger access control granularity and auditing for multi-user environments.

# Sample Code

The project contains implemented source code. Selected examples are included below.

Example 1: JWT token creation logic from authentication utility

    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

Example 2: Tree creation endpoint logic

    @router.post("", response_model=TreeResponse, status_code=status.HTTP_201_CREATED)
    async def create_tree(tree: TreeCreate, current_user: dict = Depends(get_current_user)):
        db = get_database()
        now = datetime.utcnow()
        tree_doc = {
            "tree_id": str(uuid.uuid4()),
            **tree.model_dump(),
            "created_by": current_user["user_id"],
            "created_at": now,
            "updated_at": now,
        }
        await db.trees.insert_one(tree_doc)
        return TreeResponse(**tree_doc)

Example 3: Correlation endpoint response construction

    return {
        "variables": available,
        "correlation_matrix": {
            col: {row: round(corr_matrix.loc[row, col], 4) for row in available}
            for col in available
        },
        "p_values": p_values,
        "sample_size": len(subset),
    }

Example 4: Weather alert threshold rule snippet

    if temp is not None:
        if temp > 38:
            new_alerts.append(_create_alert(
                "Extreme Heat", "critical", "weather",
                f"Temperature at {loc['_id']} is {temp}°C — dangerous heat stress for tea trees",
                loc["_id"], loc["tree_count"],
            ))

Example 5: Health score clamping logic

    score = max(0, min(100, score))

