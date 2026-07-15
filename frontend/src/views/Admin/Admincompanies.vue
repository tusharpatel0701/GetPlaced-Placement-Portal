<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const companies = ref([]);
const loading = ref(true);
const error = ref("");
const actionLoading = ref(null);
const actionError = ref("");

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("admin")) {
    router.push("/login");
    return;
  }
  await fetchCompanies();
});

async function fetchCompanies() {
  loading.value = true;
  error.value = "";
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_URL}/api/admin/companies`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch");
    const data = await res.json();
    companies.value = data;
  } catch (err) {
    error.value = "Could not load companies.";
  } finally {
    loading.value = false;
  }
}

async function handleAction(companyId, action) {
  actionLoading.value = companyId + action;
  actionError.value = "";
  try {
    const token = localStorage.getItem("token");

    // ✅ Matches your backend: AdminCompanyApproval at /api/admin/company/<company_id>
    const res = await fetch(`http://localhost:5000/api/admin/company/${companyId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ action }),  // sends { "action": "approve" } or { "action": "reject" }
    });

    const data = await res.json();

    if (!res.ok) {
      actionError.value = data.message || "Action failed.";
      return;
    }

    // Refresh list after success
    await fetchCompanies();

  } catch (err) {
    actionError.value = "Server error. Please try again.";
  } finally {
    actionLoading.value = null;
  }
}

function statusBadgeClass(status) {
  if (status === "Approved") return "badge bg-success";
  if (status === "Rejected") return "badge bg-danger";
  return "badge bg-warning text-dark";
}
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="d-flex align-items-center justify-content-between mb-4">
      <div>
        <h2 class="fw-bold mb-1">Companies</h2>
        <p class="text-muted mb-0">Manage and approve registered companies</p>
      </div>
      <button class="btn btn-outline-secondary btn-sm" @click="router.push('/admin')">
        ← Back to Dashboard
      </button>
    </div>

    <!-- Fetch Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Action Error -->
    <div v-if="actionError" class="alert alert-warning d-flex justify-content-between align-items-center">
      {{ actionError }}
      <button class="btn-close btn-sm" @click="actionError = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
      <p class="text-muted mt-2">Loading companies...</p>
    </div>

    <!-- Empty -->
    <div v-else-if="companies.length === 0" class="text-center py-5 text-muted">
      <p class="fs-5">No companies registered yet.</p>
    </div>

    <!-- Table -->
    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th class="px-4 py-3">#</th>
                <th class="py-3">Company Name</th>
                <th class="py-3">HR Email</th>
                <th class="py-3">Status</th>
                <th class="py-3 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(company, index) in companies" :key="company.id">
                <td class="px-4 text-muted">{{ index + 1 }}</td>
                <td class="fw-semibold">{{ company.company_name }}</td>
                <td class="text-muted">{{ company.hr_email }}</td>
                <td>
                  <span :class="statusBadgeClass(company.approval_status)">
                    {{ company.approval_status || "Pending" }}
                  </span>
                </td>
                <td class="text-center">
                  <div class="d-flex justify-content-center gap-2">
                    <button
                      class="btn btn-sm btn-success"
                      :disabled="company.approval_status === 'Approved' || actionLoading === company.id + 'approve'"
                      @click="handleAction(company.id, 'approve')"
                    >
                      <span v-if="actionLoading === company.id + 'approve'" class="spinner-border spinner-border-sm"></span>
                      <span v-else>Approve</span>
                    </button>
                    <button
                      class="btn btn-sm btn-danger"
                      :disabled="company.approval_status === 'Rejected' || actionLoading === company.id + 'reject'"
                      @click="handleAction(company.id, 'reject')"
                    >
                      <span v-if="actionLoading === company.id + 'reject'" class="spinner-border spinner-border-sm"></span>
                      <span v-else>Reject</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

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
.table td {
  font-size: 14px;
}
</style>