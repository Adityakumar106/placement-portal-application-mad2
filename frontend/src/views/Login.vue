<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">

    <div class="card shadow p-4 login-card">

      <h2 class="text-center mb-4 text-primary">
        Placement Portal
      </h2>

      <div v-if="message" class="alert alert-success">
        {{ message }}
      </div>

      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <form @submit.prevent="loginUser">

        <div class="mb-3">
          <label>Email</label>

          <input
            v-model="email"
            type="email"
            class="form-control"
            placeholder="Enter Email"
            required
          >
        </div>

        <div class="mb-4">
          <label>Password</label>

          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Enter Password"
            required
          >
        </div>

        <button
          class="btn btn-primary w-100"
          :disabled="loading"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>

      </form>

      <hr>

      <p class="text-center">

        Don't have an account?

        <router-link to="/register">
          Register
        </router-link>

      </p>

    </div>

  </div>
</template>

<script>

export default{

data(){

return{

email:"",
password:"",
message:"",
error:"",
loading:false

}

},

methods:{

async loginUser(){

this.loading=true
this.message=""
this.error=""

try{

const response=await fetch(`${this.$apiBase}/login`,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

credentials:"include",

body:JSON.stringify({

email:this.email,
password:this.password

})

})

const data=await response.json()

if(response.ok){

this.message=data.message

if(data.role=="admin"){

this.$router.push("/admin/dashboard")

}

else if(data.role=="student"){

this.$router.push("/student/dashboard")

}

else if(data.role=="company"){

this.$router.push("/company/dashboard")

}

}else{

this.error=data.message

}

}catch{

this.error="Unable to connect to server."

}

this.loading=false

}

}

}

</script>

<style scoped>

.login-card{

width:420px;
border-radius:15px;

}

</style>