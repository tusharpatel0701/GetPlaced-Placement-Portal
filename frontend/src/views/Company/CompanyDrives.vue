<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;

const router = useRouter();
const drives = ref([]);
const company = ref(null);
const loading = ref(true);
const error = ref("");
const showForm = ref(false);
const submitting = ref(false);
const formError = ref("");
const formSuccess = ref("");

const companyId = localStorage.getItem("company_id");

const isApproved = computed(() => company.value?.approval_status === "Approved");

// ✅ All fields matching PlacementDrive model (nullable=False fields are required)
const form = ref({
  job_title: "",
  job_description: "",
  eligibility_branch: "",
  min_cgpa: "",
  eligible_year: "",
  salary: "",
  application_deadline: "",
});

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("manager")) { router.push("/login"); return; }
  await Promise.all([fetchCompany(), fetchDrives()]);
});

async function fetchCompany() {
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_URL}/api/company/profile/${companyId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) company.value = await res.json();
  } catch {}
}

async function fetchDrives() {
  loading.value = true;
  error.value = "";
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
    loading.value = false;
  }
}

async function createDrive() {
  formError.value = "";
  formSuccess.value = "";

  // Validate all required fields
  if (!form.value.job_title || !form.value.job_description ||
      !form.value.eligibility_branch || !form.value.min_cgpa ||
      !form.value.eligible_year || !form.value.application_deadline) {
    formError.value = "Please fill all required fields.";
    return;
  }

  submitting.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await fetch("http://localhost:5000/api/company/create-drive", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        company_id: parseInt(companyId),
        job_title: form.value.job_title,
        job_description: form.value.job_description,
        eligibility_branch: form.value.eligibility_branch,
        min_cgpa: parseFloat(form.value.min_cgpa),
        eligible_year: parseInt(form.value.eligible_year),
        salary: form.value.salary,
        application_deadline: form.value.application_deadline,
      }),
    });

    const data = await res.json();
    if (!res.ok) { formError.value = data.message || "Failed to create drive."; return; }

    formSuccess.value = "Drive created successfully! Awaiting admin approval.";
    form.value = { job_title: "", job_description: "", eligibility_branch: "", min_cgpa: "", eligible_year: "", salary: "", application_deadline: "" };
    showForm.value = false;
    await fetchDrives();
  } catch {
    formError.value = "Server error. Try again.";
  } finally {
    submitting.value = false;
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
        <h2 class="fw-bold mb-1">My Placement Drives</h2>
        <p class="text-muted mb-0">Manage your placement drives</p>
      </div>

      <div v-if="!isApproved" title="Your company must be approved by admin before creating drives.">
        <button class="btn btn-primary btn-sm" disabled>➕ Create Drive</button>
        <p class="text-danger small mt-1 mb-0 text-end">⚠ Awaiting admin approval</p>
      </div>
      <button v-else class="btn btn-primary btn-sm" @click="showForm = !showForm">
        {{ showForm ? '✖ Cancel' : '➕ Create Drive' }}
      </button>
    </div>

    <!-- Not approved banner -->
    <div v-if="!isApproved && company" class="alert alert-warning d-flex align-items-center gap-2 mb-4">
      <span>⏳</span>
      <span>Your company is <strong>{{ company.approval_status || "Pending" }}</strong>. You can create drives only after admin approves your account.</span>
    </div>

    <!-- Success -->
    <div v-if="formSuccess" class="alert alert-success">{{ formSuccess }}</div>

    <!-- Create Drive Form -->
    <div v-if="showForm && isApproved" class="card border-0 shadow-sm mb-4">
      <div class="card-body p-4">
        <h5 class="fw-bold mb-1">Create New Drive</h5>
        <p class="text-muted small mb-3">Fields marked <span class="text-danger">*</span> are required</p>

        <div v-if="formError" class="alert alert-danger">{{ formError }}</div>

        <div class="row g-3">
          <!-- Job Title -->
          <div class="col-md-6">
            <label class="form-label">Job Title <span class="text-danger">*</span></label>
            <input v-model="form.job_title" type="text" class="form-control" placeholder="e.g. Software Engineer" />
          </div>

          <!-- Salary -->
          <div class="col-md-6">
            <label class="form-label">Salary Package</label>
            <input v-model="form.salary" type="text" class="form-control" placeholder="e.g. 6 LPA" />
          </div>

          <!-- Eligibility Branch -->
          <div class="col-md-4">
            <label class="form-label">Eligible Branch <span class="text-danger">*</span></label>
            <input v-model="form.eligibility_branch" type="text" class="form-control" placeholder="e.g. CSE, IT, ECE" />
          </div>

          <!-- Min CGPA -->
          <div class="col-md-4">
            <label class="form-label">Minimum CGPA <span class="text-danger">*</span></label>
            <input v-model="form.min_cgpa" type="number" step="0.1" min="0" max="10" class="form-control" placeholder="e.g. 7.0" />
          </div>

          <!-- Eligible Year -->
          <div class="col-md-4">
            <label class="form-label">Eligible Year <span class="text-danger">*</span></label>
            <select v-model="form.eligible_year" class="form-select">
              <option value="">-- Select Year --</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>
          </div>

          <!-- Application Deadline -->
          <div class="col-md-6">
            <label class="form-label">Application Deadline <span class="text-danger">*</span></label>
            <input v-model="form.application_deadline" type="date" class="form-control" />
          </div>

          <!-- Job Description -->
          <div class="col-12">
            <label class="form-label">Job Description <span class="text-danger">*</span></label>
            <textarea v-model="form.job_description" class="form-control" rows="3" placeholder="Describe the role, responsibilities, and requirements..."></textarea>
          </div>

          <div class="col-12">
            <button class="btn btn-primary px-4" :disabled="submitting" @click="createDrive">
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
              Submit Drive
            </button>
            <button class="btn btn-outline-secondary px-4 ms-2" @click="showForm = false">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="drives.length === 0" class="text-center py-5 text-muted">
      <p class="fs-5">No drives yet.</p>
      <p class="small">{{ isApproved ? 'Click "Create Drive" to post your first placement drive.' : 'You can create drives once your account is approved.' }}</p>
    </div>

    <!-- Drives Table -->
    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th class="px-4 py-3">#</th>
                <th class="py-3">Job Title</th>
                <th class="py-3">Branch</th>
                <th class="py-3">Min CGPA</th>
                <th class="py-3">Deadline</th>
                <th class="py-3">Applicants</th>
                <th class="py-3">Status</th>
                <th class="py-3 text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(drive, index) in drives" :key="drive.id">
                <td class="px-4 text-muted">{{ index + 1 }}</td>
                <td class="fw-semibold">{{ drive.job_title }}</td>
                <td class="text-muted">{{ drive.eligibility_branch || "—" }}</td>
                <td class="text-muted">{{ drive.min_cgpa || "—" }}</td>
                <td class="text-muted">{{ drive.application_deadline || "—" }}</td>
                <td><span class="badge bg-light text-dark border">{{ drive.applicant_count || 0 }}</span></td>
                <td><span :class="statusBadgeClass(drive.status)">{{ drive.status || "Pending" }}</span></td>
                <td class="text-center">
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="router.push(`/company-dashboard/applications?drive_id=${drive.id}`)"
                  >
                    View Applicants
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