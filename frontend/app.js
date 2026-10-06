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
        { name: "Citizen Science", href: "/citizen", icon: "👥" },
        { name: "Climate Simulator", href: "/climate-scenarios", icon: "🌡️" },
        { name: "Regions", href: "/regions", icon: "🌐" },
        { name: "Soil Portal", href: "/soil", icon: "🌱" },
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


/* ============================================================
   TEATREE MODERN NAVIGATION
   ============================================================ */

/*
    IMPORTANT:

    This function intentionally keeps the same function name
    used by the existing TeaTree pages:

        renderNavbar("Map")
        renderNavbar("Trees")
        renderNavbar("Soil Portal")

    Therefore existing HTML pages do NOT need to be rewritten.
*/

function renderNavbar(currentPage = "") {

    /*
        Normalize page names used by existing pages.
    */

    const page = String(currentPage || "").toLowerCase();

    const isActive = (...names) => {

        return names.some(name =>
            page.includes(String(name).toLowerCase())
        );

    };


    /*
        DASHBOARD
    */

    const dashboardActive =
        isActive("dashboard");


    /*
        TREES
    */

    const treesActive =
        isActive("trees", "tree inventory");


    /*
        EXPLORE
    */

    const mapActive =
        isActive("map");

    const passportActive =
        isActive("passport");

    const citizenActive =
        isActive("citizen");


    const exploreActive =
        mapActive ||
        passportActive ||
        citizenActive;


    /*
        ANALYTICS
    */

    const analyticsActive =
        isActive("analytics");

    const ecosystemActive =
        isActive("ecosystem", "ehi");

    const regionsActive =
        isActive("regions", "regional");

    const soilActive =
        isActive("soil", "soil portal");


    const analyticsGroupActive =
        analyticsActive ||
        ecosystemActive ||
        regionsActive ||
        soilActive;


    /*
        MONITORING
    */

    const healthActive =
        isActive("health", "tree health");

    const climateActive =
        isActive("climate");

    const satelliteActive =
        isActive("satellite");

    const alertsActive =
        isActive("alerts");

    const lifecycleActive =
        isActive("lifecycle");

    const monitoringGroupActive =
        healthActive ||
        climateActive ||
        satelliteActive ||
        alertsActive ||
        lifecycleActive;


    /*
        REPORTS
    */

    const reportsActive =
        isActive("reports");


    /*
        USER INFORMATION
    */

    let userName = "";

    try {

        const storedUser =
            localStorage.getItem("user");

        if (storedUser) {

            const user =
                JSON.parse(storedUser);

            userName =
                user.name ||
                user.username ||
                user.email ||
                "";

        }

    } catch (error) {

        console.warn(
            "Unable to read stored user:",
            error
        );

    }


    /*
        NAVIGATION HTML
    */

    return `

        <nav class="tt-navbar">

            <!-- =================================================
                 BRAND
                 ================================================= -->

            <a
                href="/dashboard"
                class="tt-brand"
                aria-label="TeaTree Dashboard">

                <span class="tt-brand-icon">
                    🌿
                </span>

                <span class="tt-brand-text">
                    TeaTree
                </span>

            </a>


            <!-- =================================================
                 MOBILE MENU BUTTON
                 ================================================= -->

            <button
                type="button"
                class="tt-mobile-btn"
                id="tt-mobile-menu-btn"
                aria-label="Open navigation"
                aria-expanded="false"
                onclick="toggleTeaTreeMobileMenu()">

                ☰

            </button>


            <!-- =================================================
                 MAIN NAVIGATION
                 ================================================= -->

            <div
                class="tt-nav"
                id="tt-navigation">


                <!-- =================================================
                     DASHBOARD
                     ================================================= -->

                <div class="tt-nav-item">

                    <a
                        href="/dashboard"
                        class="tt-nav-link ${dashboardActive ? "active" : ""}">

                        <span>🏠</span>
                        <span>Dashboard</span>

                    </a>

                </div>


                <!-- =================================================
                     TREES
                     ================================================= -->

                <div class="tt-nav-item">

                    <a
                        href="/trees"
                        class="tt-nav-link ${treesActive ? "active" : ""}">

                        <span>🌳</span>
                        <span>Trees</span>

                    </a>

                </div>


                <!-- =================================================
                     EXPLORE
                     ================================================= -->

                <div
                    class="tt-nav-item ${exploreActive ? "group-active" : ""}">

                    <a
                        href="#"
                        class="tt-nav-link ${exploreActive ? "active" : ""}"
                        onclick="toggleTeaTreeDropdown(event, this)"
                        aria-haspopup="true"
                        aria-expanded="false">

                        <span>🔎</span>
                        <span>Explore</span>

                        <span class="tt-nav-arrow">
                            ▼
                        </span>

                    </a>


                    <div class="tt-dropdown">


                        <a
                            href="/map"
                            class="${mapActive ? "active" : ""}">

                            <span>🗺️</span>
                            <span>Tree Map</span>

                        </a>


                        <a
                            href="/tree_passport.html"
                            class="${passportActive ? "active" : ""}">

                            <span>🪪</span>
                            <span>Tree Passport</span>

                        </a>


                        <a
                            href="/citizen"
                            class="${citizenActive ? "active" : ""}">

                            <span>👥</span>
                            <span>Citizen Science</span>

                        </a>


                    </div>

                </div>


                <!-- =================================================
                     ANALYTICS
                     ================================================= -->

                <div
                    class="tt-nav-item ${analyticsGroupActive ? "group-active" : ""}">

                    <a
                        href="#"
                        class="tt-nav-link ${analyticsGroupActive ? "active" : ""}"
                        onclick="toggleTeaTreeDropdown(event, this)"
                        aria-haspopup="true"
                        aria-expanded="false">

                        <span>📊</span>
                        <span>Analytics</span>

                        <span class="tt-nav-arrow">
                            ▼
                        </span>

                    </a>


                    <div class="tt-dropdown">


                        <a
                            href="/analytics"
                            class="${analyticsActive ? "active" : ""}">

                            <span>📈</span>
                            <span>Analytics Dashboard</span>

                        </a>


                        <!--
                            Ecosystem Health

                            Only keep this item if your FastAPI
                            frontend actually has an /ecosystem page.

                            If it does not, this item is hidden.
                        -->

                        <a
                            href="/analytics"
                            class="${ecosystemActive ? "active" : ""}">

                            <span>🌱</span>
                            <span>Ecosystem Health</span>

                        </a>


                        <a
                            href="/regions"
                            class="${regionsActive ? "active" : ""}">

                            <span>🌍</span>
                            <span>Regional Comparison</span>

                        </a>


                        <a
                            href="/soil"
                            class="${soilActive ? "active" : ""}">

                            <span>🪨</span>
                            <span>Soil Health</span>

                        </a>


                    </div>

                </div>


                <!-- =================================================
                     MONITORING
                     ================================================= -->

                <div
                    class="tt-nav-item ${monitoringGroupActive ? "group-active" : ""}">

                    <a
                        href="#"
                        class="tt-nav-link ${monitoringGroupActive ? "active" : ""}"
                        onclick="toggleTeaTreeDropdown(event, this)"
                        aria-haspopup="true"
                        aria-expanded="false">

                        <span>🛰️</span>
                        <span>Monitoring</span>

                        <span class="tt-nav-arrow">
                            ▼
                        </span>

                    </a>


                    <div class="tt-dropdown">


                        <a
                            href="/tree-health"
                            class="${healthActive ? "active" : ""}">

                            <span>❤️</span>
                            <span>Tree Health</span>

                        </a>


                        <a
                            href="/climate-scenarios"
                            class="${climateActive ? "active" : ""}">

                            <span>🌡️</span>
                            <span>Climate</span>

                        </a>


                        <a
                            href="/satellite"
                            class="${satelliteActive ? "active" : ""}">

                            <span>🛰️</span>
                            <span>Satellite</span>

                        </a>


                        <a
                            href="/alerts"
                            class="${alertsActive ? "active" : ""}">

                            <span>🚨</span>
                            <span>Alerts</span>

                        </a>


                        <a
                            href="/tea_lifecycle"
                            class="${lifecycleActive ? "active" : ""}">

                            <span>🌿</span>
                            <span>Lifecycle Intelligence</span>

                        </a>


                    </div>

                </div>


                <!-- =================================================
                     REPORTS
                     ================================================= -->

                <div class="tt-nav-item">

                    <a
                        href="/reports"
                        class="tt-nav-link ${reportsActive ? "active" : ""}">

                        <span>📄</span>
                        <span>Reports</span>

                    </a>

                </div>


            </div>


            <!-- =================================================
                 USER AREA
                 ================================================= -->

            <div class="tt-user-area">

                ${
                    userName
                        ? `
                            <span class="tt-user-name">
                                ${escapeTeaTreeHTML(userName)}
                            </span>
                          `
                        : ""
                }


                <button
                    type="button"
                    class="tt-logout-btn"
                    onclick="teaTreeLogout()">

                    Logout

                </button>

            </div>


        </nav>

    `;
}


