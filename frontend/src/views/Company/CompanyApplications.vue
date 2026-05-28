<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const drives = ref([]);
const applicants = ref([]);
const selectedDriveId = ref(route.query.drive_id || "");
const loadingDrives = ref(true);
const loadingApplicants = ref(false);
const error = ref("");
const actionLoading = ref(null);
const actionError = ref("");

const companyId = localStorage.getItem("company_id");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("manager")) { router.push("/login"); return; }
  await fetchDrives();
  if (selectedDriveId.value) await fetchApplicants(selectedDriveId.value);
});

async function fetchDrives() {
  loadingDrives.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/company/drives/${companyId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error();
    drives.value = await res.json();
  } catch {
    error.value = "Could not load drives.";
  } finally {
    loadingDrives.value = false;
  }
}

async function fetchApplicants(driveId) {
  if (!driveId) return;
  loadingApplicants.value = true;
  applicants.value = [];
  error.value = "";
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/company/applicants/${driveId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error();
    applicants.value = await res.json();
  } catch {
    error.value = "Could not load applicants.";
  } finally {
    loadingApplicants.value = false;
  }
}

async function updateStatus(applicationId, status) {
  // ✅ Use string key to avoid number+string concat issues
  const key = `${applicationId}-${status}`;
  actionLoading.value = key;
  actionError.value = "";

  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/company/application/${applicationId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ status }),
    });

    const data = await res.json();

    if (!res.ok) {
      actionError.value = data.message || "Failed to update status.";
      return;
    }

    // Update locally without re-fetching
    const app = applicants.value.find(a => a.id === applicationId);
    if (app) app.status = status;

  } catch {
    actionError.value = "Server error. Please try again.";
  } finally {
    actionLoading.value = null;
  }
}

function onDriveChange() {
  fetchApplicants(selectedDriveId.value);
}

function statusBadgeClass(status) {
  if (status === "Selected")   return "badge bg-success";
  if (status === "Rejected")   return "badge bg-danger";
  if (status === "Shortlisted") return "badge bg-info text-dark";
  return "badge bg-secondary";
}

function isLoading(appId, status) {
  return actionLoading.value === `${appId}-${status}`;
}

const selectedDriveName = computed(() => {
  const d = drives.value.find(d => String(d.id) === String(selectedDriveId.value));
  return d ? d.job_title : "";
});

