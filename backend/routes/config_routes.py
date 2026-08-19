"""
Configuration & Network Routes
Provides LAN IP auto-detection and public/local URL endpoints for QR code generation.
"""
import os
import socket
from fastapi import APIRouter, Request
from backend.config import get_settings

router = APIRouter(prefix="/api", tags=["Configuration"])


def detect_lan_ip() -> str:
    """Auto-detect the machine's local network IPv4 address."""
    # Try outbound socket connection to detect actual LAN adapter
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            return ip
    except Exception:
        pass

    # Fallback to hostname resolution
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if ip and not ip.startswith('127.'):
            return ip
    except Exception:
        pass

    return "127.0.0.1"


@router.get("/network-info")
@router.get("/config/network")
async def get_network_info(request: Request):
    """
    Returns server network and LAN configuration for mobile / cross-device QR scanning.
    Priority order:
    1. FRONTEND_PUBLIC_URL / BACKEND_PUBLIC_URL environment variables
    2. LOCAL_NETWORK_HOST / HOST_IP environment variables
    3. Auto-detected LAN IP address
    """
    settings = get_settings()

    # Determine default port from incoming request or PORT env
    req_port = request.url.port if request.url.port else 3000
    port = os.getenv("PORT") or str(req_port)

    # 1. Full URL override
    full_url = (
        os.getenv("FRONTEND_PUBLIC_URL") or 
        settings.frontend_public_url or 
        os.getenv("BACKEND_PUBLIC_URL") or 
        settings.backend_public_url
    )
    if full_url:
        clean_url = full_url.strip().rstrip("/")
        host_part = clean_url.split("://")[-1].split("/")[0].split(":")[0]
        return {
            "lan_ip": host_part,
            "port": int(port) if str(port).isdigit() else 3000,
            "base_url": clean_url,
            "source": "environment_url_override",
            "is_configured": True,
        }

    # 2. Host / IP override
    host_override = (
        os.getenv("LOCAL_NETWORK_HOST") or 
        settings.local_network_host or 
        os.getenv("HOST_IP") or 
        settings.host_ip
    )
    if host_override:
        clean_host = host_override.strip().rstrip("/")
        if "://" in clean_host:
            base_url = clean_host
            lan_ip = clean_host.split("://")[-1].split("/")[0].split(":")[0]
        elif ":" in clean_host:
            base_url = f"http://{clean_host}"
            lan_ip = clean_host.split(":")[0]
        else:
            base_url = f"http://{clean_host}:{port}"
            lan_ip = clean_host

        return {
            "lan_ip": lan_ip,
            "port": int(port) if str(port).isdigit() else 3000,
            "base_url": base_url,
            "source": "environment_host_override",
            "is_configured": True,
        }

    # 3. Auto-detected LAN IP
    detected_ip = detect_lan_ip()
    base_url = f"http://{detected_ip}:{port}"

    return {
        "lan_ip": detected_ip,
        "port": int(port) if str(port).isdigit() else 3000,
        "base_url": base_url,
        "source": "auto_detected_lan",
        "is_configured": detected_ip != "127.0.0.1" and detected_ip != "localhost",
    }
