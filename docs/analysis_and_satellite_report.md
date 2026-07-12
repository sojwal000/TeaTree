# Analysis Page and Satellite Page Report

## 1. Purpose

This report documents the implemented behavior of the Analytics page and the Satellite page in the Wild Tea Tree Big Data Visualization Platform. Both pages are part of the research and monitoring workflow, but they serve different roles:

- The Analytics page focuses on statistical exploration of tree data stored in MongoDB.
- The Satellite page focuses on vegetation and climate proxy monitoring using NASA POWER data.

Together, these pages support scientific interpretation, ecological comparison, and decision support for field researchers.

---

## 2. Analytics Page Overview

File: [frontend/analytics.html](../frontend/analytics.html)

The Analytics page is a multi-panel statistical workbench that lets the user run several analyses from the browser without leaving the page. It is authenticated, data-driven, and designed for interactive exploration of tree morphology and site conditions.

### 2.1 Page goals

The page is intended to answer questions such as:

- Which ecological variables are strongly related?
- Can tree diameter, height, or ring count be predicted from other measurements?
- Do tree groups differ significantly across locations?
- What does the distribution of a variable look like?
- How do estimated age and observed ring count compare?

### 2.2 Main UI sections

The page is divided into five functional cards:

1. Correlation Analysis
2. Regression Analysis
3. ANOVA Testing
4. Tree Age Estimation
5. Scatter Plot Matrix

Each section has its own controls, response container, and visualization area.

### 2.3 Correlation Analysis

This section accepts a comma-separated variable list, with a default value of:

- elevation
- diameter
- height
- ring_count

When the user clicks Run Analysis, the page calls:

- GET /api/analytics/correlation?variables=...

The backend returns:

- The validated variable list
- A Pearson correlation matrix
- Pairwise p-values
- Sample size used for the computation

The frontend renders the result in two ways:

- A heat-colored table showing numeric correlation values
- An ECharts heatmap for quick visual comparison

Significant pairings are marked when p < 0.05. The page uses color intensity to indicate whether values are strongly positive, weakly positive, weakly negative, or strongly negative.

### 2.4 Regression Analysis

This section lets the user choose:

- A target variable Y, such as diameter, height, or ring_count
- A feature list X, such as elevation,height

When executed, it calls:

- GET /api/analytics/regression?target=...&features=...

The backend builds a linear regression model and returns:

- Target field
- Feature fields
- Coefficients
- Intercept
- R-squared score
- Sample size
- Scatter data for plotting actual versus predicted values

The frontend presents:

- A prominent R-squared badge
- A coefficient summary panel
- An actual-vs-predicted scatter chart

This gives the user a quick sense of how well the selected features explain the target variable.

### 2.5 ANOVA Testing

This section provides a one-way analysis of variance comparison across groups. The default configuration compares a numeric variable across location_name.

The page calls:

- GET /api/analytics/anova?variable=...&group_by=...

The backend returns:

- F-statistic
- p-value
- Significance flag
- Number of groups
- Group summary statistics

The frontend displays the result in statistical cards and a grouped bar chart. The tooltip includes mean, standard deviation, count, and range per group.

This is useful when the user wants to determine whether one location or group differs meaningfully from others.

### 2.6 Tree Age Estimation

This section provides a simple model-based estimation of tree age using the observed diameter-to-ring_count relationship.

The page calls:

- GET /api/analytics/age-estimation

The backend returns:

- Model name
- R-squared score
- Coefficient
- Training sample size
- A set of estimated and actual points

The frontend shows:

- Model quality metrics
- A scatter plot of estimated versus actual ring count

This section is especially useful for quickly comparing modeled age proxies against trees with known ring counts.

### 2.7 Scatter Plot Matrix

This section accepts a comma-separated variable list and generates a grid of pairwise scatter plots.

The page calls:

- GET /api/analytics/scatter-matrix?variables=...

The backend provides sampled data points that can be reused to render each pairwise combination.

The frontend then builds a matrix where:

- Diagonal cells display the variable name
- Off-diagonal cells display scatter plots

This is the most exploratory view on the page and is useful for spotting patterns that are not obvious in one-dimensional summaries.

### 2.8 Visual and interaction behavior

The Analytics page uses:

- ECharts for heatmaps, scatter plots, bar charts, and matrix panels
- Custom card layouts and a control strip at the top of each section
- Loading placeholders during API calls
- Responsive behavior for smaller screens

The page also auto-runs the correlation analysis on load, so the user sees immediate output instead of an empty dashboard.

### 2.9 Backend dependency summary

The page depends on the Analytics route module:

File: [backend/routes/analytics_routes.py](../backend/routes/analytics_routes.py)

Important endpoints used by this page are:

- /api/analytics/correlation
- /api/analytics/regression
- /api/analytics/anova
- /api/analytics/age-estimation
- /api/analytics/scatter-matrix

The backend logic uses:

- pandas for tabular cleaning and transformation
- NumPy for numeric operations
- SciPy for Pearson correlation and ANOVA testing
- scikit-learn LinearRegression for regression modeling

### 2.10 Strengths

The Analytics page is strong because it combines multiple analytical modes in one place. It is useful for both quick inspection and more structured statistical comparison. The page also keeps the logic transparent by exposing sample sizes, coefficients, and significance indicators directly to the user.

### 2.11 Limitations

The page still has a few implementation limits:

