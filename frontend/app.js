/* ═══════════════════════════════════════════════════════════════
   Wild Tea Tree Platform – Utility JavaScript
   ═══════════════════════════════════════════════════════════════ */

const API_BASE = "";


// ═══════════════════════════════════════════════════════════════
// AUTH HELPERS
// ═══════════════════════════════════════════════════════════════

function getToken() {
    return localStorage.getItem("tea_token");
}


function setToken(token) {
    localStorage.setItem("tea_token", token);
}


function getUser() {

    const u = localStorage.getItem("tea_user");

    try {
        return u ? JSON.parse(u) : null;
    } catch {
        return null;
    }
}


function setUser(user) {
    localStorage.setItem(
        "tea_user",
        JSON.stringify(user)
    );
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


// ═══════════════════════════════════════════════════════════════
// API HELPERS
// ═══════════════════════════════════════════════════════════════

async function apiFetch(url, options = {}) {

    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };

    if (token) {
        headers["Authorization"] =
            `Bearer ${token}`;
    }


    const res = await fetch(
        API_BASE + url,
        {
            ...options,
            headers
        }
    );


    if (res.status === 401) {

        logout();

        throw new Error(
            "Session expired"
        );
    }


    if (!res.ok) {

        const err =
            await res
                .json()
                .catch(() => ({
                    detail: "Request failed"
                }));


        throw new Error(
            err.detail ||
            "Request failed"
        );
    }


    if (res.status === 204) {
        return null;
    }


    return res.json();
}


async function apiGet(url) {

    return apiFetch(url);
}


async function apiPost(url, data) {

    return apiFetch(
        url,
        {
            method: "POST",
            body: JSON.stringify(data)
        }
    );
}


async function apiPut(url, data) {

    return apiFetch(
        url,
        {
            method: "PUT",
            body: JSON.stringify(data)
        }
    );
}


async function apiDelete(url) {

    return apiFetch(
        url,
        {
            method: "DELETE"
        }
    );
}


// ═══════════════════════════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════════════════════════

function showAlert(
    container,
    message,
    type = "error"
) {

    const div =
        document.createElement("div");


    div.className =
        `alert alert-${type}`;


    div.textContent =
        message;


    container.prepend(div);


    setTimeout(
        () => div.remove(),
        5000
    );
}


