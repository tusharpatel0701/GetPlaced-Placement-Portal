<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;

const router = useRouter();
const applications = ref([]);
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("admin")) {
    router.push("/login");
    return;
  }
  await fetchApplications();
});

async function fetchApplications() {
  loading.value = true;
  error.value = "";

  try {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_URL}/api/admin/applications`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    applications.value = data;
  } catch (err) {
    error.value = "Could not load applications.";
  } finally {
    loading.value = false;
  }
}

function statusBadge(status) {
  if (status === "Accepted") return "badge bg-success";
  if (status === "Rejected") return "badge bg-danger";
  return "badge bg-warning text-dark";
}
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold">Applications</h2>
        <p class="text-muted mb-0">All student applications</p>
      </div>

      <button class="btn btn-outline-secondary btn-sm" @click="router.push('/admin')">
        ← Back to Dashboard
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="applications.length === 0" class="text-center text-muted py-5">
      No applications found
    </div>

    <!-- Table -->
    <div v-else class="card shadow-sm border-0">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover mb-0 align-middle">

            <thead class="table-light">
              <tr>
                <th class="px-4">#</th>
                <th>Student</th>
                <th>Company</th>
                <th>Job</th>
                <th>Status</th>
                <th>Applied On</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(app, index) in applications" :key="app.id">
                <td class="px-4">{{ index + 1 }}</td>
                <td>{{ app.student_name }}</td>
                <td>{{ app.company }}</td>
                <td>{{ app.job_title }}</td>
                <td>
                  <span :class="statusBadge(app.status)">
                    {{ app.status || "Pending" }}
                  </span>
                </td>
                <td>{{ app.applied_on }}</td>
              </tr>
            </tbody>

          </table>
        </div>
      </div>
    </div>

  </div>
</template>