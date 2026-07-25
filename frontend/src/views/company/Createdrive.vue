<template>
  <div class="card shadow">
    <div class="card-body">

      <h3>Create Placement Drive</h3>

      <form @submit.prevent="createDrive">

        <div class="mb-3">
          <label>Drive Title</label>
          <input
            v-model="title"
            class="form-control"
            placeholder="Campus Recruitment 2026"
            required
          >
        </div>

        <div class="mb-3">
          <label>Job Title</label>
          <input
            v-model="job_title"
            class="form-control"
            required
          >
        </div>

        <div class="mb-3">
          <label>Description</label>
          <textarea
            v-model="description"
            class="form-control"
          ></textarea>
        </div>

        <div class="mb-3">
          <label>Eligibility</label>
          <input
            v-model="eligibility"
            class="form-control"
          >
        </div>

        <div class="mb-3">
          <label>Salary</label>
          <input
            v-model="salary"
            class="form-control"
          >
        </div>

        <div class="mb-3">
          <label>Deadline</label>
          <input
            type="date"
            v-model="deadline"
            class="form-control"
          >
        </div>

        <button class="btn btn-success">
          Create Drive
        </button>

      </form>

    </div>
  </div>
</template>

<script>
export default {

  data() {
    return {
      title: "",
      job_title: "",
      description: "",
      eligibility: "",
      salary: "",
      deadline: ""
    }
  },

  methods: {
    async createDrive() {
      try {
        const response = await fetch(`${this.$apiBase}/company/create-drive`, {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            title: this.title,
            job_title: this.job_title,
            description: this.description,
            eligibility: this.eligibility,
            salary: this.salary,
            deadline: this.deadline
          })
        })

        const data = await response.json().catch(() => ({}))

        if (!response.ok) {
          throw new Error(data.message || "Failed to create drive")
        }

        alert(data.message || "Placement Drive Created Successfully")
        this.$router.push("/company/drives")
      } catch (error) {
        console.error(error)
        alert(error.message || "Unable to create placement drive")
      }
    }
  }

}
</script>