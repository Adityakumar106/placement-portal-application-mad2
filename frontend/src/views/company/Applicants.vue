<template>
  <div class="container mt-4">

    <h2 class="mb-4">Drive Details</h2>

    <!-- Drive Details -->
    <div class="card shadow mb-4">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">{{ drive.title }}</h4>
      </div>

      <div class="card-body">

        <div class="row mb-3">
          <div class="col-md-6">
            <strong>Job Title:</strong><br>
            {{ drive.job_title }}
          </div>

          <div class="col-md-6">
            <strong>Status:</strong><br>

            <span
              v-if="drive.status=='open'"
              class="badge bg-success"
            >
              Open
            </span>

            <span
              v-else
              class="badge bg-danger"
            >
              Closed
            </span>

          </div>
        </div>

        <div class="mb-3">
          <strong>Description</strong>

          <p class="mt-2">
            {{ drive.description }}
          </p>
        </div>

        <div class="row">

          <div class="col-md-4">
            <strong>Eligibility</strong><br>
            {{ drive.eligibility }}
          </div>

          <div class="col-md-4">
            <strong>Salary</strong><br>
            {{ drive.salary }}
          </div>

          <div class="col-md-4">
            <strong>Deadline</strong><br>
            {{ drive.deadline }}
          </div>

        </div>

      </div>
    </div>

    <!-- Applicants -->

    <div class="card shadow">

      <div class="card-header bg-dark text-white">
        <h4 class="mb-0">
          Student Applications
        </h4>
      </div>

      <div class="card-body">

        <table class="table table-hover table-bordered">

          <thead class="table-light">

          <tr>

            <th>ID</th>
            <th>Student Name</th>
            <th>Action</th>

          </tr>

          </thead>

          <tbody>

          <tr
            v-for="student in applicants"
            :key="student.id"
          >

            <td>{{ student.id }}</td>

            <td>{{ student.username }}</td>

            <td>

              <button
                class="btn btn-primary btn-sm"
                @click="reviewApplication(student.id)"
              >
                Review Application
              </button>

            </td>

          </tr>

          <tr v-if="applicants.length==0">

            <td colspan="3" class="text-center">

              No Students Have Applied Yet

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

drive:{},
applicants:[]

}

},

mounted(){

this.loadDrive()

},

methods:{

async loadDrive(){

const res=await fetch(
`${this.$apiBase}/company/drive/${this.$route.params.id}`,
{
credentials:"include"
})

const data=await res.json()

this.drive=data.drive
this.applicants=data.students

},

reviewApplication(studentId){

this.$router.push(
`/company/application/${this.$route.params.id}/${studentId}`
)

}

}

}



</script>