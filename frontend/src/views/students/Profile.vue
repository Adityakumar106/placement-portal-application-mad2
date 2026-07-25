<template>
  <div class="container mt-4">

    <div class="card shadow">

      <div class="card-header bg-primary text-white">
        <h3 class="mb-0">Student Profile</h3>
      </div>

      <div class="card-body">

        <form @submit.prevent="saveProfile">

          <div class="mb-3">
            <label class="form-label">Name</label>
            <input
              v-model="student.username"
              class="form-control"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Degree</label>
            <input
              v-model="student.degree"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Course</label>
            <input
              v-model="student.course"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Branch</label>
            <input
              v-model="student.branch"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">CGPA</label>
            <input
              v-model="student.cgpa"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Phone</label>
            <input
              v-model="student.phone"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">LinkedIn</label>
            <input
              v-model="student.linkdin"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Resume</label>
            <input
              v-model="student.resume"
              class="form-control"
              placeholder="Resume Link"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">About</label>
            <textarea
              v-model="student.about"
              class="form-control"
              rows="4"
            ></textarea>
          </div>

          <button class="btn btn-primary">
            Save Profile
          </button>

        </form>

      </div>

    </div>

  </div>
</template>

<script>
export default {

  data() {
    return {
      student: {}
    }
  },

  mounted() {
    this.loadProfile()
  },

  methods: {

    async loadProfile() {

      const res = await fetch(
        `${this.$apiBase}/student/profile`,
        {
          credentials: "include"
        }
      )

      this.student = await res.json()
    },

    async saveProfile() {

      const res = await fetch(
        `${this.$apiBase}/student/profile`,
        {
          method: "PUT",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(this.student)
        }
      )

      const data = await res.json()

      alert(data.message)
    }

  }

}
</script>