// Summary counts
const summary = computed(() => ({
  total:       applicants.value.length,
  shortlisted: applicants.value.filter(a => a.status === "Shortlisted").length,
  selected:    applicants.value.filter(a => a.status === "Selected").length,
  rejected:    applicants.value.filter(a => a.status === "Rejected").length,
}));
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="d-flex align-items-center justify-content-between mb-4">
      <div>
        <h2 class="fw-bold mb-1">Student Applications</h2>
        <p class="text-muted mb-0">View and manage applicants per drive</p>
      </div>
      <button class="btn btn-outline-secondary btn-sm" @click="router.push('/company-dashboard')">
        ← Back to Dashboard
      </button>
    </div>

    <!-- Errors -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="actionError" class="alert alert-warning d-flex justify-content-between align-items-center">
      {{ actionError }}
      <button class="btn-close btn-sm" @click="actionError = ''"></button>
    </div>

    <!-- Drive Selector -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body p-4">
        <label class="form-label fw-semibold">Select Placement Drive</label>
        <select
          v-model="selectedDriveId"
          class="form-select"
          style="max-width: 420px;"
          @change="onDriveChange"
          :disabled="loadingDrives"
        >
          <option value="">-- Choose a drive --</option>
          <option v-for="drive in drives" :key="drive.id" :value="drive.id">
            {{ drive.job_title }} — {{ drive.status }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading applicants -->
    <div v-if="loadingApplicants" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
      <p class="text-muted mt-2">Loading applicants...</p>
    </div>

    <!-- No drive selected -->
    <div v-else-if="!selectedDriveId" class="text-center py-5 text-muted">
      <p class="fs-5">Select a drive above to view applicants.</p>
    </div>

    <!-- Empty -->
    <div v-else-if="applicants.length === 0" class="text-center py-5 text-muted">
      <p class="fs-5">No applications received for <strong>{{ selectedDriveName }}</strong> yet.</p>
    </div>

    <!-- Applicants -->
    <template v-else>

      <!-- Summary Cards -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0">{{ summary.total }}</h4>
            <p class="text-muted small mb-0">Total</p>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0 text-info">{{ summary.shortlisted }}</h4>
            <p class="text-muted small mb-0">Shortlisted</p>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0 text-success">{{ summary.selected }}</h4>
            <p class="text-muted small mb-0">Selected</p>
          </div>
        </div>
        <div class="col-6 col-md-3">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0 text-danger">{{ summary.rejected }}</h4>
            <p class="text-muted small mb-0">Rejected</p>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="d-flex align-items-center justify-content-between mb-3">
        <h5 class="fw-bold mb-0">
          {{ selectedDriveName }}
          <span class="badge bg-light text-dark border ms-2">{{ summary.total }} applicants</span>
        </h5>
      </div>

      <div class="card border-0 shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="px-4 py-3">#</th>
                  <th class="py-3">Student Name</th>
                  <th class="py-3">Roll No</th>
                  <th class="py-3">Branch</th>
                  <th class="py-3">CGPA</th>
                  <th class="py-3">Resume</th>
                  <th class="py-3">Status</th>
                  <th class="py-3 text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(app, index) in applicants" :key="app.id">
                  <td class="px-4 text-muted">{{ index + 1 }}</td>
                  <td class="fw-semibold">{{ app.student_name }}</td>
                  <td class="text-muted">{{ app.roll_no || "—" }}</td>
                  <td class="text-muted">{{ app.branch || "—" }}</td>
                  <td><span class="badge bg-light text-dark border">{{ app.cgpa || "—" }}</span></td>
                  <td>
                    <a
                      v-if="app.resume_path"
                      :href="`http://localhost:5000/${app.resume_path}`"
                      target="_blank"
                      class="btn btn-sm btn-outline-primary"
                    >
                      View Resume
                    </a>
                    <span v-else class="text-muted">No resume</span>
                  </td>
                  <td><span :class="statusBadgeClass(app.status)">{{ app.status || "Applied" }}</span></td>
                  <td class="text-center">
                    <div class="d-flex justify-content-center gap-1 flex-wrap">
                      <!-- Shortlist -->
                      <button
                        class="btn btn-sm btn-outline-info"
                        :disabled="app.status === 'Shortlisted' || app.status === 'Selected' || isLoading(app.id, 'Shortlisted')"
                        @click="updateStatus(app.id, 'Shortlisted')"
                      >
                        <span v-if="isLoading(app.id, 'Shortlisted')" class="spinner-border spinner-border-sm"></span>
                        <span v-else>⭐ Shortlist</span>
                      </button>

                      <!-- Select -->
                      <button
                        class="btn btn-sm btn-outline-success"
                        :disabled="app.status === 'Selected' || isLoading(app.id, 'Selected')"
                        @click="updateStatus(app.id, 'Selected')"
                      >
                        <span v-if="isLoading(app.id, 'Selected')" class="spinner-border spinner-border-sm"></span>
                        <span v-else>✔ Select</span>
                      </button>

                      <!-- Reject -->
                      <button
                        class="btn btn-sm btn-outline-danger"
                        :disabled="app.status === 'Selected' || app.status === 'Rejected' || isLoading(app.id, 'Rejected')"
                        @click="updateStatus(app.id, 'Rejected')"
                      >
                        <span v-if="isLoading(app.id, 'Rejected')" class="spinner-border spinner-border-sm"></span>
                        <span v-else>✖ Reject</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<style scoped>
.table th {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: #6c757d;
}
.table td { font-size: 14px; }
</style>