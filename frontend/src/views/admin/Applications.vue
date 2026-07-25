<template>

<div>

<h2 class="mb-4">
Applications
</h2>

<table class="table table-striped shadow">

<thead class="table-dark">

<tr>

<th>ID</th>
<th>Student</th>
<th>Company</th>
<th>Drive</th>
<th>Action</th>

</tr>

</thead>

<tbody>

<tr
v-for="app in applications"
:key="app.id"
>

<td>{{ app.id }}</td>

<td>{{ app.student }}</td>

<td>{{ app.company }}</td>

<td>{{ app.drive }}</td>

<td>

<router-link
class="btn btn-primary btn-sm"
:to="`/admin/application/${app.id}`"
>
View Details
</router-link>

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

const response = await fetch(
`${this.$apiBase}/admin/applications`,
{
credentials:"include"
})

const data = await response.json()

this.applications = data.applications || []

}

}

}
</script>