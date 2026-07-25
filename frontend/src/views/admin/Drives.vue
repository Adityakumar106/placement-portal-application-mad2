<template>

<div>

<h2 class="mb-4">Placement Drives</h2>

<input
v-model="search"
class="form-control mb-3"
placeholder="Search Drive">

<table class="table table-bordered shadow">

<thead class="table-primary">

<tr>

<th>ID</th>
<th>Drive Name</th>
<th>Company</th>
<th>Action</th>

</tr>

</thead>

<tbody>

<tr
v-for="drive in filteredDrives"
:key="drive.id"
>

<td>{{ drive.id }}</td>

<td>{{ drive.title }}</td>

<td>{{ drive.company }}</td>

<td>

<button
class="btn btn-primary btn-sm me-2"
@click="viewDetails(drive.id)"
>
View Details
</button>

<button
v-if="drive.status=='open'"
class="btn btn-success btn-sm"
@click="completeDrive(drive.id)"
>
Mark as Completed
</button>

<button
v-else
class="btn btn-secondary btn-sm"
disabled
>
Completed
</button>

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

drives:[],
search:""

}

},

computed:{

filteredDrives(){

return this.drives.filter(d=>
d.title.toLowerCase().includes(this.search.toLowerCase())
)

}

},

mounted(){

this.loadDrives()

},

methods:{

async loadDrives(){

const res=await fetch(
`${this.$apiBase}/admin/drives`,
{
credentials:"include"
})

const data=await res.json()

this.drives=data.drives

},

viewDetails(id){

this.$router.push(`/admin/drive/${id}`)

},

async completeDrive(id){

await fetch(
`${this.$apiBase}/admin/drive/${id}/complete`,
{
method:"POST",
credentials:"include"
})

this.loadDrives()

}

}

}
</script>