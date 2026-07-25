<template>

<div class="container mt-4">

<div class="card shadow">

<div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">

<h3 class="mb-0">
Placement History
</h3>

<div>

<button
class="btn btn-light"
@click="exportApplications"
:disabled="isExporting"
>

<span
v-if="isExporting"
class="spinner-border spinner-border-sm me-2"
></span>

{{ isExporting ? "Exporting..." : "Export CSV" }}

</button>

</div>

</div>

<div class="card-body">

<div
v-if="exportMessage"
class="alert alert-info"
>

{{ exportMessage }}

</div>

<table class="table table-bordered table-hover">

<thead class="table-light">

<tr>

<th>Drive Name</th>
<th>Company</th>
<th>Interview Mode</th>
<th>Interview Date</th>
<th>Result</th>

</tr>

</thead>

<tbody>

<tr
v-for="item in history"
:key="item.id"
>

<td>{{ item.drive }}</td>

<td>{{ item.company }}</td>

<td>{{ item.interview_mode }}</td>

<td>{{ item.interview_date }}</td>

<td>

<span
v-if="item.result=='Selected'"
class="badge bg-success"
>
Selected
</span>

<span
v-else-if="item.result=='Rejected'"
class="badge bg-danger"
>
Rejected
</span>

<span
v-else
class="badge bg-warning text-dark"
>
Waiting
</span>

</td>

</tr>

<tr v-if="history.length==0">

<td colspan="5" class="text-center">
No Placement History Available
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

history:[],
isExporting:false,
exportMessage:""

}

},

mounted(){

this.loadHistory()

},

methods:{

async loadHistory(){

const res = await fetch(
`${this.$apiBase}/student/history`,
{
credentials:"include"
}
)

const data = await res.json()

this.history = data.history

},

async exportApplications(){

this.isExporting = true

this.exportMessage = "Starting export..."

try{

const res = await fetch(
`${this.$apiBase}/student/export_applications`,
{
method:"POST",
credentials:"include"
}
)

const data = await res.json()

if(!res.ok){

this.exportMessage = data.message
this.isExporting = false
return

}

this.exportMessage = "Waiting for CSV generation..."

this.pollExport(data.job_id)

}

catch(error){

this.exportMessage = "Unable to start export."

this.isExporting = false

}

},

pollExport(jobId){

const timer = setInterval(async()=>{

try{

const res = await fetch(
`${this.$apiBase}/student/export/status/${jobId}`,
{
credentials:"include"
}
)

const data = await res.json()

if(data.status==="Pending"){

this.exportMessage="Waiting in queue..."

}

else if(data.status==="Processing"){

this.exportMessage="Generating CSV..."

}

else if(data.status==="Completed"){

clearInterval(timer)

this.exportMessage="Download started..."

this.isExporting=false

window.location.href=
`${this.$apiBase}/student/export/download/${jobId}`

}

else if(data.status==="Failed"){

clearInterval(timer)

this.exportMessage="Export Failed"

this.isExporting=false

}

}

catch(error){

clearInterval(timer)

this.exportMessage="Unable to check export status."

this.isExporting=false

}

},1000)

}

}

}

</script>