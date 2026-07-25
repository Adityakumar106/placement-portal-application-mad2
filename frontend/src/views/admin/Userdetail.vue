<template>

<div class="container mt-4">

<div class="card shadow">

<div class="card-header bg-primary text-white">

<h3>Application Details</h3>

</div>

<div class="card-body" v-if="application">

<div class="row mb-3">

<div class="col-md-6">
<label><b>Name</b></label>
<p>{{ application.student.username }}</p>
</div>

<div class="col-md-6">
<label><b>Email</b></label>
<p>{{ application.student.email }}</p>
</div>

</div>

<div class="row mb-3">

<div class="col-md-6">
<label><b>Degree</b></label>
<p>{{ application.student.degree }}</p>
</div>

<div class="col-md-6">
<label><b>Course</b></label>
<p>{{ application.student.course }}</p>
</div>

</div>

<div class="row mb-3">

<div class="col-md-6">
<label><b>Branch</b></label>
<p>{{ application.student.branch }}</p>
</div>

<div class="col-md-6">
<label><b>CGPA</b></label>
<p>{{ application.student.cgpa }}</p>
</div>

</div>

<div class="row mb-3">

<div class="col-md-6">
<label><b>Phone</b></label>
<p>{{ application.student.phone }}</p>
</div>

<div class="col-md-6">
<label><b>LinkedIn</b></label>
<p>{{ application.student.linkedin }}</p>
</div>

</div>

<div class="mb-3">

<label><b>About</b></label>

<p>{{ application.student.about }}</p>

</div>

<a
:href="application.student.resume"
target="_blank"
class="btn btn-success me-2"
>
View Resume
</a>

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

application:null

}

},

mounted(){

this.loadApplication()

},

methods:{

async loadApplication(){

const res = await fetch(
`${this.$apiBase}/admin/application/${this.$route.params.id}`,
{
credentials:"include"
})

const data = await res.json()
this.application = data

}

}

}
</script>