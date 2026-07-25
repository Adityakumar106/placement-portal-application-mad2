<template>

<div class="container mt-4">

<div class="card shadow">

<div class="card-header bg-primary text-white">
<h3 class="mb-0">My Applications</h3>
</div>

<div class="card-body">

<table class="table table-bordered table-hover">

<thead class="table-light">

<tr>

<th>Drive Name</th>
<th>Company</th>

<th>Status</th>
<th>Action</th>

</tr>

</thead>

<tbody>

<tr
v-for="app in applications"
:key="app.id"
>

<td>{{ app.drive }}</td>

<td>{{ app.company }}</td>

<td>
<span class="badge bg-info">
{{ app.status }}
</span>
</td>

<td>

<button
class="btn btn-primary btn-sm"
@click="viewDetails(app.drive_id)"
>
View Details
</button>

</td>

</tr>

<tr v-if="applications.length==0">

<td colspan="5" class="text-center">
No Applications Found
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

applications:[]

}

},

mounted(){

this.loadApplications()

},

methods:{

async loadApplications(){

const res=await fetch(
`${this.$apiBase}/student/applications`,
{
credentials:"include"
})

const data=await res.json()

this.applications=data.applications

},

viewDetails(id){

this.$router.push(`/student/drive/${id}`)

}

}

}
</script>