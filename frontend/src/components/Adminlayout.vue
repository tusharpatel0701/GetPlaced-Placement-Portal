<script setup>
import {
  ref,
  onMounted,
  onBeforeUnmount,
} from "vue";

import {
  useRouter,
  useRoute,
} from "vue-router";

const router = useRouter();
const route = useRoute();

// -----------------------------------
// State
// -----------------------------------
const sendingReminder = ref(false);
const sendingReport = ref(false);

const mobileOpen = ref(false);

const searchQuery = ref("");

const searchResults = ref({
  students: [],
  companies: [],
  drives: [],
});

const searching = ref(false);
const showResults = ref(false);

// -----------------------------------
// Logout
// -----------------------------------
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");

  router.push("/");
}

// -----------------------------------
// Reminder
// -----------------------------------
async function triggerReminder() {
  sendingReminder.value = true;

  try {
    const token = localStorage.getItem("token");

    const res = await fetch(
      "http://localhost:5000/api/admin/trigger-reminder",
      {
        method: "POST",

        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!res.ok) {
      throw new Error("Failed");
    }

    const data = await res.json();

    alert(data.message || "Reminders sent successfully.");
  } catch (err) {
    console.error(err);
    alert("Failed to send reminders.");
  } finally {
    sendingReminder.value = false;
  }
}

// -----------------------------------
// Monthly Report
// -----------------------------------
async function triggerMonthlyReport() {
  sendingReport.value = true;

  try {
    const token = localStorage.getItem("token");

    const res = await fetch(
      "http://localhost:5000/api/admin/trigger-monthly-report",
      {
        method: "POST",

        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!res.ok) {
      throw new Error("Failed");
    }

    const data = await res.json();

    alert(data.message || "Report generated successfully.");
  } catch (err) {
    console.error(err);
    alert("Failed to send report.");
  } finally {
    sendingReport.value = false;
  }
}

// -----------------------------------
// Search
// -----------------------------------
let searchTimeout = null;

async function onSearchInput() {
  const q = searchQuery.value.trim();

  if (!q || q.length < 2) {
    searchResults.value = {
      students: [],
      companies: [],
      drives: [],
    };

    showResults.value = false;

    return;
  }

  clearTimeout(searchTimeout);

  searchTimeout = setTimeout(async () => {
    searching.value = true;
    showResults.value = true;

    try {
      const token = localStorage.getItem("token");

      const res = await fetch(
        `http://localhost:5000/api/admin/search?q=${encodeURIComponent(q)}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) {
        throw new Error("Search failed");
      }

      const data = await res.json();

      searchResults.value = {
        students: Array.isArray(data.students)
          ? data.students
          : [],

        companies: Array.isArray(data.companies)
          ? data.companies
          : [],

        drives: Array.isArray(data.drives)
          ? data.drives
          : [],
      };
    } catch (err) {
      console.error(err);

      searchResults.value = {
        students: [],
        companies: [],
        drives: [],
      };
    } finally {
      searching.value = false;
    }
  }, 400);
}

// -----------------------------------
// Navigation
// -----------------------------------
function goToStudent() {
  showResults.value = false;
  searchQuery.value = "";

  router.push("/admin/students");
}

function goToCompany() {
  showResults.value = false;
  searchQuery.value = "";

  router.push("/admin/companies");
}

function goToDrive() {
  showResults.value = false;
  searchQuery.value = "";

  router.push("/admin/drives");
}

function closeSearch() {
  setTimeout(() => {
    showResults.value = false;
  }, 200);
}

// -----------------------------------
// Helpers
// -----------------------------------
function hasResults() {
  return (
    searchResults.value.students.length > 0 ||
    searchResults.value.companies.length > 0 ||
    searchResults.value.drives.length > 0
  );
}

// -----------------------------------
// ESC Key
// -----------------------------------
function handleEscape(e) {
  if (e.key === "Escape") {
    showResults.value = false;
    mobileOpen.value = false;
  }
}

// -----------------------------------
// Lifecycle
// -----------------------------------
onMounted(() => {
  window.addEventListener(
    "keydown",
    handleEscape
  );
});

onBeforeUnmount(() => {
  clearTimeout(searchTimeout);

  window.removeEventListener(
    "keydown",
    handleEscape
  );
});

// -----------------------------------
// Nav Items
// -----------------------------------
const navItems = [
  {
    label: "Overview",
    path: "/admin",
  },

  {
    label: "Students",
    path: "/admin/students",
  },

  {
    label: "Companies",
    path: "/admin/companies",
  },

  {
    label: "Drives",
    path: "/admin/drives",
  },

  {
    label: "Applications",
    path: "/admin/applications",
  },
];
</script>

<template>
  <div class="layout">

    <!-- Navbar -->
    <nav class="navbar">

      <div class="nav-inner">

        <!-- Brand -->
        <div
          class="nav-brand">

          <span class="brand-name">
            GetPlaced
          </span>

          <span class="brand-pill">
            Admin
          </span>
        </div>

        <!-- Desktop Nav -->
        <ul class="nav-links">

          <li
            v-for="item in navItems"
            :key="item.path"
          >
            <span
              class="nav-link"

              :class="{
                active:
                  item.path === '/admin'
                    ? route.path === '/admin'
                    : route.path.startsWith(item.path)
              }"

              @click="router.push(item.path)"
            >
              {{ item.label }}
            </span>
          </li>

          <!-- Daily Reminder -->
          <li>
            <button
              class="action-btn"

              @click="triggerReminder"

              :disabled="sendingReminder">

              {{
                sendingReminder
                  ? "Sending..."
                  : "Daily Reminder"
              }}
            </button>
          </li>

          <!-- Monthly Report -->
          <li>
            <button
              class="action-btn"

              @click="triggerMonthlyReport"

              :disabled="sendingReport"
            >

              {{
                sendingReport
                  ? "Generating..."
                  : "Monthly Report"
              }}
            </button>
          </li>

        </ul>

        <!-- Search -->
        <div class="search-wrap">

          <div class="search-box">

            <svg
              class="search-icon"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
            >
              <circle
                cx="11"
                cy="11"
                r="7"
                stroke="#888"
                stroke-width="2"
              />

              <path
                d="M20 20l-3-3"
                stroke="#888"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>

            <input
              type="text"
              class="search-input"

              placeholder="Search students, companies, drives..."

              v-model="searchQuery"

              @input="onSearchInput"

              @blur="closeSearch"

              @focus="
                searchQuery &&
                (showResults = true)
              "
            />

            <span
              v-if="searching"
              class="search-spinner"
            ></span>
          </div>

          <!-- Search Results -->
          <transition name="dropdown-fade">

            <div
              v-if="showResults"
              class="search-results"
            >
              <!-- Loading -->
              <div
                v-if="searching"
                class="search-empty"
              >
                🔍 Searching...
              </div>

              <!-- Empty -->
              <div
                v-else-if="!hasResults()"
                class="search-empty"
              >
                No results for
                "<strong>{{ searchQuery }}</strong>"
              </div>

              <!-- Results -->
              <template v-else>

                <!-- Students -->
                <div
                  v-if="searchResults.students.length > 0"
                >
                  <div class="result-section-label">
                    👨‍🎓 Students
                  </div>

                  <div
                    v-for="s in searchResults.students"
                    :key="'s-' + s.id"

                    class="result-item"

                    @mousedown="goToStudent"
                  >
                    <span class="result-name">
                      {{ s.name }}
                    </span>

                    <span class="result-meta">
                      ID: {{ s.id }}
                    </span>
                  </div>
                </div>

                <!-- Companies -->
                <div
                  v-if="searchResults.companies.length > 0"
                >
                  <div class="result-section-label">
                    🏢 Companies
                  </div>

                  <div
                    v-for="c in searchResults.companies"
                    :key="'c-' + c.id"

                    class="result-item"

                    @mousedown="goToCompany"
                  >
                    <span class="result-name">
                      {{ c.company_name }}
                    </span>

                    <span class="result-meta">
                      ID: {{ c.id }}
                    </span>
                  </div>
                </div>

                <!-- Drives -->
                <div
                  v-if="searchResults.drives.length > 0"
                >
                  <div class="result-section-label">
                    📅 Drives
                  </div>

                  <div
                    v-for="d in searchResults.drives"
                    :key="'d-' + d.id"

                    class="result-item"

                    @mousedown="goToDrive"
                  >
                    <span class="result-name">
                      {{ d.job_title }}
                    </span>

                    <span class="result-meta">
                      {{ d.company_name }}
                    </span>
                  </div>
                </div>

              </template>
            </div>

          </transition>
        </div>

        <!-- Right -->
        <div class="nav-right">
          <button
            class="btn-logout"
            @click="logout"
          >
            Logout
          </button>
        </div>

        <!-- Hamburger -->
        <button
          class="hamburger"
          @click="mobileOpen = !mobileOpen"
        >
          <span
            :class="
              mobileOpen
                ? 'bar bar-open-1'
                : 'bar'
            "
          ></span>

          <span
            :class="
              mobileOpen
                ? 'bar bar-open-2'
                : 'bar'
            "
          ></span>

          <span
            :class="
              mobileOpen
                ? 'bar bar-open-3'
                : 'bar'
            "
          ></span>
        </button>

      </div>

      <!-- Mobile -->
      <transition name="slide-down">

        <div
          v-if="mobileOpen"
          class="mobile-menu"
        >
          <!-- Links -->
          <span
            v-for="item in navItems"
            :key="'m-' + item.path"

            class="mobile-link"

            :class="{
              active:
                item.path === '/admin'
                  ? route.path === '/admin'
                  : route.path.startsWith(item.path)
            }"

            @click="
              router.push(item.path);
              mobileOpen = false;
            "
          >
            {{ item.label }}
          </span>

          <!-- Actions -->
          <div class="mobile-section-label">
            ⚡ Quick Actions
          </div>

          <button
            class="mobile-action-btn"

            @click="
              triggerReminder();
              mobileOpen = false;
            "

            :disabled="sendingReminder"
          >
            🔔

            {{
              sendingReminder
                ? "Sending..."
                : "Daily Reminder"
            }}
          </button>

          <button
            class="mobile-action-btn"

            @click="
              triggerMonthlyReport();
              mobileOpen = false;
            "

            :disabled="sendingReport"
          >
            📊

            {{
              sendingReport
                ? "Generating..."
                : "Monthly Report"
            }}
          </button>

          <!-- Footer -->
          <div class="mobile-footer">

            <span class="user-label">
              🛡️
            </span>

            <button
              class="btn-logout"
              @click="logout"
            >
              Logout
            </button>
          </div>
        </div>

      </transition>
    </nav>

    <!-- Content -->
    <div class="page-content">
      <router-view />
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&family=DM+Sans:wght@400;500&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.layout {
  font-family: 'DM Sans', sans-serif;

  width: 100%;
  min-height: 100vh;

  display: flex;
  flex-direction: column;

  background: #f8f7f4;
}

/* Navbar */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;

  z-index: 9999;

  background: rgba(248,247,244,0.92);

  backdrop-filter: blur(12px);

  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;

  padding: 0 24px;
  height: 60px;

  display: flex;
  align-items: center;
  gap: 20px;
}

/* Brand */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;

  flex-shrink: 0;

  cursor: pointer;
}

.brand-icon {
  font-size: 18px;
}

.brand-name {
  font-family: 'Bricolage Grotesque', sans-serif;

  font-weight: 800;
  font-size: 17px;

  color: #0f0f0f;
}

.brand-pill {
  font-size: 11px;
  font-weight: 600;

  background: #fee2e2;
  color: #991b1b;

  border: 1px solid #fca5a5;

  padding: 2px 8px;
  border-radius: 999px;
}

/* Nav */
.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;

  list-style: none;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 5px;

  padding: 6px 11px;
  border-radius: 8px;

  font-size: 13.5px;
  font-weight: 500;

  color: #555;

  cursor: pointer;
  white-space: nowrap;

  transition: all 0.15s ease;
}

.nav-link:hover {
  background: rgba(0,0,0,0.05);
  color: #0f0f0f;
}

.nav-link.active {
  background: #0f0f0f;
  color: white;
}

/* Action Buttons */
.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;

  padding: 8px 14px;

  border: 1px solid #e5e7eb;
  border-radius: 10px;

  background: white;

  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;

  color: #111827;

  cursor: pointer;

  transition: all 0.18s ease;

  white-space: nowrap;
}

.action-btn:hover:not(:disabled) {
  background: #111827;
  color: white;

  border-color: #111827;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Search */
.search-wrap {
  position: relative;

  flex: 1;
  max-width: 300px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;

  background: white;

  border: 1.5px solid #e5e7eb;
  border-radius: 10px;

  padding: 7px 12px;

  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}

.search-box:focus-within {
  border-color: #6366f1;

  box-shadow:
    0 0 0 3px rgba(99,102,241,0.1);
}

.search-input {
  flex: 1;

  border: none;
  outline: none;

  background: transparent;

  font-family: 'DM Sans', sans-serif;
}

.search-input::placeholder {
  color: #bbb;
}

.search-results {
  position: absolute;

  top: calc(100% + 8px);
  left: 0;

  width: 340px;
  max-height: 380px;

  overflow-y: auto;

  background: white;

  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 14px;

  box-shadow:
    0 10px 40px rgba(0,0,0,0.12),
    0 2px 10px rgba(0,0,0,0.06);

  z-index: 99999;
}

.search-empty {
  padding: 20px;

  text-align: center;

  font-size: 13px;
  color: #888;
}

.result-section-label {
  padding: 8px 14px 6px;

  font-size: 11px;
  font-weight: 600;

  text-transform: uppercase;
  letter-spacing: 0.06em;

  color: #aaa;

  border-bottom: 1px solid #f3f4f6;
}

.result-item {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 10px 14px;

  cursor: pointer;

  border-bottom: 1px solid #f9fafb;

  transition: background 0.15s ease;
}

.result-item:hover {
  background: #f8f7f4;
}

.result-name {
  font-size: 13px;
  font-weight: 500;

  color: #0f0f0f;
}

.result-meta {
  font-size: 11px;
  color: #aaa;
}

/* Spinner */
.search-spinner {
  width: 14px;
  height: 14px;

  border: 2px solid #e5e7eb;
  border-top-color: #6366f1;

  border-radius: 50%;

  animation: spin 0.7s linear infinite;
}

/* Right */
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;

  margin-left: auto;
}

.user-label {
  font-size: 18px;
}

.btn-logout {
  padding: 7px 16px;

  border: 1.5px solid #0f0f0f;
  border-radius: 8px;

  background: transparent;

  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;

  cursor: pointer;

  transition:
    background 0.18s,
    color 0.18s;
}

.btn-logout:hover {
  background: #0f0f0f;
  color: white;
}

/* Hamburger */
.hamburger {
  display: none;

  flex-direction: column;
  gap: 5px;

  background: none;
  border: none;

  cursor: pointer;

  margin-left: auto;
}

.bar {
  width: 22px;
  height: 2px;

  background: #0f0f0f;

  border-radius: 2px;

  transition: all 0.25s ease;
}

.bar-open-1 {
  transform:
    translateY(7px)
    rotate(45deg);
}

.bar-open-2 {
  opacity: 0;
}

.bar-open-3 {
  transform:
    translateY(-7px)
    rotate(-45deg);
}

/* Mobile */
.mobile-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;

  padding: 16px;

  border-top: 1px solid rgba(0,0,0,0.06);

  background: rgba(248,247,244,0.98);

  max-height: calc(100vh - 60px);
  overflow-y: auto;
}

.mobile-link {
  padding: 10px 14px;
  border-radius: 10px;

  font-size: 15px;
  font-weight: 500;

  color: #555;

  cursor: pointer;

  transition: all 0.15s ease;
}

.mobile-link:hover {
  background: rgba(0,0,0,0.05);
}

.mobile-link.active {
  background: #0f0f0f;
  color: white;
}

.mobile-section-label {
  font-size: 11px;
  font-weight: 600;

  text-transform: uppercase;
  letter-spacing: 0.06em;

  color: #aaa;

  padding: 10px 14px 4px;
}

.mobile-action-btn {
  display: flex;
  align-items: center;
  gap: 8px;

  padding: 10px 14px;

  border-radius: 10px;

  background: white;
  border: 1px solid #e5e7eb;

  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;

  color: #0f0f0f;

  cursor: pointer;

  transition: background 0.15s ease;
}

.mobile-action-btn:hover:not(:disabled) {
  background: #f3f4f6;
}

.mobile-action-btn:disabled {
  opacity: 0.4;
}

.mobile-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-top: 12px;
  margin-top: 8px;

  border-top: 1px solid rgba(0,0,0,0.06);
}

/* Page */
.page-content {
  flex: 1;
  margin-top: 60px;
}

/* Animations */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Transitions */
.dropdown-fade-enter-active {
  transition:
    opacity 0.15s,
    transform 0.15s;
}

.dropdown-fade-leave-active {
  transition:
    opacity 0.12s,
    transform 0.12s;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.slide-down-enter-active {
  transition: all 0.22s ease;
}

.slide-down-leave-active {
  transition: all 0.18s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Responsive */
@media (max-width: 1200px) {
  .action-btn {
    padding: 8px 10px;
    font-size: 12px;
  }
}

@media (max-width: 1024px) {
  .search-wrap {
    max-width: 220px;
  }
}

@media (max-width: 860px) {
  .nav-links,
  .nav-right,
  .search-wrap {
    display: none;
  }

  .hamburger {
    display: flex;
  }
}
</style>