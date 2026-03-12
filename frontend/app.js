/* ═══════════════════════════════════════════════════════════════
   Wild Tea Tree Platform – Utility JavaScript
   ═══════════════════════════════════════════════════════════════ */

const API_BASE = "";  // Same origin

// ─── Auth helpers ───────────────────────────────────────────────
function getToken() {
    return localStorage.getItem("tea_token");
}

function setToken(token) {
    localStorage.setItem("tea_token", token);
}

function getUser() {
    const u = localStorage.getItem("tea_user");
    return u ? JSON.parse(u) : null;
}

function setUser(user) {
    localStorage.setItem("tea_user", JSON.stringify(user));
}

function logout() {
    localStorage.removeItem("tea_token");
    localStorage.removeItem("tea_user");
    window.location.href = "/login";
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = "/login";
        return false;
    }
    return true;
}

// ─── API helpers ────────────────────────────────────────────────
async function apiFetch(url, options = {}) {
    const token = getToken();
    const headers = { "Content-Type": "application/json", ...options.headers };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(API_BASE + url, { ...options, headers });

    if (res.status === 401) {
        logout();
        throw new Error("Session expired");
    }

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Request failed" }));
        throw new Error(err.detail || "Request failed");
    }

    if (res.status === 204) return null;
    return res.json();
}

async function apiGet(url) {
    return apiFetch(url);
}

async function apiPost(url, data) {
    return apiFetch(url, { method: "POST", body: JSON.stringify(data) });
}

async function apiPut(url, data) {
    return apiFetch(url, { method: "PUT", body: JSON.stringify(data) });
}

async function apiDelete(url) {
    return apiFetch(url, { method: "DELETE" });
}

// ─── UI helpers ─────────────────────────────────────────────────
function showAlert(container, message, type = "error") {
    const div = document.createElement("div");
    div.className = `alert alert-${type}`;
    div.textContent = message;
    container.prepend(div);
    setTimeout(() => div.remove(), 5000);
}

function showLoading(container) {
    container.innerHTML = `<div class="loading"><div class="spinner"></div> Loading...</div>`;
}

function formatDate(dateStr) {
    if (!dateStr) return "—";
    return new Date(dateStr).toLocaleDateString("en-US", {
        year: "numeric", month: "short", day: "numeric"
    });
}

function roundNum(val, decimals = 2) {
    if (val == null || isNaN(val)) return "—";
    return Number(val).toFixed(decimals);
}

// ─── Navbar rendering ───────────────────────────────────────────
function renderNavbar(activePage) {
    const user = getUser();
    const pages = [
        { name: "Dashboard", href: "/dashboard", icon: "📊" },
        { name: "Trees", href: "/trees", icon: "🌳" },
        { name: "Map", href: "/map", icon: "🗺️" },
        { name: "Analytics", href: "/analytics", icon: "📈" },
        { name: "Satellite", href: "/satellite", icon: "🛰️" },
        { name: "Reports", href: "/reports", icon: "📋" },
        { name: "Alerts", href: "/alerts", icon: "🔔" },
        { name: "Upload", href: "/upload", icon: "📤" },
    ];

    const navLinks = pages.map(p =>
        `<a href="${p.href}" class="${p.name === activePage ? 'active' : ''}">${p.icon} ${p.name}</a>`
    ).join("");

    return `
    <div class="navbar">
        <div class="brand">
            <span>🌿</span> Wild Tea Tree Platform
        </div>
        <button class="hamburger" onclick="document.querySelector('.navbar nav').classList.toggle('open')" aria-label="Toggle menu">☰</button>
        <nav>${navLinks}</nav>
        <div class="user-section">
            <span>${user ? user.name : "Guest"}</span>
            <button class="btn-logout" onclick="logout()">⏻ Logout</button>
        </div>
    </div>`;
}
