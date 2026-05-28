<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const isOpen = ref(false);

const goToLogin           = () => { router.push("/login");             isOpen.value = false; };
const goToStudentRegister = () => { router.push("/register/student");  isOpen.value = false; };
const goToCompanyRegister = () => { router.push("/register/company");  isOpen.value = false; };
</script>

<template>
  <nav class="navbar">
    <div class="nav-inner">

      <!-- Logo -->
      <div class="nav-brand" @click="router.push('/')">
        <!-- <img src="@/assets/logo.jpg" alt="GetPlaced Logo" class="logo-img" /> -->
        <span class="brand-name">GetPlaced</span>
      </div>

      <!-- Desktop Buttons -->
      <div class="nav-actions">
        <button class="btn-login" @click="goToLogin">Login</button>
        <button class="btn-student" @click="goToStudentRegister">
          🎓 Student Register
        </button>
        <button class="btn-company" @click="goToCompanyRegister">
          🏢 Company Register
        </button>
      </div>

      <!-- Hamburger -->
      <button class="hamburger" @click="isOpen = !isOpen" aria-label="Toggle menu">
        <span :class="isOpen ? 'bar bar-open-1' : 'bar'"></span>
        <span :class="isOpen ? 'bar bar-open-2' : 'bar'"></span>
        <span :class="isOpen ? 'bar bar-open-3' : 'bar'"></span>
      </button>

    </div>
  </nav>

  <!-- Mobile Menu -->
  <transition name="slide-down">
    <div v-if="isOpen" class="mobile-menu">
      <button class="mobile-btn mobile-login"   @click="goToLogin">Login</button>
      <button class="mobile-btn mobile-student" @click="goToStudentRegister">🎓 Student Register</button>
      <button class="mobile-btn mobile-company" @click="goToCompanyRegister">🏢 Company Register</button>
    </div>
  </transition>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&family=DM+Sans:wght@400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Navbar ── */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  background: rgba(248,247,244,0.88);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 48px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

/* Brand */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  text-decoration: none;
}
.logo-img {
  height: 36px;
  width: auto;
  object-fit: contain;
  border-radius: 8px;
}
.brand-name {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 800;
  font-size: 18px;
  color: #0f0f0f;
}

/* Desktop Buttons */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-login {
  padding: 9px 24px;
  border: 1.5px solid #0f0f0f;
  border-radius: 8px;
  background: transparent;
  color: #0f0f0f;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}
.btn-login:hover { background: #0f0f0f; color: white; }

.btn-student {
  padding: 9px 22px;
  border: 1.5px solid #c4b5fd;
  border-radius: 8px;
  background: #ede9fe;
  color: #5b21b6;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500;
  cursor: pointer;
  transition: background 0.18s, transform 0.18s;
}
.btn-student:hover { background: #ddd6fe; transform: translateY(-1px); }

.btn-company {
  padding: 9px 22px;
  border: 1.5px solid #6ee7b7;
  border-radius: 8px;
  background: #d1fae5;
  color: #065f46;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 500;
  cursor: pointer;
  transition: background 0.18s, transform 0.18s;
}
.btn-company:hover { background: #a7f3d0; transform: translateY(-1px); }

/* Hamburger */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none; border: none;
  cursor: pointer; padding: 4px;
}
.bar {
  display: block;
  width: 22px; height: 2px;
  background: #0f0f0f; border-radius: 2px;
  transition: all 0.25s;
}
.bar-open-1 { transform: translateY(7px) rotate(45deg); }
.bar-open-2 { opacity: 0; }
.bar-open-3 { transform: translateY(-7px) rotate(-45deg); }

/* Mobile Menu */
.mobile-menu {
  position: fixed;
  top: 64px; left: 0; right: 0;
  z-index: 999;
  background: rgba(248,247,244,0.98);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.08);
  padding: 16px 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mobile-btn {
  width: 100%;
  padding: 13px 18px;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px; font-weight: 500;
  cursor: pointer;
  text-align: left;
  transition: opacity 0.18s, transform 0.18s;
  border: 1.5px solid transparent;
}
.mobile-btn:hover { transform: translateY(-1px); opacity: 0.9; }

.mobile-login {
  background: transparent;
  border-color: #0f0f0f;
  color: #0f0f0f;
}
.mobile-student {
  background: #ede9fe;
  border-color: #c4b5fd;
  color: #5b21b6;
}
.mobile-company {
  background: #d1fae5;
  border-color: #6ee7b7;
  color: #065f46;
}

/* Transition */
.slide-down-enter-active { transition: all 0.22s ease; }
.slide-down-leave-active { transition: all 0.18s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-10px); }

/* Responsive */
@media (max-width: 700px) {
  .nav-actions { display: none; }
  .hamburger   { display: flex; }
}
</style>