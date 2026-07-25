import { createRouter, createWebHistory } from "vue-router"


import Home from "../views/Home.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"


import AdminLayout from "../layouts/AdminLayout.vue"
import CompanyLayout from "../layouts/CompanyLayout.vue"
import StudentLayout from "../layouts/StudentLayout.vue"


import Dashboard from "../views/admin/Dashboard.vue"
import Students from "../views/admin/Students.vue"
import Companies from "../views/admin/Companies.vue"
import Drives from "../views/admin/Drives.vue"
import Applications from "../views/admin/Applications.vue"
import DriveDetails from "../views/admin/Admindrivedetail.vue"
import Userdetail from "../views/admin/Userdetail.vue"

import CompanyDashboard from "../views/company/Dashboard.vue"
import CompanyProfile from "../views/company/Profile.vue"
import CompanyDrives from "../views/company/Drives.vue"
import CreateDrive from "../views/company/Createdrive.vue"
import CompanyApplications from "../views/company/Applicants.vue"
import Studentdetail from "../views/company/Reviewapp.vue"


import StudentDashboard from "../views/students/Dashboard.vue"
import StudentProfile from "../views/students/Profile.vue"
import StudentApplications from "../views/students/Application.vue"
import StudentHistory from "../views/students/History.vue"
import StudentDriveDetails from "../views/students/Studentdrivedetail.vue"

const routes = [

  {
    path: "/",
    component: Home
  },

  {
    path: "/login",
    component: Login
  },

  {
    path: "/register",
    component: Register
  },
  
  
  {
    path: "/admin",
    component: AdminLayout,

    children: [

      {
        path: "dashboard",
        component: Dashboard
      },

      {
        path: "students",
        component: Students
      },

      {
        path: "companies",
        component: Companies
      },

      {
        path: "drives",
        component: Drives
      },

      {
        path: "applications",
        component: Applications
      },

      
      {
        path: "drive/:id",
        component: DriveDetails
      },
      {
        path: "application/:id",
        component: Userdetail
      }

    ]

  },


  {
    path: "/company",
    component: CompanyLayout,

    children: [

      {
        path: "dashboard",
        component: CompanyDashboard
      },

      {
        path: "profile",
        component: CompanyProfile
      },

      {
        path: "drives",
        component: CompanyDrives
      },

      {
        path: "create-drive",
        component: CreateDrive
      },

      {
        path: "drive/:id",
        component: CompanyApplications
      },
      {
        path: "application/:driveId/:studentId",
        component: Studentdetail
      }

    ]

  },

 

  {
    path: "/student",
    component: StudentLayout,

    children: [

      {
        path: "dashboard",
        component: StudentDashboard
      },

      {
        path: "profile",
        component: StudentProfile
      },

      {
        path: "applications",
        component: StudentApplications
      },

      {
        path: "history",
        component: StudentHistory
      },
      {
        path: "drive/:id",
        component: StudentDriveDetails
      }

    ]

  }

]

const router = createRouter({

  history: createWebHistory(),

  routes

})

export default router