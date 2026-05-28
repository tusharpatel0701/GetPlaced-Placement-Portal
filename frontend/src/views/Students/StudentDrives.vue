<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const drives = ref([]);
const applications = ref([]);
const loading = ref(true);
const error = ref("");
const applyingId = ref(null);
const applyError = ref("");
const applySuccess = ref("");

const searchQuery = ref("");
const filterBranch = ref("");
const filterMinCgpa = ref("");
const filterYear = ref("");

const studentId = localStorage.getItem("student_id");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("student")) { router.push("/login"); return; }
  await Promise.all([fetchDrives(), fetchApplications()]);
});

async function fetchDrives() {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await fetch("http://localhost:5000/api/student/drives", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error();
    drives.value = await res.json();
  } catch {
    error.value = "Could not load drives.";
  } finally {
    loading.value = false;
  }
}

async function fetchApplications() {
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/student/applications/${studentId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) applications.value = await res.json();
  } catch {}
}

function hasApplied(driveId) {
  return applications.value.some(a => a.drive_id === driveId);
}

async function applyToDrive(driveId) {
  applyingId.value = driveId;
  applyError.value = "";
  applySuccess.value = "";
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/student/apply/${driveId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ student_id: parseInt(studentId) }),
    });
    const data = await res.json();
    if (!res.ok) { applyError.value = data.message || "Failed to apply."; return; }
    applySuccess.value = "Application submitted successfully!";
    await fetchApplications();
  } catch {
    applyError.value = "Server error. Try again.";
  } finally {
    applyingId.value = null;
  }
}

const filteredDrives = computed(() => {
  return drives.value.filter(d => {
    const matchSearch = !searchQuery.value ||
      d.job_title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      d.company_name?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchBranch = !filterBranch.value ||
      d.eligibility_branch?.toLowerCase().includes(filterBranch.value.toLowerCase());
    const matchCgpa = !filterMinCgpa.value ||
      (d.min_cgpa <= parseFloat(filterMinCgpa.value));
    const matchYear = !filterYear.value ||
      String(d.eligible_year) === String(filterYear.value);
    return matchSearch && matchBranch && matchCgpa && matchYear;
  });
});

function clearFilters() {
  searchQuery.value = "";
  filterBranch.value = "";
  filterMinCgpa.value = "";
  filterYear.value = "";
}

function getInitials(name) {
  if (!name) return "?";
  return name.split(" ").map(w => w[0]).join("").toUpperCase().slice(0, 2);
}

function getAvatarColor(name) {
  const colors = ["#4f46e5","#0891b2","#059669","#d97706","#dc2626","#7c3aed","#db2777"];
  if (!name) return colors[0];
  const i = name.charCodeAt(0) % colors.length;
  return colors[i];
}

