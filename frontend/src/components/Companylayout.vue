<script setup>
import { useRouter, useRoute } from "vue-router";
import { ref } from "vue";

const router = useRouter();
const route = useRoute();

const mobileOpen = ref(false);

function logout() {
  localStorage.clear();
  router.push("/");
}

const navItems = [
  {
    label: "Overview",
    path: "/company-dashboard",
  },
  {
    label: "My Drives",
    path: "/company-dashboard/drives",
  },
  {
    label: "Applications",
    path: "/company-dashboard/applications",
  },
];
</script>

<template>
  <div class="layout">

    <!-- Navbar -->
    <nav class="navbar">

      <div class="nav-inner">

        <!-- Brand -->
        <div
          class="nav-brand"
          @click="router.push('/company-dashboard')"
        >

          <span class="brand-name">
            GetPlaced
          </span>

          <span class="brand-pill">
            Company
          </span>
        </div>

        <!-- Desktop Nav -->
        <ul class="nav-links">

          <li
            v-for="item in navItems"
            :key="item.path"
          >
            <span
              class="nav-link"

              :class="{
                active: route.path === item.path
              }"

              @click="router.push(item.path)"
            >
              {{ item.label }}
            </span>
          </li>

        </ul>

        <!-- Right Side -->
        <div class="nav-right">

          <button
            class="btn-logout"
            @click="logout"
          >
            Logout
          </button>

        </div>

        <!-- Mobile Hamburger -->
        <button
          class="hamburger"
          @click="mobileOpen = !mobileOpen"
        >
          <span
            :class="
              mobileOpen
                ? 'bar bar-open-1'
                : 'bar'
            "
          ></span>

          <span
            :class="
              mobileOpen
                ? 'bar bar-open-2'
                : 'bar'
            "
          ></span>

          <span
            :class="
              mobileOpen
                ? 'bar bar-open-3'
                : 'bar'
            "
          ></span>
        </button>

      </div>

      <!-- Mobile Menu -->
      <transition name="slide-down">

        <div
          v-if="mobileOpen"
          class="mobile-menu"
        >

          <span
            v-for="item in navItems"
            :key="item.path"

            class="mobile-link"

            :class="{
              active: route.path === item.path
            }"

            @click="
              router.push(item.path);
              mobileOpen = false;
            "
          >
            {{ item.label }}
          </span>

          <div class="mobile-footer">

            <span class="user-label">
              🏢 <strong>Manager</strong>
            </span>

            <button
              class="btn-logout"
              @click="logout"
            >
              Logout
            </button>

          </div>

        </div>

      </transition>

    </nav>

    <!-- Page Content -->
    <div class="page-content">
      <router-view />
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&family=DM+Sans:wght@400;500&display=swap');

*{
  box-sizing:border-box;
  margin:0;
  padding:0;
}

.layout{
  font-family:'DM Sans',sans-serif;
  width:100%;
  min-height:100vh;
  display:flex;
  flex-direction:column;
  background:#f8f7f4;
}

/* NAVBAR */

.navbar{
  position:fixed;
  top:0;
  left:0;
  right:0;
  z-index:100;
  background:rgba(248,247,244,0.92);
  backdrop-filter:blur(12px);
  border-bottom:1px solid rgba(0,0,0,0.08);
}

.nav-inner{
  max-width:1280px;
  margin:0 auto;
  padding:0 28px;
  height:60px;
  display:flex;
  align-items:center;
  gap:32px;
  width:100%;
}

/* BRAND */

.nav-brand{
  display:flex;
  align-items:center;
  gap:8px;
  cursor:pointer;
  flex-shrink:0;
}

.brand-icon{
  width:28px;
  height:28px;
  background:#0f0f0f;
  color:white;
  border-radius:7px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:15px;
  font-weight:700;
}

.brand-name{
  font-family:'Bricolage Grotesque',sans-serif;
  font-weight:800;
  font-size:17px;
  color:#0f0f0f;
}

.brand-pill{
  font-size:11px;
  font-weight:600;
  background:#dbeafe;
  color:#1d4ed8;
  border:1px solid #93c5fd;
  padding:2px 8px;
  border-radius:999px;
}

/* NAV LINKS */

.nav-links{
  display:flex;
  align-items:center;
  gap:2px;
  list-style:none;
  flex:1;
}

.nav-link{
  display:flex;
  align-items:center;
  gap:6px;
  padding:6px 12px;
  border-radius:8px;
  font-size:14px;
  font-weight:500;
  color:#555;
  cursor:pointer;
  transition:background .15s,color .15s;
  white-space:nowrap;
}

.nav-link:hover{
  background:rgba(0,0,0,0.05);
  color:#0f0f0f;
}

.nav-link.active{
  background:#0f0f0f;
  color:white;
}

/* RIGHT SIDE */

.nav-right{
  display:flex;
  align-items:center;
  gap:12px;
  flex-shrink:0;
  margin-left:auto;
}

.user-label{
  font-size:13px;
  color:#777;
}

.user-label strong{
  color:#0f0f0f;
}

.btn-logout{
  padding:7px 16px;
  border:1.5px solid #0f0f0f;
  border-radius:8px;
  background:transparent;
  color:#0f0f0f;
  font-family:'DM Sans',sans-serif;
  font-size:13px;
  font-weight:500;
  cursor:pointer;
  transition:background .18s,color .18s;
}

.btn-logout:hover{
  background:#0f0f0f;
  color:white;
}

/* HAMBURGER */

.hamburger{
  display:none;
  flex-direction:column;
  gap:5px;
  background:none;
  border:none;
  cursor:pointer;
  padding:4px;
  margin-left:auto;
}

.bar{
  display:block;
  width:22px;
  height:2px;
  background:#0f0f0f;
  border-radius:2px;
  transition:all .25s;
}

.bar-open-1{
  transform:translateY(7px) rotate(45deg);
}

.bar-open-2{
  opacity:0;
}

.bar-open-3{
  transform:translateY(-7px) rotate(-45deg);
}

/* MOBILE MENU */

.mobile-menu{
  display:flex;
  flex-direction:column;
  padding:12px 20px 16px;
  border-top:1px solid rgba(0,0,0,0.06);
  background:rgba(248,247,244,0.98);
  gap:2px;
}

.mobile-link{
  padding:10px 14px;
  border-radius:10px;
  font-size:15px;
  font-weight:500;
  color:#555;
  cursor:pointer;
  transition:background .15s,color .15s;
  display:flex;
  align-items:center;
  gap:8px;
}

.mobile-link:hover{
  background:rgba(0,0,0,0.05);
  color:#0f0f0f;
}

.mobile-link.active{
  background:#0f0f0f;
  color:white;
}

.mobile-footer{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:12px 14px 0;
  margin-top:8px;
  border-top:1px solid rgba(0,0,0,0.06);
}

/* PAGE CONTENT */

.page-content{
  flex:1;
  margin-top:60px;
  background:#f8f7f4;
}

/* TRANSITIONS */

.slide-down-enter-active{
  transition:all .22s ease;
}

.slide-down-leave-active{
  transition:all .18s ease;
}

.slide-down-enter-from{
  opacity:0;
  transform:translateY(-8px);
}

.slide-down-leave-to{
  opacity:0;
  transform:translateY(-8px);
}

/* RESPONSIVE */

@media (max-width:900px){

  .nav-links,
  .nav-right{
    display:none;
  }

  .hamburger{
    display:flex;
  }
}
</style>