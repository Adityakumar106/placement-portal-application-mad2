<template>

<div>

<h2 class="mb-4">Dashboard Overview</h2>

<div class="row">

<div class="col-md-3 mb-4">

<div class="card shadow text-center">

<div class="card-body">

<h6>Total Students</h6>

<h2>{{students}}</h2>

</div>

</div>

</div>

<div class="col-md-3 mb-4">

<div class="card shadow text-center">

<div class="card-body">

<h6>Total Companies</h6>

<h2>{{companies}}</h2>

</div>

</div>

</div>

<div class="col-md-3 mb-4">

<div class="card shadow text-center">

<div class="card-body">

<h6>Total Drives</h6>

<h2>{{drives}}</h2>

</div>

</div>

</div>

<div class="col-md-3 mb-4">

<div class="card shadow text-center">

<div class="card-body">

<h6>Applications</h6>

<h2>{{applications}}</h2>

</div>

</div>

</div>

</div>

</div>

</template>

<script>

export default{

data(){

return{

students:0,
companies:0,
drives:0,
applications:0

}

},

mounted(){

this.loadDashboard()

},

methods:{

async loadDashboard(){

const response=await fetch(`${this.$apiBase}/admin/dashboard`,{

credentials:"include"

})

const data=await response.json()

this.students=data.students
this.companies=data.companies
this.drives=data.drives
this.applications=data.applications

}

}

}

</script>