<template>
  <div class="container mt-4">

    <h2 class="mb-4">Student Dashboard</h2>

    <div class="card shadow">

      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Available Placement Drives</h4>
      </div>

      <div class="card-body">

        <div v-if="message" class="alert alert-success">{{ message }}</div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <table class="table table-bordered table-hover">

          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Company</th>
              <th>Drive Title</th>
              <th>Job Title</th>
              <th>Eligibility</th>
              <th>Deadline</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="drive in drives"
              :key="drive.id"
            >

              <td>{{ drive.id }}</td>

              <td>{{ drive.company }}</td>

              <td>{{ drive.title }}</td>

              <td>{{ drive.job_title }}</td>

              <td>{{ drive.eligibility }}</td>

              <td>{{ drive.deadline }}</td>

              <td>

                <button
                  class="btn btn-primary btn-sm"
                  @click="viewDetails(drive.id)"
                >
                  View Details
                </button>

              </td>

            </tr>

            <tr v-if="drives.length==0">

              <td colspan="7" class="text-center">
                No Placement Drives Available
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script>
export default{

data(){

return{

drives:[],
message:"",
error:""

}

},

mounted(){

this.loadDashboard()

},

methods:{

async loadDashboard(){

this.message = ""
this.error = ""

try {
  const res = await fetch(
  `${this.$apiBase}/student/dashboard`,
  {
  credentials:"include"
  })

  const data = await res.json().catch(() => ({}))

  if (!res.ok) {
    throw new Error(data.message || "Unable to load drives")
  }

  this.drives = data.drives || []
} catch (err) {
  this.error = err.message || "Unable to load drives"
  this.drives = []
}

},

viewDetails(id){

this.$router.push(`/student/drive/${id}`)

}

}

}
</script>