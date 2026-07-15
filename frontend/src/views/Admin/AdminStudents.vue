<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const API_URL = import.meta.env.VITE_API_URL;

const students = ref([]);
const loading = ref(true);
const error = ref("");
const actionLoading = ref(null);

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("admin")) {
    router.push("/login");
    return;
  }

  await fetchStudents();
});

async function fetchStudents() {
  loading.value = true;
  error.value = "";

  try {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_URL}/api/admin/students`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) throw new Error();

    const data = await res.json();
    students.value = data;

  } catch {
    error.value = "Could not load students.";
  } finally {
    loading.value = false;
  }
}

async function blacklistStudent(id) {
  actionLoading.value = id;

  try {
    const token = localStorage.getItem("token");

    const res = await fetch(`http://localhost:5000/api/admin/user/${id}/deactivate`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) throw new Error();

    await fetchStudents();

  } catch {
    alert("Failed to blacklist student");
  } finally {
    actionLoading.value = null;
  }
}

function badgeClass(status) {
  return status === "Active"
    ? "badge bg-success"
    : "badge bg-danger";
}
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="d-flex justify-content-between mb-4">
      <div>
        <h2 class="fw-bold">Students</h2>
        <p class="text-muted">Manage all registered students</p>
      </div>

      <button class="btn btn-outline-secondary btn-sm" @click="router.push('/admin')" style="height: 30px;">
        ← Back to Dashboard
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border"></div>
    </div>

    <!-- Table -->
    <div v-else class="card shadow-sm border-0">
      <div class="card-body p-0">
        <div class="table-responsive">

          <table class="table table-hover align-middle mb-0">

            <thead class="table-light">
              <tr>
                <th class="px-4">#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(s, index) in students" :key="s.id">
                <td class="px-4">{{ index + 1 }}</td>
                <td class="fw-semibold">{{ s.name }}</td>
                <td class="text-muted">{{ s.email }}</td>

                <td>
                  <span :class="badgeClass(s.status)">
                    {{ s.status }}
                  </span>
                </td>

                <td class="text-center">
                  <button
                    class="btn btn-sm btn-danger"
                    :disabled="s.status === 'Blacklisted' || actionLoading === s.id"
                    @click="blacklistStudent(s.id)"
                  >
                    <span v-if="actionLoading === s.id" class="spinner-border spinner-border-sm"></span>
                    <span v-else>Blacklist</span>
                  </button>
                </td>

              </tr>
            </tbody>

          </table>

        </div>
      </div>
    </div>

  </div>
</template>