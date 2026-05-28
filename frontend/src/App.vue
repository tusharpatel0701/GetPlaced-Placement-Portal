<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import Navbar from "@/components/Navbar.vue";

const route = useRoute();

const hidePublicNavbar = computed(() =>
  route.path.startsWith("/admin") || route.path.startsWith("/company-dashboard") || route.path.startsWith("/student-dashboard")
);
</script>

<template>
  <!-- Admin & Company routes: full screen, no public navbar -->
  <template v-if="hidePublicNavbar">
    <router-view />
  </template>

  <!-- Public routes: fixed navbar + content pushed down 70px -->
  <template v-else>
    <Navbar />
    <div style="padding-top: 70px;">
      <router-view />
    </div>
  </template>
</template>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
}
</style>