# Wild Tea Tree Platform Mermaid Diagrams

This file contains multiple Mermaid diagrams for the Wild Tea Tree Big Data Visualization Platform.

## 1) High-Level System Architecture

```mermaid
flowchart LR
    U[User Browser]\nHTML CSS JS --> FE[Frontend Pages]
    FE --> API[FastAPI App main.py]

    subgraph Backend
        API --> AR[auth_routes]
        API --> TR[tree_routes]
        API --> ER[environmental_routes]
        API --> ANR[analytics_routes]
        API --> MR[map_routes]
        API --> HR[health_routes]
        API --> CR[climate_routes]
        API --> SR[satellite_routes]
        API --> RR[report_routes]
        API --> ALR[alert_routes]
    end

    AR --> DB[(MongoDB)]
    TR --> DB
    ER --> DB
    ANR --> DB
    MR --> DB
    HR --> DB
    RR --> DB
    ALR --> DB

    CR --> OM[Open-Meteo API]
    SR --> NP[NASA POWER API]
```

## 2) Backend Route Dependency Map

```mermaid
graph TD
    A[main.py] --> B[backend.config]
    A --> C[backend.database]
    A --> D[backend.models]
    A --> E[backend.auth]

    A --> R1[auth_routes]
    A --> R2[tree_routes]
    A --> R3[environmental_routes]
    A --> R4[analytics_routes]
    A --> R5[map_routes]
    A --> R6[health_routes]
    A --> R7[climate_routes]
    A --> R8[satellite_routes]
    A --> R9[report_routes]
    A --> R10[alert_routes]

    R1 --> D
    R1 --> E
    R1 --> C

    R2 --> D
    R2 --> C
    R2 --> E

    R3 --> D
    R3 --> C

    R4 --> C
    R5 --> C
    R6 --> C
    R7 --> C
    R8 --> C
    R9 --> C
    R10 --> C
```

## 3) Frontend Navigation / Page Relationship

```mermaid
flowchart TD
    IDX[/ index /] --> LOGIN[/ login /]
    IDX --> REG[/ register /]

    LOGIN --> DASH[/ dashboard /]
    REG --> DASH

    DASH --> TREES[/ trees /]
    DASH --> MAP[/ map /]
    DASH --> ANALYTICS[/ analytics /]
    DASH --> SAT[/ satellite /]
    DASH --> REPORTS[/ reports /]
    DASH --> ALERTS[/ alerts /]
    DASH --> UPLOAD[/ upload /]

    TREES --> DETAIL[/ tree/{id} /]
    TREES --> UPLOAD
    MAP --> DETAIL
    ALERTS --> DASH
    REPORTS --> DASH
```

## 4) Authentication Sequence

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant FE as Frontend
    participant API as FastAPI
    participant DB as MongoDB

    U->>FE: Submit login form
    FE->>API: POST /api/auth/login
    API->>DB: Validate user credentials
    DB-->>API: User record
    API-->>FE: JWT access token
    FE->>FE: Store token in localStorage
    FE->>API: GET /api/auth/profile (Bearer token)
    API-->>FE: User profile
    FE-->>U: Redirect to dashboard
```

## 5) Tree Data CRUD and CSV Upload Flow

```mermaid
flowchart LR
    User[Researcher] --> TBL[Trees Page]
    TBL -->|Create/Edit/Delete| API1[/api/trees]
    TBL -->|Filter/List| API2[/api/trees?filters]
    TBL -->|Open Detail| TD[Tree Detail Page]

    TD --> IMG[Upload Image]
    IMG --> API3[/api/trees/{id}/images]

    UP[Upload Page] --> CSV[Drop CSV file]
    CSV --> API4[/api/trees/upload-csv]

    API1 --> MDB[(MongoDB)]
    API2 --> MDB
    API3 --> UPF[(uploads/ folder)]
    API3 --> MDB
    API4 --> MDB
```

## 6) AI Health Prediction Flow

```mermaid
flowchart TD
    A[Tree Detail Page] --> B[Upload tree image for health check]
    B --> C[POST /api/health/{tree_id}/check]
    C --> D[Health analysis module\ncolor/canopy metrics]
    D --> E[Compute score and grade]
    E --> F[Detect issues and recommendations]
    F --> G[Store health result in MongoDB]
    G --> H[Return score + issues + actions]
    H --> I[Display health result and history]

    I --> J[GET /api/health/{tree_id}/history]
    J --> K[Timeline of previous checks]
```

## 7) Climate and Satellite Integration Flow

```mermaid
flowchart LR
    TD[Tree Detail Page] --> LATLON[Tree coordinates]

    LATLON --> CL[GET /api/climate/tree/{tree_id}]
    CL --> OM[Open-Meteo API]
    OM --> CL
    CL --> UI1[Current weather + 7 day forecast]

    LATLON --> SAT[GET /api/satellite/vegetation/{tree_id}]
    SAT --> NP[NASA POWER API]
    NP --> SAT
    SAT --> UI2[Vegetation Health Index + badges]
```

## 8) Alert Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Generated: Weather/Health rule triggered
    Generated --> Active: Saved as active alert
    Active --> Investigating: User reviews alert
    Investigating --> Resolved: POST /api/alerts/resolve/{alert_id}
    Active --> Deleted: DELETE /api/alerts/{alert_id}
    Resolved --> Archived: Included in history/summary
    Deleted --> [*]
    Archived --> [*]
```

## 9) Reporting and Search Workflow

```mermaid
flowchart TD
    R[Reports Page] --> S1[Search query + filters]
    S1 --> API1[GET /api/reports/search]
    API1 --> DB[(MongoDB)]
    DB --> API1
    API1 --> S2[Matching trees list]

    R --> G1[Generate report]
    G1 --> API2[GET /api/reports/generate]
    API2 --> DB
    API2 --> G2[Summary stats + location table + correlations]
    G2 --> G3[Render printable report]
    G3 --> G4[Browser print/export]
```

## 10) Mobile Responsive Behavior Map

```mermaid
flowchart TB
    A[Desktop >= 1024px] --> B[Multi-column dashboards]
    C[Tablet 768 to 1023px] --> D[Reduced columns + wrapped controls]
    E[Mobile < 768px] --> F[Single column sections]

    F --> G[Hamburger navigation]
    F --> H[Scrollable data tables]
    F --> I[Touch-friendly buttons]
    F --> J[Stacked filter panels]
```
