<template>

<div class="card shadow">

<div class="card-body">

<h3>

Company Profile

</h3>

<form @submit.prevent="saveProfile">

<div class="mb-3">

<label>Company Name</label>

<input
v-model="company.Companyname"
class="form-control">

</div>

<div class="mb-3">

<label>HR Contact</label>

<input
v-model="company.hrcontact"
class="form-control">

</div>

<div class="mb-3">

<label>Website</label>

<input
v-model="company.website"
class="form-control">

</div>

<button class="btn btn-primary">

Save

</button>

</form>

</div>

</div>

</template>

<script>

export default{

data(){

return{

company:{}

}

},

mounted(){

this.loadProfile()

},

methods:{

async loadProfile(){

const res=await fetch(
`${this.$apiBase}/company/profile`,
{
credentials:"include"
})

this.company=await res.json()

},

async saveProfile(){

await fetch(
`${this.$apiBase}/company/profile`,
{

method:"PUT",

credentials:"include",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(this.company)

})

alert("Profile Updated")

}

}

}

</script>