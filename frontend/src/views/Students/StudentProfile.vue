<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();
const student = ref(null);
const loading = ref(true);
const saving = ref(false);
const uploadingResume = ref(false);
const error = ref("");
const saveSuccess = ref("");
const resumeSuccess = ref("");
const resumeError = ref("");

const studentId = localStorage.getItem("student_id");

const form = ref({
  name: "", roll_no: "", branch: "",
  cgpa: "", year: "", phone: "",
});

onMounted(async () => {
  const roles = JSON.parse(localStorage.getItem("roles") || "[]");
  if (!roles.includes("student")) { router.push("/login"); return; }
  await fetchProfile();
});

async function fetchProfile() {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_URL}/api/student/profile/${studentId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error();
    student.value = await res.json();
    // Populate form
    form.value = {
      name:     student.value.name || "",
      roll_no:  student.value.roll_no || "",
      branch:   student.value.branch || "",
      cgpa:     student.value.cgpa || "",
      year:     student.value.year || "",
      phone:    student.value.phone || "",
    };
  } catch {
    error.value = "Could not load profile.";
  } finally {
    loading.value = false;
  }
}

async function saveProfile() {
  saving.value = true;
  saveSuccess.value = "";
  error.value = "";
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/student/profile/${studentId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(form.value),
    });
    const data = await res.json();
    if (!res.ok) { error.value = data.message || "Failed to save."; return; }
    saveSuccess.value = "Profile updated successfully!";
    await fetchProfile();
  } catch {
    error.value = "Server error. Try again.";
  } finally {
    saving.value = false;
  }
}

async function uploadResume(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (file.type !== "application/pdf") {
    resumeError.value = "Only PDF files are allowed.";
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    resumeError.value = "File size must be under 5MB.";
    return;
  }

  resumeError.value = "";
  resumeSuccess.value = "";
  uploadingResume.value = true;

  try {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("resume", file);

    const res = await fetch(`http://localhost:5000/api/student/resume/${studentId}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) { resumeError.value = data.message || "Upload failed."; return; }
    resumeSuccess.value = "Resume uploaded successfully!";
    await fetchProfile();
  } catch {
    resumeError.value = "Server error during upload.";
  } finally {
    uploadingResume.value = false;
  }
}
</script>

<template>
  <div class="container-fluid px-4 py-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-1">My Profile</h2>
        <p class="text-muted mb-0">Update your personal details and resume</p>
      </div>
      <button class="btn btn-outline-secondary btn-sm" @click="router.push('/student-dashboard')">
        ← Back to Dashboard
      </button>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-secondary" role="status"></div>
    </div>

    <template v-else>

      <div class="row g-4">

        <!-- Edit Profile Form -->
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
              <h5 class="fw-bold mb-4">Personal Information</h5>

              <div v-if="saveSuccess" class="alert alert-success">{{ saveSuccess }}</div>

              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Full Name</label>
                  <input v-model="form.name" type="text" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Roll No</label>
                  <input v-model="form.roll_no" type="text" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Branch</label>
                  <input v-model="form.branch" type="text" class="form-control" placeholder="e.g. CSE" />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Phone</label>
                  <input v-model="form.phone" type="text" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label">CGPA</label>
                  <input v-model="form.cgpa" type="number" step="0.01" min="0" max="10" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Year</label>
                  <select v-model="form.year" class="form-select">
                    <option value="">-- Select --</option>
                    <option value="1">1st Year</option>
                    <option value="2">2nd Year</option>
                    <option value="3">3rd Year</option>
                    <option value="4">4th Year</option>
                  </select>
                </div>
                <div class="col-12">
                  <button class="btn btn-primary px-4" :disabled="saving" @click="saveProfile">
                    <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Resume & Info -->
        <div class="col-lg-4 d-flex flex-column gap-4">

          <!-- Placement Status -->
          <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
              <h6 class="fw-bold mb-3">Placement Status</h6>
              <div class="d-flex align-items-center gap-2">
                <span v-if="student?.is_placed" class="badge bg-success fs-6 px-3 py-2">✔ Placed</span>
                <span v-else class="badge bg-warning text-dark fs-6 px-3 py-2">⏳ Not Placed</span>
              </div>
            </div>
          </div>

          <!-- Resume Upload -->
          <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
              <h6 class="fw-bold mb-3">Resume</h6>

              <div v-if="resumeSuccess" class="alert alert-success py-2 small">{{ resumeSuccess }}</div>
              <div v-if="resumeError" class="alert alert-danger py-2 small">{{ resumeError }}</div>

              <!-- Current resume -->
              <div v-if="student?.resume_path" class="mb-3 p-3 bg-light rounded d-flex align-items-center gap-2">
                <span>📄</span>
                <div>
                  <p class="mb-0 small fw-semibold">Current Resume</p>
                  <a :href="`http://localhost:5000/${student.resume_path}`" target="_blank"
                    class="text-primary small">View / Download</a>
                </div>
              </div>
              <div v-else class="mb-3 p-3 bg-light rounded text-muted small">
                No resume uploaded yet.
              </div>

              <!-- Upload -->
              <label class="form-label small">Upload New Resume (PDF, max 5MB)</label>
              <input
                type="file"
                accept=".pdf"
                class="form-control form-control-sm"
                :disabled="uploadingResume"
                @change="uploadResume"
              />
              <div v-if="uploadingResume" class="text-muted small mt-2">
                <span class="spinner-border spinner-border-sm me-1"></span> Uploading...
              </div>
            </div>
          </div>

        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.table th { font-size: 13px; font-weight: 600; color: #6c757d; }
</style>