<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const applications = ref([]);
const loading = ref(true);
const error = ref("");
const activeTab = ref("all"); // all | active | history

const studentId = localStorage.getItem("student_id");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("student")) { router.push("/login"); return; }
  await fetchApplications();
});

async function fetchApplications() {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_URL}/api/student/applications/${studentId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error();
    applications.value = await res.json();
  } catch {
    error.value = "Could not load applications.";
  } finally {
    loading.value = false;
  }
}

function statusBadgeClass(status) {
  if (status === "Selected")    return "badge bg-success";
  if (status === "Rejected")    return "badge bg-danger";
  if (status === "Shortlisted") return "badge bg-info text-dark";
  return "badge bg-secondary";
}

const filteredApps = computed(() => {
  if (activeTab.value === "active")
    return applications.value.filter(a => a.status === "Applied" || a.status === "Shortlisted");
  if (activeTab.value === "history")
    return applications.value.filter(a => a.status === "Selected" || a.status === "Rejected");
  return applications.value;
});

const summary = computed(() => ({
  total:       applications.value.length,
  applied:     applications.value.filter(a => a.status === "Applied").length,
  shortlisted: applications.value.filter(a => a.status === "Shortlisted").length,
  selected:    applications.value.filter(a => a.status === "Selected").length,
  rejected:    applications.value.filter(a => a.status === "Rejected").length,
}));
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-1">My Applications</h2>
        <p class="text-muted mb-0">Track your placement application status</p>
      </div>
      <button class="btn btn-outline-success btn-sm" @click="router.push('/student-dashboard/drives')">
        ➕ Apply to Drive
      </button>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
    </div>

    <template v-else>

      <!-- Summary Cards -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0">{{ summary.total }}</h4>
            <p class="text-muted small mb-0">Total</p>
          </div>
        </div>
        <div class="col-6 col-md">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0 text-secondary">{{ summary.applied }}</h4>
            <p class="text-muted small mb-0">Applied</p>
          </div>
        </div>
        <div class="col-6 col-md">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0 text-info">{{ summary.shortlisted }}</h4>
            <p class="text-muted small mb-0">Shortlisted</p>
          </div>
        </div>
        <div class="col-6 col-md">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0 text-success">{{ summary.selected }}</h4>
            <p class="text-muted small mb-0">Selected</p>
          </div>
        </div>
        <div class="col-6 col-md">
          <div class="card border-0 shadow-sm text-center p-3">
            <h4 class="fw-bold mb-0 text-danger">{{ summary.rejected }}</h4>
            <p class="text-muted small mb-0">Rejected</p>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <ul class="nav nav-tabs mb-3">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'all' }"
            style="cursor:pointer" @click="activeTab = 'all'">
            All <span class="badge bg-secondary ms-1">{{ summary.total }}</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'active' }"
            style="cursor:pointer" @click="activeTab = 'active'">
            Active <span class="badge bg-info ms-1">{{ summary.applied + summary.shortlisted }}</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'history' }"
            style="cursor:pointer" @click="activeTab = 'history'">
            History <span class="badge bg-success ms-1">{{ summary.selected + summary.rejected }}</span>
          </a>
        </li>
      </ul>

      <!-- Empty -->
      <div v-if="filteredApps.length === 0" class="text-center py-5 text-muted">
        <p class="fs-5">No applications in this category.</p>
        <button class="btn btn-outline-success btn-sm" @click="router.push('/student-dashboard/drives')">
          Browse Drives
        </button>
      </div>

      <!-- Table -->
      <div v-else class="card border-0 shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="px-4 py-3">#</th>
                  <th class="py-3">Company</th>
                  <th class="py-3">Job Title</th>
                  <th class="py-3">Salary</th>
                  <th class="py-3">Applied On</th>
                  <th class="py-3">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(app, index) in filteredApps" :key="app.id">
                  <td class="px-4 text-muted">{{ index + 1 }}</td>
                  <td class="fw-semibold">{{ app.company_name }}</td>
                  <td class="text-muted">{{ app.job_title }}</td>
                  <td class="text-muted">{{ app.salary || "—" }}</td>
                  <td class="text-muted">{{ app.applied_on || "—" }}</td>
                  <td>
                    <span :class="statusBadgeClass(app.status)">{{ app.status }}</span>
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
.table th { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px; color: #6c757d; }
.table td { font-size: 14px; }
.nav-link { color: #6c757d; }
.nav-link.active { color: #1a6b4a; font-weight: 600; border-bottom-color: #1a6b4a; }
</style>