/* ============================================================
   HTML ESCAPE
   ============================================================ */

function escapeTeaTreeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        String(value ?? "");

    return div.innerHTML;
}


/* ============================================================
   DROPDOWN HANDLER
   ============================================================ */

function toggleTeaTreeDropdown(event, element) {

    event.preventDefault();
    event.stopPropagation();


    const currentItem =
        element.closest(".tt-nav-item");


    if (!currentItem) {
        return;
    }


    const currentDropdown =
        currentItem.querySelector(".tt-dropdown");


    const currentlyOpen =
        currentItem.classList.contains("open");


    /*
        Close every other dropdown.
    */

    document
        .querySelectorAll(".tt-nav-item.open")
        .forEach(item => {

            if (item !== currentItem) {

                item.classList.remove("open");

                const link =
                    item.querySelector(".tt-nav-link");

                if (link) {

                    link.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }

        });


    /*
        Toggle current dropdown.
    */

    currentItem.classList.toggle(
        "open",
        !currentlyOpen
    );


    element.setAttribute(
        "aria-expanded",
        !currentlyOpen
            ? "true"
            : "false"
    );

}


/* ============================================================
   CLOSE DROPDOWNS WHEN CLICKING OUTSIDE
   ============================================================ */

document.addEventListener(
    "click",
    function(event) {

        if (
            !event.target.closest(".tt-nav-item")
        ) {

            document
                .querySelectorAll(
                    ".tt-nav-item.open"
                )
                .forEach(item => {

                    item.classList.remove(
                        "open"
                    );


                    const link =
                        item.querySelector(
                            ".tt-nav-link"
                        );

                    if (link) {

                        link.setAttribute(
                            "aria-expanded",
                            "false"
                        );

                    }

                });

        }

    }
);


/* ============================================================
   MOBILE MENU
   ============================================================ */

function toggleTeaTreeMobileMenu() {

    const navigation =
        document.getElementById(
            "tt-navigation"
        );


    const button =
        document.getElementById(
            "tt-mobile-menu-btn"
        );


    if (!navigation || !button) {
        return;
    }


    const isOpen =
        navigation.classList.toggle(
            "mobile-open"
        );


    button.setAttribute(
        "aria-expanded",
        isOpen
            ? "true"
            : "false"
    );


    button.textContent =
        isOpen
            ? "✕"
            : "☰";

}


/* ============================================================
   LOGOUT
   ============================================================ */

function teaTreeLogout() {

    /*
        Keep this intentionally compatible
        with your existing authentication.
    */

    const possibleKeys = [

        "token",
        "access_token",
        "auth_token",
        "jwt",
        "user"

    ];


    possibleKeys.forEach(key => {

        try {

            localStorage.removeItem(key);

        } catch (error) {

            console.warn(
                "Unable to remove localStorage key:",
                key
            );

        }

    });


    window.location.href =
        "/login";

}