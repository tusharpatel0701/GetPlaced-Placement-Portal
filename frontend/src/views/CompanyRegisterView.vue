<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const company = reactive({
  company_name: "",
  email: "",
  password: "",
  website: "",
  hr_name: "",
  hr_email: "",
  hr_phone: "",
});

const error = ref("");
const loading = ref(false);
const showPassword = ref(false);

const registerCompany = async () => {
  error.value = "";

  if (
    !company.company_name ||
    !company.email ||
    !company.password ||
    !company.hr_name ||
    !company.hr_email ||
    !company.hr_phone
  ) {
    error.value = "Please fill all required fields";
    return;
  }

  try {
    loading.value = true;

    const payload = {
      email: company.email,
      password: company.password,
      role: "manager",
      company: {
        company_name: company.company_name,
        website: company.website || "",
        hr_name: company.hr_name,
        hr_email: company.hr_email,
        hr_phone: company.hr_phone,
      },
    };

    const res = await fetch("http://127.0.0.1:5000/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
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

    <!-- Main Layout -->
    <div class="main-wrap">

      <!-- Form Side -->
      <div class="form-side">

        <div class="card-header">
          <div class="role-badge">🏢 Company Registration</div>
          <h1 class="card-title">Register your company</h1>
          <p class="card-sub">Fill in your company and HR details to get started.</p>
        </div>

        <!-- Error -->
        <transition name="fade">
          <div v-if="error" class="error-banner">
            <span>⚠️</span> {{ error }}
          </div>
        </transition>

        <div class="form">

          <!-- Section: Company Info -->
          <div class="section-label">
            <span class="section-dot dot-teal"></span>
            Company Information
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Company Name <span class="required">*</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="e.g. Infosys, TCS"
                v-model="company.company_name"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Company Email <span class="required">*</span></label>
              <input
                type="email"
                class="form-input"
                placeholder="admin@company.com"
                v-model="company.email"
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
                  v-model="company.password"
                />
                <button class="toggle-pw" @click="showPassword = !showPassword" type="button">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Website <span class="optional">(optional)</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="https://company.com"
                v-model="company.website"
              />
            </div>
          </div>

          <!-- Section: HR Info -->
          <div class="section-label" style="margin-top: 8px;">
            <span class="section-dot dot-purple"></span>
            HR Contact Details
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">HR Name <span class="required">*</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="Full name"
                v-model="company.hr_name"
              />
            </div>
            <div class="form-group">
              <label class="form-label">HR Email <span class="required">*</span></label>
              <input
                type="email"
                class="form-input"
                placeholder="hr@company.com"
                v-model="company.hr_email"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">HR Phone <span class="required">*</span></label>
              <input
                type="text"
                class="form-input"
                placeholder="+91 9XXXXXXXXX"
                v-model="company.hr_phone"
              />
            </div>
            <div class="form-group"></div>
          </div>

          <button
            class="btn-primary btn-full"
            @click="registerCompany"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner"></span>
            <span v-else>Create Company Account</span>
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

/* Main Layout */
.main-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 90px 24px 60px;
  position: relative;
  z-index: 1;
}

/* Form Side */
.form-side {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 44px 48px;
  width: 100%;
  max-width: 680px;
  background: white;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 20px;
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
  background: #d1fae5; color: #065f46;
  border: 1px solid #6ee7b7;
}
.card-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 30px; font-weight: 800;
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
.optional { color: #aaa; font-weight: 400; font-size: 12px; }

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
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.1);
}
.form-input::placeholder { color: #bbb; }

.input-wrap { position: relative; }
.input-wrap .form-input { padding-right: 44px; }
.toggle-pw {
  position: absolute; right: 12px; top: 50%;
  transform: translateY(-50%);
  background: none; border: none;
  cursor: pointer; font-size: 16px;
}

/* Section labels */
.section-label {
  display: flex; align-items: center; gap: 8px;
  font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: #888;
}
.section-dot {
  width: 8px; height: 8px; border-radius: 50%;
}
.dot-teal   { background: #10b981; }
.dot-purple { background: #6366f1; }

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

/* Side Panel */
.side-panel {
  width: 400px; flex-shrink: 0;
  background: #0f0f0f;
  display: flex; align-items: center; justify-content: center;
}
.side-inner {
  padding: 52px 44px;
  display: flex; flex-direction: column; gap: 40px;
}
.side-logo {
  display: flex; align-items: center; gap: 10px;
}
.brand-icon-lg {
  width: 36px; height: 36px;
  background: white; color: #0f0f0f;
  border-radius: 9px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 700; line-height: 1;
}
.side-brand-name {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 22px; font-weight: 800; color: white;
}
.side-quote p {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 20px; font-weight: 600; color: white;
  line-height: 1.45;
}
.side-perks { display: flex; flex-direction: column; gap: 20px; }
.perk-item { display: flex; align-items: flex-start; gap: 14px; }
.perk-icon { font-size: 22px; margin-top: 2px; }
.perk-title { font-size: 14px; font-weight: 600; color: white; margin-bottom: 3px; }
.perk-desc  { font-size: 13px; color: #555; line-height: 1.5; }

.side-stats { display: flex; gap: 32px; }
.stat-item { display: flex; flex-direction: column; gap: 4px; }
.stat-num {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 32px; font-weight: 800; color: white; letter-spacing: -1px;
}
.stat-label { font-size: 13px; color: #555; }

/* Transitions */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Responsive */
@media (max-width: 600px) {
  .form-row { grid-template-columns: 1fr; }
  .form-side { padding: 32px 20px; }
  .nav-hint  { display: none; }
}
</style>