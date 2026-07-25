<template>

<div class="container mt-4">

<div class="card shadow">

<div class="card-header bg-primary text-white">

<h3 class="mb-0">
Review Application
</h3>

</div>

<div class="card-body" v-if="application">

<h5 class="mb-3">Student Details</h5>

<div class="row">

<div class="col-md-6">

<p><strong>Name:</strong> {{ application.username }}</p>

<p><strong>Email:</strong> {{ application.email }}</p>

<p><strong>Degree:</strong> {{ application.degree }}</p>

<p><strong>Course:</strong> {{ application.course }}</p>

<p><strong>Branch:</strong> {{ application.branch }}</p>

<p><strong>CGPA:</strong> {{ application.cgpa }}</p>

<p><strong>Phone:</strong> {{ application.phone }}</p>

<p><strong>LinkedIn:</strong></p>

<a
:href="application.linkedin"
target="_blank"
>
{{ application.linkedin }}
</a>

</div>

<div class="col-md-6">

<p><strong>Drive:</strong> {{ application.drive }}</p>

<p><strong>Company:</strong> {{ application.company }}</p>

<p><strong>About:</strong></p>

<p>{{ application.about }}</p>

</div>

</div>

<hr>

<div class="mb-3">

<a
:href="application.resume"
target="_blank"
class="btn btn-success"
>
View Resume
</a>

</div>

<hr>

<h5>Interview Decision</h5>

<div class="mb-3">

<label class="form-label">
Application Result
</label>

<select
v-model="application.result"
class="form-select"
>

<option value="Waiting">Waiting</option>

<option value="Shortlisted">Shortlisted</option>

<option value="Declined">Declined</option>

</select>

</div>

<div class="mb-3">

<label class="form-label">
Interview Mode
</label>

<select
v-model="application.mode"
class="form-select"
>

<option value="">Select Mode</option>

<option value="Online">Online</option>

<option value="Offline">Offline</option>

</select>

</div>

<div class="mb-3">

<label class="form-label">
Interview Date
</label>

<input
type="date"
v-model="application.interview_date"
class="form-control"
>

</div>

<button
class="btn btn-primary me-2"
@click="saveApplication"
>
Save
</button>

<button
class="btn btn-secondary"
@click="$router.back()"
>
Back
</button>

</div>

</div>

</div>

</template>

<script>
export default{

data(){

return{

application:{}

}

},

mounted(){

this.loadApplication()

},

methods:{

async loadApplication(){

const res = await fetch(

`${this.$apiBase}/company/application/${this.$route.params.driveId}/${this.$route.params.studentId}`,

{

credentials:"include"

})

this.application = await res.json()

},

async saveApplication(){

const res = await fetch(

`${this.$apiBase}/company/application/${this.$route.params.driveId}/${this.$route.params.studentId}`,

{

method:"PUT",

credentials:"include",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

result:this.application.result,

mode:this.application.mode,

interview_date:this.application.interview_date

})

})

const data = await res.json()

alert(data.message)

}

}

}
</script>