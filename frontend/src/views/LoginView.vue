<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const showPassword = ref(false);

const handleLogin = async () => {
  if (!email.value || !password.value) {
    error.value = "Please fill all fields";
    return;
  }

  error.value = "";
  loading.value = true;

  try {
    const res = await fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value }),
    });

    const data = await res.json();

    if (!res.ok) {
      error.value = data.message || "Login failed";
      loading.value = false;
      return;
    }

    //Store all user data
    localStorage.setItem("token", data.token);
    localStorage.setItem("roles", JSON.stringify(data.roles));
    localStorage.setItem("user_id", data.id);

    // Store company_id if manager
    if (data.company_id) {
      localStorage.setItem("company_id", data.company_id);
    }

    // Store student_id if student
    if (data.student_id) {
      localStorage.setItem("student_id", data.student_id);
    }

    // Redirect based on role
    const roles = data.roles || [];
    if (roles.includes("admin")) {
      router.push("/admin");
    } else if (roles.includes("manager")) {
      router.push("/company-dashboard");
    } else {
      router.push("/student-dashboard");
    }

  } catch (err) {
    error.value = "Server error. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <section class="login-page">

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
          <span class="nav-hint">Don't have an account?</span>
          <button class="btn-outline" @click="router.push('/register')">Sign up</button>
        </div>
      </div>
    </nav>

    <!-- Login Card -->
    <div class="login-wrap">

      <!-- Left: Form -->
      <div class="login-card">

        <div class="card-header">
          <h1 class="card-title">Sign in to GetPlaced</h1>
          <p class="card-sub">Enter your credentials to access your dashboard.</p>
        </div>

        <!-- Error -->
        <transition name="fade">
          <div v-if="error" class="error-banner">
            <span class="error-icon">⚠️</span>
            {{ error }}
          </div>
        </transition>

        <!-- Form -->
        <div class="form">

          <div class="form-group">
            <label class="form-label">Email Address</label>
            <input
              type="email"
              class="form-input"
              placeholder="manish@gmail.com"
              v-model="email"
              @keyup.enter="handleLogin"
            />
          </div>

          <div class="form-group">
            <div class="label-row">
              <label class="form-label">Password</label>
              <span class="forgot-link" @click="router.push('/forgot-password')">Forgot password?</span>
            </div>
            <div class="input-wrap">
              <input
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Enter your password"
                v-model="password"
                @keyup.enter="handleLogin"
              />
              <button class="toggle-pw" @click="showPassword = !showPassword" type="button">
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <button
            class="btn-primary btn-full"
            :disabled="loading"
            @click="handleLogin"
          >
            <span v-if="loading" class="spinner"></span>
            <span v-else>Sign In</span>
            <span v-if="!loading" class="btn-arrow">→</span>
          </button>

        </div>

        <!-- Divider -->
        <div class="divider">
          <span>New to GetPlaced?</span>
        </div>

        <!-- Register links -->
        <div class="register-row">
          <button class="btn-register btn-register-purple" @click="router.push('/register/student')">
            🎓 Join as Student
          </button>
          <button class="btn-register btn-register-teal" @click="router.push('/register/company')">
            🏢 Join as Company
          </button>
        </div>
      </div>
    </div>

  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&family=DM+Sans:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.login-page {
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
  background: #0f0f0f;
  color: white;
  border-radius: 7px;
  display: inline-flex;
  align-items: center; justify-content: center;
  font-size: 16px; font-weight: 700; line-height: 1;
}
.nav-links { display: flex; align-items: center; gap: 14px; }
.nav-hint { font-size: 14px; color: #888; }
.btn-outline {
  padding: 8px 20px;
  border: 1.5px solid #0f0f0f;
  border-radius: 8px;
  background: transparent;
  color: #0f0f0f;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}
.btn-outline:hover { background: #0f0f0f; color: white; }

/* Login Layout */
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: stretch;
  padding-top: 57px;
  position: relative;
  z-index: 1;
}

/* Login Card */
.login-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 48px;
  max-width: 560px;
  margin: 0 auto;
}

.card-header { margin-bottom: 32px; }

.welcome-badge {
  display: inline-block;
  padding: 5px 14px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 14px;
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fcd34d;
}

.card-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 32px;
  font-weight: 800;
  color: #0f0f0f;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}
.card-sub { font-size: 15px; color: #777; line-height: 1.6; }

/* Error Banner */
.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  font-size: 14px;
  color: #b91c1c;
  margin-bottom: 20px;
}
.error-icon { font-size: 16px; }

/* Form */
.form { display: flex; flex-direction: column; gap: 20px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.label-row { display: flex; align-items: center; justify-content: space-between; }
.form-label { font-size: 13px; font-weight: 500; color: #444; }
.forgot-link {
  font-size: 13px;
  color: #6366f1;
  cursor: pointer;
  text-decoration: underline;
}
.forgot-link:hover { color: #4f46e5; }

.form-input {
  padding: 12px 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #0f0f0f;
  background: white;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
  width: 100%;
}
.form-input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}
.form-input::placeholder { color: #bbb; }

.input-wrap { position: relative; }
.input-wrap .form-input { padding-right: 44px; }
.toggle-pw {
  position: absolute;
  right: 12px; top: 50%;
  transform: translateY(-50%);
  background: none; border: none;
  cursor: pointer; font-size: 16px;
}

/* Buttons */
.btn-primary {
  padding: 13px 24px;
  border: none;
  border-radius: 10px;
  background: #0f0f0f;
  color: white;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px; font-weight: 500;
  cursor: pointer;
  transition: opacity 0.18s, transform 0.18s;
  display: flex; align-items: center; justify-content: center; gap: 8px;
}
.btn-primary:hover:not(:disabled) { opacity: 0.85; transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.45; cursor: not-allowed; transform: none; }
.btn-full { width: 100%; }
.btn-arrow { font-size: 18px; }

/* Spinner */
.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Divider */
.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 28px 0 20px;
  color: #bbb;
  font-size: 13px;
}
.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e5e7eb;
}

/* Register Row */
.register-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.btn-register {
  padding: 12px;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500;
  cursor: pointer;
  transition: transform 0.18s, box-shadow 0.18s;
  border: 1.5px solid transparent;
  text-align: center;
}
.btn-register:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.btn-register-purple {
  background: #ede9fe;
  color: #5b21b6;
  border-color: #c4b5fd;
}
.btn-register-teal {
  background: #d1fae5;
  color: #065f46;
  border-color: #6ee7b7;
}

/* Side Panel */
.side-panel {
  width: 420px;
  flex-shrink: 0;
  background: #0f0f0f;
  display: flex;
  align-items: center;
  justify-content: center;
}
.side-inner {
  padding: 48px 44px;
  display: flex;
  flex-direction: column;
  gap: 44px;
}
.side-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-icon-lg {
  width: 36px; height: 36px;
  background: white;
  color: #0f0f0f;
  border-radius: 9px;
  display: inline-flex;
  align-items: center; justify-content: center;
  font-size: 20px; font-weight: 700; line-height: 1;
}
.side-brand-name {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 22px; font-weight: 800;
  color: white;
}
.side-quote p {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 22px; font-weight: 600;
  color: white;
  line-height: 1.45;
}
.side-stats { display: flex; flex-direction: column; gap: 24px; }
.stat-item { display: flex; flex-direction: column; gap: 4px; }
.stat-num {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 34px; font-weight: 800;
  color: white; letter-spacing: -1px;
}
.stat-label { font-size: 13px; color: #555; }
.side-avatars { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; }
.avatar {
  width: 36px; height: 36px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 600;
  border: 2px solid #1a1a1a;
  margin-right: -8px;
}
.av1 { background: #ede9fe; color: #5b21b6; }
.av2 { background: #d1fae5; color: #065f46; }
.av3 { background: #fef3c7; color: #92400e; }
.av4 { background: #1e293b; color: #94a3b8; }
.avatar-text { font-size: 13px; color: #555; margin-left: 18px; }

/* Transition */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Responsive */
@media (max-width: 900px) {
  .side-panel { display: none; }
  .login-card { padding: 48px 28px; }
}
@media (max-width: 480px) {
  .login-card { padding: 32px 20px; }
  .register-row { grid-template-columns: 1fr; }
  .nav-hint { display: none; }
}
</style>