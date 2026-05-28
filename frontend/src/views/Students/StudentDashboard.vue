<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const student = ref(null);
const applications = ref([]);
const loading = ref(true);
const error = ref("");
const exporting = ref(false);

const studentId = localStorage.getItem("student_id");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("student")) { router.push("/login"); return; }
  await fetchData();
});

async function fetchData() {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const headers = { Authorization: `Bearer ${token}` };

    const [profileRes, appsRes] = await Promise.all([
      fetch(`http://localhost:5000/api/student/profile/${studentId}`, { headers }),
      fetch(`http://localhost:5000/api/student/applications/${studentId}`, { headers }),
    ]);

    if (profileRes.ok) student.value = await profileRes.json();
    if (appsRes.ok) applications.value = await appsRes.json();

  } catch {
    error.value = "Could not load dashboard data.";
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

const placed = (app) => app.status === "Selected";


async function exportCSV() {
  exporting.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/student/${studentId}/export-csv`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    alert(data.message); // "Export started! You'll receive an email shortly."
  } catch {
    alert("Export failed. Please try again.");
  } finally {
    exporting.value = false;
  }
}
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <div class="mb-4">
      <h2 class="fw-bold mb-1">Dashboard</h2>
      <p class="text-muted mb-0">Welcome back, <strong>{{ student?.name || "Student" }}</strong>!</p>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
    </div>

    <template v-else>

      <!-- Placement badge -->
      <div v-if="student?.is_placed" class="alert alert-success d-flex align-items-center gap-2 mb-4">
        🎉 <strong>Congratulations! You have been placed.</strong>
      </div>

      <!-- Stat Cards -->
      <div class="row g-4 mb-4">
        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3 p-4">
              <div class="icon-box bg-primary bg-opacity-10 text-primary rounded-3 p-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
                </svg>
              </div>
              <div>
                <p class="text-muted small mb-1">CGPA</p>
                <h3 class="fw-bold mb-0">{{ student?.cgpa || "—" }}</h3>
              </div>
            </div>
          </div>
        </div>

        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3 p-4">
              <div class="icon-box bg-success bg-opacity-10 text-success rounded-3 p-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm4 18H6V4h7v5h5v11z"/>
                </svg>
              </div>
              <div>
                <p class="text-muted small mb-1">Applications</p>
                <h3 class="fw-bold mb-0">{{ applications.length }}</h3>
              </div>
            </div>
          </div>
        </div>

        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3 p-4">
              <div class="icon-box bg-info bg-opacity-10 text-info rounded-3 p-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <div>
                <p class="text-muted small mb-1">Shortlisted</p>
                <h3 class="fw-bold mb-0">{{ applications.filter(a => a.status === 'Shortlisted').length }}</h3>
              </div>
            </div>
          </div>
        </div>

        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3 p-4">
              <div class="icon-box bg-warning bg-opacity-10 text-warning rounded-3 p-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
              </div>
              <div>
                <p class="text-muted small mb-1">Placement</p>
                <h3 class="fw-bold mb-0">{{ student?.is_placed ? "Placed ✓" : "Active" }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Student Info Card -->
      <div class="card border-0 shadow-sm mb-4" v-if="student">
        <div class="card-body p-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-bold mb-0">My Profile</h5>
            <button class="btn btn-sm btn-outline-primary" @click="router.push('/student-dashboard/profile')">Edit Profile</button>
          </div>
          <div class="row g-3">
            <div class="col-md-3">
              <p class="text-muted small mb-1">Name</p>
              <p class="fw-semibold mb-0">{{ student.name }}</p>
            </div>
            <div class="col-md-3">
              <p class="text-muted small mb-1">Roll No</p>
              <p class="fw-semibold mb-0">{{ student.roll_no }}</p>
            </div>
            <div class="col-md-3">
              <p class="text-muted small mb-1">Branch</p>
              <p class="fw-semibold mb-0">{{ student.branch }}</p>
            </div>
            <div class="col-md-3">
              <p class="text-muted small mb-1">Year</p>
              <p class="fw-semibold mb-0">{{ student.year }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Applications -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="fw-bold mb-0">Recent Applications</h5>
        <button class="btn btn-sm btn-primary" @click="router.push('/student-dashboard/applications')">View All →</button>
      </div>

      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="px-4 py-3">Company</th>
                  <th class="py-3">Job Title</th>
                  <th class="py-3">Applied On</th>
                  <th class="py-3">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="applications.length === 0">
                  <td colspan="4" class="text-center text-muted py-4">No applications yet.</td>
                </tr>
                <tr v-for="app in applications.slice(0, 5)" :key="app.id">
                  <td class="px-4 fw-semibold">{{ app.company_name }}</td>
                  <td class="text-muted">{{ app.job_title }}</td>
                  <td class="text-muted">{{ app.applied_on || "—" }}</td>
                  <td><span :class="statusBadgeClass(app.status)">{{ app.status }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <h5 class="fw-bold mb-3">Quick Actions</h5>
      <div class="row g-3">
        <div class="col-6 col-md-3">
          <button class="btn btn-outline-success w-100 py-3" @click="router.push('/student-dashboard/drives')">🏢 Browse Drives</button>
        </div>
        <div class="col-6 col-md-3">
          <button class="btn btn-outline-primary w-100 py-3" @click="router.push('/student-dashboard/applications')">📋 My Applications</button>
        </div>
        <div class="col-6 col-md-3">
          <button class="btn btn-outline-secondary w-100 py-3" @click="router.push('/student-dashboard/profile')">👤 Edit Profile</button>
        </div>

        <div class="col-6 col-md-3">
    <button 
      class="btn btn-outline-warning w-100 py-3" 
      @click="exportCSV"
      :disabled="exporting"
    >
      {{ exporting ? '⏳ Exporting...' : '📥 Export History' }}
    </button>
  </div>
      </div>

    </template>
  </div>
</template>

<style scoped>
.icon-box { flex-shrink: 0; }
.table th { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px; color: #6c757d; }
.table td { font-size: 14px; }
</style>