- It assumes the relevant variables already exist in the tree dataset.
- Regression is linear only and does not support non-linear modeling.
- The scatter matrix can become visually dense when too many variables are requested.
- Statistical interpretation still depends on the user understanding the meaning of p-values and R-squared.

---

## 3. Satellite Page Overview

File: [frontend/satellite.html](../frontend/satellite.html)

The Satellite page is a vegetation monitoring interface built around NASA POWER data. It combines a regional summary of tree locations with per-tree vegetation analysis.

### 3.1 Page goals

The page is designed to answer questions such as:

- What is the vegetation health condition across tree-growing locations?
- Which locations show better or poorer climate support for tea trees?
- What are the recent temperature, precipitation, humidity, and solar radiation patterns for one tree?
- How does a selected tree compare across a chosen time period?

### 3.2 Main UI sections

The Satellite page has three major areas:

1. Regional Vegetation Summary
2. VHI Distribution chart
3. Per-Tree Vegetation Analysis

### 3.3 Regional Vegetation Summary

This top section loads automatically when the page opens.

It calls:

- GET /api/satellite/region-summary

The backend groups trees by location_name and computes climate proxy metrics using NASA POWER data for each location. The response contains a list of locations with values such as:

- tree count
- average temperature
- total precipitation over the period
- average solar radiation
- vegetation index
- vegetation status

The page renders the data in a table with columns for:

- Location
- Trees
- Avg Temp
- Precipitation
- VHI
- Status

A colored badge is used to display the vegetation category.

### 3.4 VHI Distribution chart

On the right side of the hero section, the page renders a bar chart that visualizes VHI values by location.

The chart uses:

- ECharts
- Location names on the X axis
- Vegetation Health Index on the Y axis
- Color coding based on status:
  - Excellent
  - Good
  - Moderate
  - Poor
  - Critical

This chart gives the user a quick regional comparison without needing to read the full table.

### 3.5 Per-Tree Vegetation Analysis

This is the most detailed part of the page.

The user selects:

- A tree from a dropdown list
- A number of days, between 7 and 365

The tree list is fetched from the tree API:

- GET /api/trees?limit=500

When the user clicks Analyze, the page calls:

- GET /api/satellite/vegetation/{tree_id}?days=...

The backend returns a daily series plus summary metrics derived from the selected tree’s coordinates and the NASA POWER dataset.

The page displays:

- VHI score
- Average temperature
- Total precipitation
- Average solar radiation
- Average humidity
- Vegetation status
- Start and end dates for the selected period

### 3.6 Per-tree charts

The page then renders two charts for the chosen period:

1. Temperature and precipitation chart
2. Solar radiation chart

The first chart uses a dual-axis layout so temperature and precipitation can be compared on the same timeline.
The second chart shows solar radiation as a smooth line chart with a light area fill.

These charts are useful for understanding how weather and radiation conditions changed across the selected window, not just what the final summary score was.

### 3.7 Backend dependency summary

The Satellite page depends on the Satellite route module:

File: [backend/routes/satellite_routes.py](../backend/routes/satellite_routes.py)

Important endpoints used by this page are:

- /api/satellite/region-summary
- /api/satellite/vegetation/{tree_id}
- /api/satellite/vegetation

The backend behavior includes:

- Querying MongoDB for tree coordinates
- Calling NASA POWER daily point data
- Filtering fill values such as -999
- Building daily records for the selected period
- Computing a proxy Vegetation Health Index
- Assigning a categorical status label based on the score

### 3.8 Vegetation Health Index logic

The implemented VHI is not a raw satellite NDVI value. It is a proxy index derived from climate parameters returned by NASA POWER.

The score combines three weighted components:

- Temperature suitability
- Precipitation suitability
- Solar radiation suitability

The page presents the result as a single vegetation health number and a status label. This makes the data easier to interpret for field users who need a quick health indicator rather than a raw climate dump.

### 3.9 Visual and interaction behavior

The Satellite page uses:

- Automatic loading on page open for the regional summary
- A tree selector for targeted lookup
- A numeric input for the time window
- Loading states while external data is being fetched
- Responsive grid layout for smaller screens

The interface is deliberately practical: summary first, then detail on demand.

### 3.10 Strengths

The Satellite page is useful because it bridges local tree records with external climate intelligence. It lets users compare locations, inspect an individual tree, and understand the recent environmental context around that tree.

### 3.11 Limitations

The main limitations are:

- The data depends on external NASA POWER availability.
- The vegetation score is a proxy, not a direct NDVI satellite product.
- Regional summaries are location-based and may not reflect fine-grained field variability.
- The page does not provide true image tiles or map overlays in its current form.

---

## 4. Comparison of the Two Pages

The Analytics page and the Satellite page serve different analytical layers:

- Analytics page: internal statistical analysis of stored tree data
- Satellite page: external climate-informed vegetation monitoring

A simple way to think about the relationship is:

- Analytics answers "what do our tree measurements say statistically?"
- Satellite answers "what does the environmental context say about tree conditions?"

Together they create a stronger interpretation pipeline than either page alone.

---

## 5. Overall Assessment

Both pages are well aligned with the goals of the platform. The Analytics page gives the project its statistical research capability, while the Satellite page adds environmental intelligence that can support ecological interpretation. In combination, they help researchers move from raw tree records to meaningful analytical and monitoring outputs.