<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const company = ref(null);
const drives = ref([]);
const loading = ref(true);
const error = ref("");

const companyId = localStorage.getItem("company_id");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("manager")) {
    router.push("/login");
    return;
  }
  await fetchData();
});

async function fetchData() {
  loading.value = true;
  error.value = "";
  try {
    const token = localStorage.getItem("token");
    const headers = { Authorization: `Bearer ${token}` };

    const [profileRes, drivesRes] = await Promise.all([
      fetch(`${API_URL}/api/company/profile/${companyId}`, { headers }),
      fetch(`${API_URL}/api/company/drives/${companyId}`, { headers }),
    ]);

    if (profileRes.ok) company.value = await profileRes.json();
    if (drivesRes.ok) drives.value = await drivesRes.json();

  } catch (err) {
    error.value = "Could not load dashboard data.";
  } finally {
    loading.value = false;
  }
}

function totalApplicants() {
  return drives.value.reduce((sum, d) => sum + (d.applicant_count || 0), 0);
}

function statusBadgeClass(status) {
  if (status === "Approved") return "badge bg-success";
  if (status === "Rejected") return "badge bg-danger";
  return "badge bg-warning text-dark";
}
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <div class="mb-4">
      <h2 class="fw-bold mb-1">Dashboard</h2>
      <p class="text-muted mb-0">Welcome back! Here's your company overview.</p>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
    </div>

    <template v-else>

      <!-- Stat Cards -->
      <div class="row g-4 mb-4">
        <div class="col-sm-6 col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3 p-4">
              <div class="icon-box bg-primary bg-opacity-10 text-primary rounded-3 p-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 7V3H2v18h20V7H12zm-2 12H4v-2h6v2zm0-4H4v-2h6v2zm0-4H4V9h6v2zm0-4H4V5h6v2zm10 12h-8V9h8v10zm-2-8h-4v2h4v-2zm0 4h-4v2h4v-2z"/>
                </svg>
              </div>
              <div>
                <p class="text-muted small mb-1">Total Drives</p>
                <h3 class="fw-bold mb-0">{{ drives.length }}</h3>
              </div>
            </div>
          </div>
        </div>

        <div class="col-sm-6 col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3 p-4">
              <div class="icon-box bg-success bg-opacity-10 text-success rounded-3 p-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                </svg>
              </div>
              <div>
                <p class="text-muted small mb-1">Total Applicants</p>
                <h3 class="fw-bold mb-0">{{ totalApplicants() }}</h3>
              </div>
            </div>
          </div>
        </div>

        <div class="col-sm-6 col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3 p-4">
              <div class="icon-box bg-warning bg-opacity-10 text-warning rounded-3 p-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
              </div>
              <div>
                <p class="text-muted small mb-1">Approved Drives</p>
                <h3 class="fw-bold mb-0">{{ drives.filter(d => d.status === 'Approved').length }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Company Details -->
      <div class="card border-0 shadow-sm mb-4" v-if="company">
        <div class="card-body p-4">
          <h5 class="fw-bold mb-3">Company Details</h5>
          <div class="row g-3">
            <div class="col-md-4">
              <p class="text-muted small mb-1">Company Name</p>
              <p class="fw-semibold mb-0">{{ company.company_name || "—" }}</p>
            </div>
            <div class="col-md-4">
              <p class="text-muted small mb-1">HR Name</p>
              <p class="fw-semibold mb-0">{{ company.hr_name || "—" }}</p>
            </div>
            <div class="col-md-4">
              <p class="text-muted small mb-1">HR Email</p>
              <p class="fw-semibold mb-0">{{ company.hr_email || "—" }}</p>
            </div>
            <div class="col-md-4">
              <p class="text-muted small mb-1">HR Phone</p>
              <p class="fw-semibold mb-0">{{ company.hr_phone || "—" }}</p>
            </div>
            <div class="col-md-4">
              <p class="text-muted small mb-1">Website</p>
              <p class="fw-semibold mb-0">{{ company.website || "—" }}</p>
            </div>
            <div class="col-md-4">
              <p class="text-muted small mb-1">Approval Status</p>
              <span :class="statusBadgeClass(company.approval_status)">
                {{ company.approval_status || "Pending" }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Drives -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="fw-bold mb-0">Recent Drives</h5>
        <button class="btn btn-sm btn-primary" @click="router.push('/company-dashboard/drives')">View All →</button>
      </div>

      <div class="card border-0 shadow-sm">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="px-4 py-3">Job Title</th>
                  <th class="py-3">Deadline</th>
                  <th class="py-3">Applicants</th>
                  <th class="py-3">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="drives.length === 0">
                  <td colspan="4" class="text-center text-muted py-4">No drives created yet.</td>
                </tr>
                <tr v-for="drive in drives.slice(0, 5)" :key="drive.id">
                  <td class="px-4 fw-semibold">{{ drive.job_title }}</td>
                  <td class="text-muted">{{ drive.application_deadline || "—" }}</td>
                  <td><span class="badge bg-light text-dark border">{{ drive.applicant_count || 0 }}</span></td>
                  <td><span :class="statusBadgeClass(drive.status)">{{ drive.status || "Pending" }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-4">
        <h5 class="fw-bold mb-3">Quick Actions</h5>
        <div class="row g-3">
          <div class="col-6 col-md-3">
            <button class="btn btn-outline-primary w-100 py-3" @click="router.push('/company-dashboard/drives')">📋 My Drives</button>
          </div>
          <div class="col-6 col-md-3">
            <button class="btn btn-outline-success w-100 py-3" @click="router.push('/company-dashboard/drives')">➕ Create Drive</button>
          </div>
          <div class="col-6 col-md-3">
            <button class="btn btn-outline-warning w-100 py-3" @click="router.push('/company-dashboard/applications')">👥 Applications</button>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<style scoped>
.icon-box { flex-shrink: 0; }
.table th {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: #6c757d;
}
.table td { font-size: 14px; }
</style>