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

app = FastAPI(
    title="Wild Tea Tree Big Data Visualization Platform",
    description="Data management, analytics, and visualization platform for wild tea tree research",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup / shutdown events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

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
