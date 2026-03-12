"""
Data analytics routes: correlation, regression, ANOVA, statistics
"""
import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from sklearn.linear_model import LinearRegression
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.database import get_database

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


async def _get_tree_dataframe(filters: dict = None) -> pd.DataFrame:
    """Helper: fetch tree data from DB and return as DataFrame."""
    db = get_database()
    query = filters or {}
    cursor = db.trees.find(query)
    trees = await cursor.to_list(length=10000)
    if not trees:
        raise HTTPException(status_code=404, detail="No tree data available for analysis")
    df = pd.DataFrame(trees)
    numeric_cols = ["height", "diameter", "ring_count", "elevation", "latitude", "longitude"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@router.get("/summary")
async def get_statistics_summary():
    """Get overall statistical summary of tree data."""
    db = get_database()
    df = await _get_tree_dataframe()

    # Location counts
    location_counts = df["location_name"].value_counts().to_dict()

    summary = {
        "total_trees": len(df),
        "avg_height": round(df["height"].mean(), 2) if "height" in df else 0,
        "avg_diameter": round(df["diameter"].mean(), 2) if "diameter" in df else 0,
        "avg_elevation": round(df["elevation"].mean(), 2) if "elevation" in df else 0,
        "elevation_range": {
            "min": round(float(df["elevation"].min()), 2),
            "max": round(float(df["elevation"].max()), 2),
        },
        "diameter_range": {
            "min": round(float(df["diameter"].min()), 2),
            "max": round(float(df["diameter"].max()), 2),
        },
        "height_range": {
            "min": round(float(df["height"].min()), 2),
            "max": round(float(df["height"].max()), 2),
        },
        "location_counts": location_counts,
    }

    if "ring_count" in df and df["ring_count"].notna().any():
        summary["avg_ring_count"] = round(df["ring_count"].mean(), 2)
        summary["ring_count_range"] = {
            "min": int(df["ring_count"].min()),
            "max": int(df["ring_count"].max()),
        }

    return summary


@router.get("/correlation")
async def get_correlation(
    variables: str = Query(
        "elevation,diameter,height,ring_count",
        description="Comma-separated list of variables to correlate",
    )
):
    """Run correlation analysis between ecological variables."""
    df = await _get_tree_dataframe()
    var_list = [v.strip() for v in variables.split(",")]

    # Validate requested columns exist
    available = [v for v in var_list if v in df.columns]
    if len(available) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 valid numeric columns")

    subset = df[available].dropna()
    if len(subset) < 3:
        raise HTTPException(status_code=400, detail="Not enough data points for correlation")

    # Pearson correlation matrix
    corr_matrix = subset.corr(method="pearson")

    # P-values
    p_values = {}
    for col1 in available:
        p_values[col1] = {}
        for col2 in available:
            if col1 == col2:
                p_values[col1][col2] = 0.0
            else:
                valid = subset[[col1, col2]].dropna()
                if len(valid) >= 3:
                    _, p = scipy_stats.pearsonr(valid[col1], valid[col2])
                    p_values[col1][col2] = round(p, 6)
                else:
                    p_values[col1][col2] = None

    return {
        "variables": available,
        "correlation_matrix": {
            col: {row: round(corr_matrix.loc[row, col], 4) for row in available}
            for col in available
        },
        "p_values": p_values,
        "sample_size": len(subset),
    }


@router.get("/regression")
async def get_regression(
    target: str = Query("diameter", description="Target variable (y)"),
    features: str = Query("elevation,height", description="Comma-separated feature variables (x)"),
):
    """Run linear regression analysis."""
    df = await _get_tree_dataframe()
    feature_list = [f.strip() for f in features.split(",")]

    all_cols = feature_list + [target]
    available = [c for c in all_cols if c in df.columns]
    if target not in available:
        raise HTTPException(status_code=400, detail=f"Target '{target}' not found in data")

    subset = df[available].dropna()
    if len(subset) < 5:
        raise HTTPException(status_code=400, detail="Not enough data for regression")

    valid_features = [f for f in feature_list if f in subset.columns and f != target]
    if not valid_features:
        raise HTTPException(status_code=400, detail="No valid feature variables")

    X = subset[valid_features].values
    y = subset[target].values

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    r_squared = model.score(X, y)

    coefficients = {feat: round(coef, 6) for feat, coef in zip(valid_features, model.coef_)}
    coefficients["intercept"] = round(model.intercept_, 6)

    # Build scatter data for visualization
    scatter_data = []
    for i in range(min(len(subset), 500)):
        point = {target: round(float(y[i]), 3), "predicted": round(float(y_pred[i]), 3)}
        for j, feat in enumerate(valid_features):
            point[feat] = round(float(X[i][j]), 3)
        scatter_data.append(point)

    return {
        "model_type": "linear_regression",
        "target": target,
        "features": valid_features,
        "coefficients": coefficients,
        "r_squared": round(r_squared, 4),
        "sample_size": len(subset),
        "scatter_data": scatter_data,
    }


@router.get("/anova")
async def run_anova(
    variable: str = Query("diameter", description="Numeric variable to compare"),
    group_by: str = Query("location_name", description="Categorical grouping variable"),
):
    """Run one-way ANOVA to compare a variable across groups."""
    df = await _get_tree_dataframe()

    if variable not in df.columns or group_by not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid variable or group column")

    groups = df.groupby(group_by)[variable].apply(list).to_dict()
    group_data = {k: [x for x in v if pd.notna(x)] for k, v in groups.items()}
    group_data = {k: v for k, v in group_data.items() if len(v) >= 2}

    if len(group_data) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 groups with sufficient data")

    group_arrays = list(group_data.values())
    f_stat, p_value = scipy_stats.f_oneway(*group_arrays)

    # Group summaries
    group_summaries = {}
    for name, values in group_data.items():
        arr = np.array(values)
        group_summaries[name] = {
            "count": len(arr),
            "mean": round(float(arr.mean()), 3),
            "std": round(float(arr.std()), 3),
            "min": round(float(arr.min()), 3),
            "max": round(float(arr.max()), 3),
        }

    return {
        "variable": variable,
        "group_by": group_by,
        "f_statistic": round(float(f_stat), 4),
        "p_value": round(float(p_value), 6),
        "significant": p_value < 0.05,
        "group_count": len(group_data),
        "group_summaries": group_summaries,
    }


@router.get("/distribution")
async def get_distribution(
    variable: str = Query("diameter", description="Variable to analyze"),
    bins: int = Query(20, ge=5, le=100),
):
    """Get distribution data (histogram) for a numeric variable."""
    df = await _get_tree_dataframe()

    if variable not in df.columns:
        raise HTTPException(status_code=400, detail=f"Variable '{variable}' not found")

    values = df[variable].dropna().astype(float)
    if len(values) == 0:
        raise HTTPException(status_code=400, detail="No data for this variable")

    counts, bin_edges = np.histogram(values, bins=bins)

    histogram = []
    for i in range(len(counts)):
        histogram.append({
            "bin_start": round(float(bin_edges[i]), 2),
            "bin_end": round(float(bin_edges[i + 1]), 2),
            "count": int(counts[i]),
        })

    return {
        "variable": variable,
        "total_count": len(values),
        "mean": round(float(values.mean()), 3),
        "median": round(float(values.median()), 3),
        "std": round(float(values.std()), 3),
        "skewness": round(float(values.skew()), 3),
        "kurtosis": round(float(values.kurtosis()), 3),
        "histogram": histogram,
    }


@router.get("/age-estimation")
async def estimate_tree_age():
    """Estimate tree age based on trunk diameter and ring count relationship."""
    df = await _get_tree_dataframe()

    # Trees that have ring_count data for training
    training = df[["diameter", "ring_count"]].dropna()
    if len(training) < 5:
        raise HTTPException(status_code=400, detail="Not enough ring count data for estimation")

    X_train = training["diameter"].values.reshape(-1, 1)
    y_train = training["ring_count"].values

    model = LinearRegression()
    model.fit(X_train, y_train)
    r_squared = model.score(X_train, y_train)

    # Predict for all trees
    all_diameters = df["diameter"].dropna().values.reshape(-1, 1)
    predicted_ages = model.predict(all_diameters)

    estimations = []
    for i, row in df.iterrows():
        if pd.notna(row.get("diameter")):
            pred = model.predict([[row["diameter"]]])[0]
            estimations.append({
                "tree_id": row.get("tree_id", ""),
                "diameter": round(float(row["diameter"]), 2),
                "actual_ring_count": int(row["ring_count"]) if pd.notna(row.get("ring_count")) else None,
                "estimated_age": round(float(max(pred, 0)), 1),
            })

    return {
        "model": "linear_regression (diameter → ring_count)",
        "coefficient": round(float(model.coef_[0]), 4),
        "intercept": round(float(model.intercept_), 4),
        "r_squared": round(r_squared, 4),
        "training_size": len(training),
        "estimations": estimations[:200],
    }


@router.get("/scatter-matrix")
async def get_scatter_matrix_data(
    variables: str = Query(
        "height,diameter,elevation,ring_count",
        description="Comma-separated variables for scatter matrix"
    )
):
    """Get data for scatter plot matrix visualization."""
    df = await _get_tree_dataframe()
    var_list = [v.strip() for v in variables.split(",")]
    available = [v for v in var_list if v in df.columns]

    if len(available) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 valid variables")

    subset = df[available + ["tree_id", "location_name"]].dropna(subset=available)
    # Limit to 500 points for performance
    if len(subset) > 500:
        subset = subset.sample(n=500, random_state=42)

    data_points = []
    for _, row in subset.iterrows():
        point = {"tree_id": row.get("tree_id", ""), "location": row.get("location_name", "")}
        for v in available:
            point[v] = round(float(row[v]), 3)
        data_points.append(point)

    return {
        "variables": available,
        "data_points": data_points,
        "sample_size": len(data_points),
    }
