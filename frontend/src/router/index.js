import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import StudentRegisterView from "../views/StudentRegisterView.vue";
import CompanyRegisterView from "../views/CompanyRegisterView.vue";
import AdminDashboard from "../views/Admin/AdminDashboard.vue";
import Adminlayout from "../components/Adminlayout.vue";
import AdminCompanies from "../views/Admin/Admincompanies.vue";
import AdminDrives from "../views/Admin/Admindrives.vue";
import AdminApplications from "../views/Admin/AdminApplications.vue";
import AdminStudents from "@/views/Admin/AdminStudents.vue";


import CompanyLayout from "../components/Companylayout.vue";
import CompanyDashboard from "../views/Company/CompanyDashboard.vue";
import CompanyDrives from "../views/Company/CompanyDrives.vue";
import CompanyApplications from "../views/Company/CompanyApplications.vue";

import StudentDashboard from "../views/Students/StudentDashboard.vue";
import StudentProfile from "../views/Students/StudentProfile.vue";
import StudentApplications from "../views/Students/StudentApplications.vue";
import StudentDrives from "../views/Students/StudentDrives.vue";
import StudentLayout from "../components/Studentlayout.vue"; 

const routes = [
   { path: "/", component: Home },
   { path: "/login", component: LoginView },
   { path: "/register/student", component: StudentRegisterView },
   { path: "/register/company", component: CompanyRegisterView },
  //  { path: "/admin", component: AdminDashboard }

   {
    path: "/admin",
    component: Adminlayout,           // <-- swaps out the public navbar
    children: [
      { path: "",
      component: AdminDashboard },
      { path: "companies", component: AdminCompanies },
      { path: "drives", component: AdminDrives },
      { path: "applications", component: AdminApplications },
      { path: "students", component: AdminStudents }
    ]
  },

  {
  path: "/company-dashboard",
  component: CompanyLayout,
  children: [
    { path: "",  component: CompanyDashboard },
    { path: "drives", component: CompanyDrives },
    { path: "applications", component: CompanyApplications },
  ]
},

{
  path: "/student-dashboard",
  component: StudentLayout,
  children: [
    { path: "",              component: StudentDashboard },
    { path: "profile",       component: StudentProfile },
    { path: "applications",  component: StudentApplications },
    { path: "drives",        component: StudentDrives },  // if you have this view
  ]
}

];

export default createRouter({
  history: createWebHistory(),
  routes
});