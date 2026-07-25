<template>
<div class="container mt-4">

<div class="card shadow">

<div class="card-header bg-primary text-white">
<h3>{{ drive.title }}</h3>
</div>

<div class="card-body">

<div class="row mb-3">

<div class="col-md-6">
<b>Company</b>
<p>{{ drive.company }}</p>
</div>

<div class="col-md-6">
<b>Job Title</b>
<p>{{ drive.job_title }}</p>
</div>

</div>

<div class="mb-3">
<b>Description</b>
<p>{{ drive.description }}</p>
</div>

<div class="row">

<div class="col-md-4">
<b>Eligibility</b>
<p>{{ drive.eligibility }}</p>
</div>

<div class="col-md-4">
<b>Salary</b>
<p>{{ drive.salary }}</p>
</div>

<div class="col-md-4">
<b>Deadline</b>
<p>{{ drive.deadline }}</p>
</div>

</div>

<div class="mt-3">

<b>Status</b>

<p>
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

</p>

</div>

<button
v-if="!drive.applied && drive.status=='open'"
class="btn btn-success me-2"
@click="apply"
>
Apply Now
</button>

<button
v-else
disabled
class="btn btn-secondary me-2"
>
Applied
</button>

<button
class="btn btn-outline-primary"
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

drive:{}

}

},

mounted(){

this.loadDrive()

},

methods:{

async loadDrive(){

const res=await fetch(
`${this.$apiBase}/student/drive/${this.$route.params.id}`,
{
credentials:"include"
})

this.drive=await res.json()

},

async apply(){

const res=await fetch(
`${this.$apiBase}/student/apply/${this.$route.params.id}`,
{
method:"POST",
credentials:"include"
})

const data=await res.json()

alert(data.message)

this.loadDrive()

}

}

}
</script>