function showLoading(container) {

    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            Loading...
        </div>
    `;
}


function formatDate(dateStr) {

    if (!dateStr) {
        return "—";
    }


    return new Date(
        dateStr
    ).toLocaleDateString(
        "en-US",
        {
            year: "numeric",
            month: "short",
            day: "numeric"
        }
    );
}


function roundNum(
    val,
    decimals = 2
) {

    if (
        val == null ||
        isNaN(val)
    ) {
        return "—";
    }


    return Number(val)
        .toFixed(decimals);
}


// ═══════════════════════════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════════════════════════

function renderNavbar(activePage = "") {

    const user =
        getUser();


    const page =
        String(activePage)
            .toLowerCase()
            .trim();


    /*
       Helper used to determine
       which menu/group is active.
    */

    function isActive(...names) {

        return names.some(
            name =>
                page.includes(
                    String(name)
                        .toLowerCase()
                )
        );
    }


    // ───────────────────────────────────────────────────────────
    // INDIVIDUAL PAGES
    // ───────────────────────────────────────────────────────────

    const dashboardActive =
        isActive("dashboard");


    const treesActive =
        isActive(
            "trees",
            "tree inventory"
        );


    const mapActive =
        isActive("map");


    const citizenActive =
        isActive(
            "citizen",
            "citizen science"
        );


    const analyticsActive =
        isActive(
            "analytics",
            "analytics dashboard"
        );


    const regionsActive =
        isActive(
            "regions",
            "regional"
        );


    const soilActive =
        isActive(
            "soil",
            "soil portal"
        );


    const climateActive =
        isActive(
            "climate",
            "climate simulator"
        );


    const satelliteActive =
        isActive("satellite");


    const alertsActive =
        isActive("alerts");


    const lifecycleActive =
        isActive(
            "lifecycle",
            "lifecycle intelligence"
        );


    const reportsActive =
        isActive("reports");


    const uploadActive =
        isActive("upload");


    // ───────────────────────────────────────────────────────────
    // GROUP ACTIVE STATES
    // ───────────────────────────────────────────────────────────

    const exploreActive =
        mapActive ||
        citizenActive;


    const analyticsGroupActive =
        analyticsActive ||
        regionsActive ||
        soilActive;


    const monitoringGroupActive =
        climateActive ||
        satelliteActive ||
        alertsActive ||
        lifecycleActive;


    // ───────────────────────────────────────────────────────────
    // USER NAME
    // ───────────────────────────────────────────────────────────

    const userName =
        user &&
        (
            user.name ||
            user.username ||
            user.email
        )
            ? (
                user.name ||
                user.username ||
                user.email
            )
            : "Guest";


    // ───────────────────────────────────────────────────────────
    // NAVBAR
    // ───────────────────────────────────────────────────────────

    return `

        <div class="navbar">


            <!-- ═══════════════════════════════════════════════
                 BRAND
                 ═══════════════════════════════════════════════ -->

            <a
                href="/dashboard"
                class="brand"
                aria-label="Wild Tea Tree Platform">

                <span>🌿</span>

                <span>
                    Wild Tea Tree Platform
                </span>

            </a>


            <!-- ═══════════════════════════════════════════════
                 MOBILE BUTTON
                 ═══════════════════════════════════════════════ -->

            <button
                class="hamburger"
                onclick="toggleTeaTreeMobileMenu()"
                aria-label="Toggle menu">

                ☰

            </button>


            <!-- ═══════════════════════════════════════════════
                 MAIN NAVIGATION
                 ═══════════════════════════════════════════════ -->

            <nav id="tea-main-nav">


                <!-- DASHBOARD -->

                <a
                    href="/dashboard"
                    class="${
                        dashboardActive
                            ? "active"
                            : ""
                    }">

                    📊 Dashboard

                </a>


                <!-- TREES -->

                <a
                    href="/trees"
                    class="${
                        treesActive
                            ? "active"
                            : ""
                    }">

                    🌳 Trees

                </a>


                <!-- ═══════════════════════════════════════
                     EXPLORE
                     ═══════════════════════════════════════ -->

                <div
                    class="
                        nav-dropdown
                        ${
                            exploreActive
                                ? "group-active"
                                : ""
                        }
                    ">


                    <button
                        type="button"
                        class="nav-dropdown-btn"
                        onclick="toggleTeaTreeDropdown(this)"
                        aria-haspopup="true"
                        aria-expanded="false">

                        🔎 Explore
                        <span>▾</span>

                    </button>


                    <div class="nav-dropdown-menu">


                        <a
                            href="/map"
                            class="${
                                mapActive
                                    ? "active"
                                    : ""
                            }">

                            🗺️ Tree Map

                        </a>


                        <a
                            href="/citizen"
                            class="${
                                citizenActive
                                    ? "active"
                                    : ""
                            }">

                            👥 Citizen Science

                        </a>


                    </div>

                </div>


                <!-- ═══════════════════════════════════════
                     ANALYTICS
                     ═══════════════════════════════════════ -->

                <div
                    class="
                        nav-dropdown
                        ${
                            analyticsGroupActive
                                ? "group-active"
                                : ""
                        }
                    ">


                    <button
                        type="button"
                        class="nav-dropdown-btn"
                        onclick="toggleTeaTreeDropdown(this)"
                        aria-haspopup="true"
                        aria-expanded="false">

                        📈 Analytics
                        <span>▾</span>

                    </button>


                    <div class="nav-dropdown-menu">


                        <a
                            href="/analytics"
                            class="${
                                analyticsActive
                                    ? "active"
                                    : ""
                            }">

                            📊 Analytics Dashboard

                        </a>


                        <a
                            href="/regions"
                            class="${
                                regionsActive
                                    ? "active"
                                    : ""
                            }">

                            🌍 Regional Comparison

                        </a>


                        <a
                            href="/soil"
                            class="${
                                soilActive
                                    ? "active"
                                    : ""
                            }">

                            🌱 Soil Portal

                        </a>


                    </div>

                </div>


                <!-- ═══════════════════════════════════════
                     MONITORING
                     ═══════════════════════════════════════ -->

                <div
                    class="
                        nav-dropdown
                        ${
                            monitoringGroupActive
                                ? "group-active"
                                : ""
                        }
                    ">


                    <button
                        type="button"
                        class="nav-dropdown-btn"
                        onclick="toggleTeaTreeDropdown(this)"
                        aria-haspopup="true"
                        aria-expanded="false">

                        🛰️ Monitoring
                        <span>▾</span>

                    </button>


                    <div class="nav-dropdown-menu">


                        <a
                            href="/climate-scenarios"
                            class="${
                                climateActive
                                    ? "active"
                                    : ""
                            }">

                            🌡️ Climate Simulator

                        </a>


                        <a
                            href="/satellite"
                            class="${
                                satelliteActive
                                    ? "active"
                                    : ""
                            }">

                            🛰️ Satellite

                        </a>


                        <a
                            href="/alerts"
                            class="${
                                alertsActive
                                    ? "active"
                                    : ""
                            }">

                            🔔 Alerts

                        </a>


                        <a
                            href="/tea_lifecycle"
                            class="${
                                lifecycleActive
                                    ? "active"
                                    : ""
                            }">

                            🌿 Lifecycle Intelligence

                        </a>


                    </div>

                </div>


                <!-- REPORTS -->

                <a
                    href="/reports"
                    class="${
                        reportsActive
                            ? "active"
                            : ""
                    }">

                    📋 Reports

                </a>


                <!-- UPLOAD -->

                <a
                    href="/upload"
                    class="${
                        uploadActive
                            ? "active"
                            : ""
                    }">

                    📤 Upload

                </a>


            </nav>


            <!-- ═══════════════════════════════════════════════
                 USER
                 ═══════════════════════════════════════════════ -->

            <div class="user-section">

                <span>
                    ${escapeHtml(userName)}
                </span>


                <button
                    class="btn-logout"
                    onclick="logout()">

                    ⏻ Logout

                </button>

            </div>


        </div>

    `;
}


// ═══════════════════════════════════════════════════════════════
// NAVIGATION DROPDOWN
// ═══════════════════════════════════════════════════════════════

function toggleTeaTreeDropdown(button) {

    const dropdown =
        button.closest(
            ".nav-dropdown"
        );


    if (!dropdown) {
        return;
    }


    const wasOpen =
        dropdown.classList.contains(
            "open"
        );


    /*
       Close all other dropdowns.
    */

    document
        .querySelectorAll(
            ".nav-dropdown.open"
        )
        .forEach(item => {

            if (item !== dropdown) {

                item.classList.remove(
                    "open"
                );


                const btn =
                    item.querySelector(
                        ".nav-dropdown-btn"
                    );


                if (btn) {

                    btn.setAttribute(
                        "aria-expanded",
                        "false"
                    );
                }
            }
        });


    /*
       Toggle current dropdown.
    */

    dropdown.classList.toggle(
        "open",
        !wasOpen
    );


    button.setAttribute(
        "aria-expanded",
        !wasOpen
            ? "true"
            : "false"
    );
}


// ═══════════════════════════════════════════════════════════════
// CLOSE DROPDOWNS WHEN CLICKING OUTSIDE
// ═══════════════════════════════════════════════════════════════

document.addEventListener(
    "click",
    function(event) {

        if (
            !event.target.closest(
                ".nav-dropdown"
            )
        ) {

            document
                .querySelectorAll(
                    ".nav-dropdown.open"
                )
                .forEach(item => {

                    item.classList.remove(
                        "open"
                    );


                    const button =
                        item.querySelector(
                            ".nav-dropdown-btn"
                        );


                    if (button) {

                        button.setAttribute(
                            "aria-expanded",
                            "false"
                        );

                    }

                });

        }

    }
);


// ═══════════════════════════════════════════════════════════════
// MOBILE MENU
// ═══════════════════════════════════════════════════════════════

function toggleTeaTreeMobileMenu() {

    const nav =
        document.getElementById(
            "tea-main-nav"
        );


    if (!nav) {
        return;
    }


    nav.classList.toggle(
        "open"
    );
}


// ═══════════════════════════════════════════════════════════════
// HTML ESCAPE
// ═══════════════════════════════════════════════════════════════

function escapeHtml(value) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        String(value ?? "");


    return div.innerHTML;
}