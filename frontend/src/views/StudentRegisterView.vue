<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();

const student = reactive({
  name: "",
  email: "",
  password: "",
  roll_no: "",
  branch: "",
  cgpa: "",
  year: "",
  phone: "",
});

const error = ref("");
const loading = ref(false);
const showPassword = ref(false);

const registerStudent = async () => {
  error.value = "";

  if (
    !student.name ||
    !student.email ||
    !student.password ||
    !student.roll_no ||
    !student.branch ||
    !student.cgpa ||
    !student.year ||
    !student.phone
  ) {
    error.value = "Please fill all fields";
    return;
  }

  try {
    loading.value = true;

    const res = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: student.email,
        password: student.password,
        role: "student",
        student: {
          name: student.name,
          roll_no: student.roll_no,
          branch: student.branch,
          cgpa: parseFloat(student.cgpa),
          year: parseInt(student.year),
          phone: student.phone,
        },
      }),
    });

    let data;
    try {
      data = await res.json();
    } catch (e) {
      error.value = "Server error. Please try again.";
      return;
    }

    if (!res.ok) {
      error.value = data.message || "Registration failed";
      return;
    }

    router.push("/login");

  } catch (err) {
    error.value = "Cannot connect to server";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <section class="page">

    <!-- Grid Background -->
    <div class="grid-bg" aria-hidden="true"></div>

    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-inner">
        <div class="nav-brand" @click="router.push('/')" style="cursor:pointer;">
          <span class="brand-icon">+</span>
          <span class="brand-name">GetPlaced</span>
        </div>
        <div class="nav-links">
          <span class="nav-hint">Already have an account?</span>
          <button class="btn-outline" @click="router.push('/login')">Login</button>
        </div>
      </div>
    </nav>

    <!-- Centered Content -->
    <div class="page-body">
      <div class="register-card">

        <!-- Header -->
        <div class="card-header">
          <div class="role-badge">🎓 Student Registration</div>
          <h1 class="card-title">Create your student account</h1>
          <p class="card-sub">Fill in your academic details to get started with placements.</p>
        </div>

        <!-- Error -->
        <transition name="fade">
          <div v-if="error" class="error-banner">
            <span>⚠️</span> {{ error }}
          </div>
        </transition>

        <div class="form">

          <!-- Section: Personal Info -->
          <div class="section-label">
            <span class="section-dot dot-purple"></span>
            Personal Information
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Full Name <span class="required">*</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="e.g. Rahul Sharma"
                v-model="student.name"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Email Address <span class="required">*</span></label>
              <input
                type="email"
                class="form-input"
                placeholder="rahul@email.com"
                v-model="student.email"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Password <span class="required">*</span></label>
              <div class="input-wrap">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Enter your password"
                  v-model="student.password"
                />
                <button class="toggle-pw" @click="showPassword = !showPassword" type="button">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Phone Number <span class="required">*</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="+91 9XXXXXXXXX"
                v-model="student.phone"
              />
            </div>
          </div>

          <!-- Section: Academic Info -->
          <div class="section-label" style="margin-top: 4px;">
            <span class="section-dot dot-amber"></span>
            Academic Information
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Roll Number <span class="required">*</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="e.g. 2100140100050"
                v-model="student.roll_no"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Branch <span class="required">*</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="e.g. CSE, ECE, ME"
                v-model="student.branch"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">CGPA <span class="required">*</span></label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                class="form-input"
                placeholder="e.g. 8.5"
                v-model="student.cgpa"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Current Year <span class="required">*</span></label>
              <select class="form-input form-select" v-model="student.year">
                <option value="" disabled>Select year</option>
                <option value="1">1st Year</option>
                <option value="2">2nd Year</option>
                <option value="3">3rd Year</option>
                <option value="4">4th Year</option>
              </select>
            </div>
          </div>

          <button
            class="btn-primary btn-full"
            @click="registerStudent"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner"></span>
            <span v-else>Create Student Account</span>
            <span v-if="!loading" class="btn-arrow">→</span>
          </button>

          <p class="login-hint">
            Already have an account?
            <span class="link" @click="router.push('/login')">Sign in</span>
          </p>

        </div>
      </div>
    </div>

  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&family=DM+Sans:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  font-family: 'DM Sans', sans-serif;
  background: #f8f7f4;
  color: #0f0f0f;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* Grid BG */
.grid-bg {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}

/* Navbar */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(248,247,244,0.88);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 800;
  font-size: 18px;
  color: #0f0f0f;
}
.brand-icon {
  width: 28px; height: 28px;
  background: #0f0f0f; color: white;
  border-radius: 7px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 700; line-height: 1;
}
.nav-links { display: flex; align-items: center; gap: 14px; }
.nav-hint { font-size: 14px; color: #888; }
.btn-outline {
  padding: 8px 20px;
  border: 1.5px solid #0f0f0f;
  border-radius: 8px;
  background: transparent; color: #0f0f0f;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}
.btn-outline:hover { background: #0f0f0f; color: white; }

/* Page Body */
.page-body {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 90px 24px 60px;
  position: relative;
  z-index: 1;
}

/* Register Card */
.register-card {
  background: white;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 20px;
  padding: 44px 48px;
  width: 100%;
  max-width: 680px;
  box-shadow: 0 4px 40px rgba(0,0,0,0.06);
}

/* Header */
.card-header { margin-bottom: 28px; }
.role-badge {
  display: inline-block;
  padding: 5px 14px;
  border-radius: 999px;
  font-size: 13px; font-weight: 500;
  margin-bottom: 14px;
  background: #ede9fe; color: #5b21b6;
  border: 1px solid #c4b5fd;
}
.card-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 28px; font-weight: 800;
  color: #0f0f0f; letter-spacing: -0.5px;
  margin-bottom: 8px;
}
.card-sub { font-size: 15px; color: #777; line-height: 1.6; }

/* Error */
.error-banner {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  font-size: 14px; color: #b91c1c;
  margin-bottom: 20px;
}

/* Form */
.form { display: flex; flex-direction: column; gap: 18px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-label { font-size: 13px; font-weight: 500; color: #444; }
.required { color: #ef4444; }

.form-input {
  padding: 11px 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px; color: #0f0f0f;
  background: white;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none; width: 100%;
}
.form-input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}
.form-input::placeholder { color: #bbb; }

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23888' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  cursor: pointer;
}

.input-wrap { position: relative; }
.input-wrap .form-input { padding-right: 44px; }
.toggle-pw {
  position: absolute; right: 12px; top: 50%;
  transform: translateY(-50%);
  background: none; border: none;
  cursor: pointer; font-size: 16px;
}

/* Section Labels */
.section-label {
  display: flex; align-items: center; gap: 8px;
  font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: #888;
}
.section-dot { width: 8px; height: 8px; border-radius: 50%; }
.dot-purple { background: #6366f1; }
.dot-amber  { background: #f59e0b; }

/* Buttons */
.btn-primary {
  padding: 13px 24px;
  border: none; border-radius: 10px;
  background: #0f0f0f; color: white;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px; font-weight: 500;
  cursor: pointer;
  transition: opacity 0.18s, transform 0.18s;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  margin-top: 4px;
}
.btn-primary:hover:not(:disabled) { opacity: 0.85; transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
.btn-full { width: 100%; }
.btn-arrow { font-size: 18px; }

.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

.login-hint {
  text-align: center;
  font-size: 14px; color: #888;
}
.link {
  color: #6366f1; cursor: pointer;
  text-decoration: underline; font-weight: 500;
}
.link:hover { color: #4f46e5; }

/* Transitions */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Responsive */
@media (max-width: 600px) {
  .form-row { grid-template-columns: 1fr; }
  .register-card { padding: 32px 20px; }
  .nav-hint { display: none; }
}
</style>