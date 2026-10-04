"""
Wild Tea Tree Big Data Visualization Platform
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.database import connect_to_mongo, close_mongo_connection
from backend.routes.auth_routes import router as auth_router
from backend.routes.tree_routes import router as tree_router
from backend.routes.environmental_routes import router as env_router
from backend.routes.analytics_routes import router as analytics_router
from backend.routes.map_routes import router as map_router
from backend.routes.health_routes import router as health_router
from backend.routes.climate_routes import router as climate_router
from backend.routes.satellite_routes import router as satellite_router
from backend.routes.report_routes import router as report_router
from backend.routes.alert_routes import router as alert_router
from backend.routes.soil_routes import router as soil_router
from backend.routes.citizen_routes import router as citizen_router
from backend.routes.conservation_routes import router as conservation_router
from backend.routes.ecosystem_routes import router as ecosystem_router
from backend.routes.region_routes import router as region_router
from backend.routes.config_routes import router as config_router
from backend.routes import lifecycle_routes

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="Wild Tea Tree Big Data Visualization Platform",
    description="Data management, analytics, and visualization platform for wild tea tree research",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth_router)
app.include_router(tree_router)
app.include_router(env_router)
app.include_router(analytics_router)
app.include_router(map_router)
app.include_router(health_router)
app.include_router(climate_router)
app.include_router(satellite_router)
app.include_router(report_router)
app.include_router(alert_router)
app.include_router(soil_router)
app.include_router(citizen_router)
app.include_router(conservation_router)
app.include_router(ecosystem_router)
app.include_router(region_router)
app.include_router(config_router)
app.include_router(lifecycle_routes.router)

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Serve static frontend files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/login")
async def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))


@app.get("/register")
async def serve_register():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))


@app.get("/dashboard")
async def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))


@app.get("/trees")
async def serve_trees_page():
    return FileResponse(os.path.join(FRONTEND_DIR, "trees.html"))


@app.get("/tree/{tree_id}")
async def serve_tree_detail(tree_id: str):
    return FileResponse(os.path.join(FRONTEND_DIR, "tree_detail.html"))


@app.get("/trees/{tree_id}")
@app.get("/passport/{tree_id}")
@app.get("/tree_passport.html")
async def serve_passport(tree_id: str = None):
    return FileResponse(os.path.join(FRONTEND_DIR, "tree_passport.html"))


@app.get("/map")
async def serve_map():
    return FileResponse(os.path.join(FRONTEND_DIR, "map.html"))


@app.get("/analytics")
async def serve_analytics():
    return FileResponse(os.path.join(FRONTEND_DIR, "analytics.html"))


@app.get("/upload")
async def serve_upload():
    return FileResponse(os.path.join(FRONTEND_DIR, "upload.html"))


@app.get("/alerts")
async def serve_alerts():
    return FileResponse(os.path.join(FRONTEND_DIR, "alerts.html"))


@app.get("/satellite")
async def serve_satellite():
    return FileResponse(os.path.join(FRONTEND_DIR, "satellite.html"))


@app.get("/reports")
async def serve_reports():
    return FileResponse(os.path.join(FRONTEND_DIR, "reports.html"))


@app.get("/soil")
async def serve_soil():
    return FileResponse(os.path.join(FRONTEND_DIR, "soil.html"))


@app.get("/citizen_submit.html")
@app.get("/citizen")
async def serve_citizen():
    return FileResponse(os.path.join(FRONTEND_DIR, "citizen_submit.html"))


@app.get("/climate_scenarios.html")
@app.get("/climate-scenarios")
async def serve_climate_scenarios():
    return FileResponse(os.path.join(FRONTEND_DIR, "climate_scenarios.html"))


@app.get("/region_comparison.html")
@app.get("/regions")
async def serve_regions():
    return FileResponse(os.path.join(FRONTEND_DIR, "region_comparison.html"))

from fastapi.responses import FileResponse


@app.get("/tea-lifecycle")
async def tea_lifecycle_page():

    return FileResponse(
        "frontend/tea_lifecycle.html"
    )
