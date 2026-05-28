<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const stats = ref({ total_students: 0, total_companies: 0, total_drives: 0 });
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("admin")) {
    router.push("/login");
    return;
  }

  try {
    const token = localStorage.getItem("token");
    const res = await fetch("http://localhost:5000/api/admin/dashboard", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) throw new Error("Failed to fetch");

    const data = await res.json();
    stats.value = data;
  } catch (err) {
    error.value = "Could not load dashboard stats. Please try again.";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Heading -->
    <div class="mb-4">
      <h2 class="fw-bold mb-1">Dashboard</h2>
      <p class="text-muted mb-0">Welcome back! Here's a quick overview.</p>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Stat Cards -->
    <div class="row g-4 mb-5">

      <div class="col-sm-6 col-lg-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body d-flex align-items-center gap-3 p-4">
            <div class="icon-box bg-primary bg-opacity-10 text-primary rounded-3 p-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 24 24">
                <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
              </svg>
            </div>
            <div>
              <p class="text-muted small mb-1">Total Students</p>
              <h3 class="fw-bold mb-0">
                <span v-if="loading" class="placeholder-box"></span>
                <span v-else>{{ stats.total_students }}</span>
              </h3>
            </div>
          </div>
        </div>
      </div>

      <div class="col-sm-6 col-lg-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body d-flex align-items-center gap-3 p-4">
            <div class="icon-box bg-success bg-opacity-10 text-success rounded-3 p-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 7V3H2v18h20V7H12zm-2 12H4v-2h6v2zm0-4H4v-2h6v2zm0-4H4V9h6v2zm0-4H4V5h6v2zm10 12h-8V9h8v10zm-2-8h-4v2h4v-2zm0 4h-4v2h4v-2z"/>
              </svg>
            </div>
            <div>
              <p class="text-muted small mb-1">Total Companies</p>
              <h3 class="fw-bold mb-0">
                <span v-if="loading" class="placeholder-box"></span>
                <span v-else>{{ stats.total_companies }}</span>
              </h3>
            </div>
          </div>
        </div>
      </div>

      <div class="col-sm-6 col-lg-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body d-flex align-items-center gap-3 p-4">
            <div class="icon-box bg-warning bg-opacity-10 text-warning rounded-3 p-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z"/>
              </svg>
            </div>
            <div>
              <p class="text-muted small mb-1">Placement Drives</p>
              <h3 class="fw-bold mb-0">
                <span v-if="loading" class="placeholder-box"></span>
                <span v-else>{{ stats.total_drives }}</span>
              </h3>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Quick Navigation -->
    <div class="mb-3">
      <h5 class="fw-semibold">Manage</h5>
    </div>
    <div class="row g-3">
      <div class="col-6 col-md-3">
        <button class="btn btn-outline-primary w-100 py-3" @click="$router.push('/admin/students')">
          👨‍🎓 Students
        </button>
      </div>
      <div class="col-6 col-md-3">
        <button class="btn btn-outline-success w-100 py-3" @click="$router.push('/admin/companies')">
          🏢 Companies
        </button>
      </div>
      <div class="col-6 col-md-3">
        <button class="btn btn-outline-warning w-100 py-3" @click="$router.push('/admin/drives')">
          📅 Drives
        </button>
      </div>
      <div class="col-6 col-md-3">
        <button class="btn btn-outline-secondary w-100 py-3" @click="$router.push('/admin/applications')">
          📋 Applications
        </button>
      </div>
    </div>

  </div>
</template>

<style scoped>
.icon-box { flex-shrink: 0; }
.placeholder-box {
  display: inline-block;
  width: 60px;
  height: 1.8rem;
  border-radius: 4px;
  background: #dee2e6;
  animation: glow 1.4s ease-in-out infinite;
}
@keyframes glow { 50% { opacity: 0.4; } }
</style>