function daysAgo(dateStr) {
  if (!dateStr) return "";
  const diff = Math.floor((new Date() - new Date(dateStr)) / (1000 * 60 * 60 * 24));
  if (diff === 0) return "today";
  if (diff === 1) return "1 day ago";
  return `${diff} days ago`;
}
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="mb-4">
      <h2 class="fw-bold mb-1">Placement Drives</h2>
      <p class="text-muted mb-0">Browse and apply for approved placement drives</p>
    </div>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="applyError" class="alert alert-warning d-flex justify-content-between align-items-center">
      {{ applyError }}
      <button class="btn-close btn-sm" @click="applyError = ''"></button>
    </div>
    <div v-if="applySuccess" class="alert alert-success d-flex justify-content-between align-items-center">
      {{ applySuccess }}
      <button class="btn-close btn-sm" @click="applySuccess = ''"></button>
    </div>

    <!-- Filters -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body p-4">
        <div class="row g-3 align-items-end">
          <div class="col-md-4">
            <label class="form-label fw-semibold small">🔍 Search</label>
            <input v-model="searchQuery" type="text" class="form-control" placeholder="Job title or company..." />
          </div>
          <div class="col-md-2">
            <label class="form-label fw-semibold small">Branch</label>
            <input v-model="filterBranch" type="text" class="form-control" placeholder="e.g. CSE" />
          </div>
          <div class="col-md-2">
            <label class="form-label fw-semibold small">My CGPA</label>
            <input v-model="filterMinCgpa" type="number" step="0.1" class="form-control" placeholder="e.g. 7.5" />
          </div>
          <div class="col-md-2">
            <label class="form-label fw-semibold small">Year</label>
            <select v-model="filterYear" class="form-select">
              <option value="">All</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>
          </div>
          <div class="col-md-2">
            <button class="btn btn-outline-secondary w-100" @click="clearFilters">Clear</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="filteredDrives.length === 0" class="text-center py-5 text-muted">
      <p class="fs-5">No drives found matching your filters.</p>
      <button class="btn btn-outline-secondary btn-sm" @click="clearFilters">Clear Filters</button>
    </div>

    <!-- Drive Cards -->
    <div v-else class="row g-4">
      <div class="col-md-6 col-lg-4" v-for="drive in filteredDrives" :key="drive.id">
        <div class="drive-card card border h-100">
          <div class="card-body p-4 d-flex flex-column">

            <!-- Top row: avatar + save-style badge -->
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div class="company-avatar rounded-circle d-flex align-items-center justify-content-center fw-bold text-white"
                :style="{ background: getAvatarColor(drive.company_name) }">
                {{ getInitials(drive.company_name) }}
              </div>
              <span v-if="hasApplied(drive.id)" class="applied-pill">✔ Applied</span>
              <span v-else class="open-pill">Open</span>
            </div>

            <!-- Company name + posted -->
            <p class="company-name mb-1">
              {{ drive.company_name }}
              <span class="posted-time ms-1" v-if="drive.application_deadline">
                · deadline {{ drive.application_deadline }}
              </span>
            </p>

            <!-- Job title -->
            <h5 class="job-title mb-3">{{ drive.job_title }}</h5>

            <!-- Tags -->
            <div class="d-flex flex-wrap gap-2 mb-3">
              <span class="tag">{{ drive.eligibility_branch }}</span>
              <span class="tag">Year {{ drive.eligible_year }}</span>
              <span class="tag">CGPA {{ drive.min_cgpa }}+</span>
            </div>

            <hr class="my-2" />

            <!-- Salary + Apply -->
            <div class="d-flex justify-content-between align-items-center mt-auto">
              <div>
                <p class="salary mb-0">{{ drive.salary || "Salary N/A" }}</p>
              </div>

              <button
                v-if="hasApplied(drive.id)"
                class="btn btn-applied btn-sm"
                disabled
              >Applied</button>

              <button
                v-else
                class="btn btn-apply btn-sm"
                :disabled="applyingId === drive.id"
                @click="applyToDrive(drive.id)"
              >
                <span v-if="applyingId === drive.id" class="spinner-border spinner-border-sm me-1"></span>
                Apply Now
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.drive-card {
  border-color: #e5e7eb !important;
  border-radius: 16px !important;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.drive-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 28px rgba(0,0,0,0.1) !important;
}

.company-avatar {
  width: 48px;
  height: 48px;
  font-size: 16px;
  flex-shrink: 0;
}

.company-name {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.posted-time {
  font-size: 12px;
  color: #9ca3af;
}

.job-title {
  font-size: 17px;
  font-weight: 700;
  color: #111827;
  line-height: 1.3;
}

.tag {
  font-size: 12px;
  font-weight: 500;
  background: #f3f4f6;
  color: #374151;
  padding: 3px 10px;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
}

.salary {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
}

.btn-apply {
  background: #111827;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 7px 18px;
  font-size: 13px;
  font-weight: 600;
}
.btn-apply:hover {
  background: #1f2937;
  color: #fff;
}

.btn-applied {
  background: #d1fae5;
  color: #065f46;
  border: none;
  border-radius: 8px;
  padding: 7px 18px;
  font-size: 13px;
  font-weight: 600;
}

.applied-pill {
  font-size: 12px;
  font-weight: 600;
  background: #d1fae5;
  color: #065f46;
  padding: 3px 10px;
  border-radius: 20px;
}

.open-pill {
  font-size: 12px;
  font-weight: 600;
  background: #eff6ff;
  color: #1d4ed8;
  padding: 3px 10px;
  border-radius: 20px;
}
</style>