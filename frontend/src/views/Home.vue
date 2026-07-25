
<template>
  <div>

    <Navbar />

    

    <section class="bg-light py-5">
      <div class="container">

        <div class="row align-items-center">

          <div class="col-lg-6">

            <h1 class="display-4 fw-bold">
              Placement Portal
            </h1>

            <p class="lead mt-3">
              A centralized platform connecting students,
              companies and institute placement cells.
            </p>

            <div class="mt-4">

              <router-link
                to="/register"
                class="btn btn-primary btn-lg me-3"
              >
                Get Started
              </router-link>

              <router-link
                to="/login"
                class="btn btn-outline-primary btn-lg"
              >
                Login
              </router-link>

            </div>

          </div>

          <div class="col-lg-6 text-center">

            <img
              src="../assets/a.jpg"
              class="img-fluid"
              style="max-height:300px"
            />

          </div>

        </div>

      </div>
    </section>

    <!-- Features -->

    <section class="py-5">
      <div class="container">

        <h2 class="text-center mb-5">
          Platform Features
        </h2>

        <div class="row">

          <div class="col-md-4 mb-4">
            <div class="card shadow h-100">
              <div class="card-body text-center">
                <h4>Students</h4>
                <p>
                  Apply for placement drives,
                  upload resumes and track applications.
                </p>
              </div>
            </div>
          </div>

          <div class="col-md-4 mb-4">
            <div class="card shadow h-100">
              <div class="card-body text-center">
                <h4>Companies</h4>
                <p>
                  Create placement drives and manage applicants.
                </p>
              </div>
            </div>
          </div>

          <div class="col-md-4 mb-4">
            <div class="card shadow h-100">
              <div class="card-body text-center">
                <h4>Institute</h4>
                <p>
                  Monitor drives, approvals and placement statistics.
                </p>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
</script>