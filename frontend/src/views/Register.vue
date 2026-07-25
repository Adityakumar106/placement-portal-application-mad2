<template>

<div class="container vh-100 d-flex justify-content-center align-items-center">

<div class="card shadow p-4 register-card">

<h2 class="text-center text-success mb-4">

Create Account

</h2>

<div
v-if="message"
class="alert alert-success">

{{message}}

</div>

<div
v-if="error"
class="alert alert-danger">

{{error}}

</div>

<form @submit.prevent="registerUser">

<div class="mb-3">

<label>Username</label>

<input
v-model="username"
class="form-control"
type="text"
required>

</div>

<div class="mb-3">

<label>Email</label>

<input
v-model="email"
class="form-control"
type="email"
required>

</div>

<div class="mb-3">

<label>Password</label>

<input
v-model="password"
class="form-control"
type="password"
required>

</div>

<div class="mb-4">

<label>Select Role</label>

<select
v-model="role"
class="form-select">

<option value="student">
Student
</option>

<option value="company">
Company
</option>

</select>

</div>

<button
class="btn btn-success w-100"
:disabled="loading">

{{loading ? "Registering..." : "Register"}}

</button>

</form>

<hr>

<p class="text-center">

Already have an account?

<router-link to="/login">

Login

</router-link>

</p>

</div>

</div>

</template>

<script>

export default{

data(){

return{

username:"",
email:"",
password:"",
role:"student",

loading:false,
message:"",
error:""

}

},

methods:{

async registerUser(){

this.loading=true

this.message=""
this.error=""

try{

const response=await fetch(`${this.$apiBase}/register`,{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

username:this.username,
email:this.email,
password:this.password,
role:this.role

})

})

const data=await response.json()

if(response.ok){

this.message=data.message

this.username=""
this.email=""
this.password=""
this.role="student"

setTimeout(()=>{

this.$router.push("/login")

},1000)

}else{

this.error=data.message

}

}catch{

this.error="Server connection failed."

}

this.loading=false

}

}

}

</script>

<style scoped>

.register-card{

width:450px;
border-radius:15px;

}

</style>