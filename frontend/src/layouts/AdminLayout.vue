<template>

<div class="d-flex">

   

    <div class="bg-dark text-white p-3 vh-100" style="width:250px">

        <h3 class="text-center mb-4">
            Admin
        </h3>

        <router-link class="nav-link text-white mb-2" to="/admin/dashboard">
            Dashboard
        </router-link>

        <router-link class="nav-link text-white mb-2" to="/admin/students">
            Students
        </router-link>

        <router-link class="nav-link text-white mb-2" to="/admin/companies">
            Companies
        </router-link>

        <router-link class="nav-link text-white mb-2" to="/admin/drives">
            Drives
        </router-link>

        <router-link class="nav-link text-white mb-2" to="/admin/applications">
            Applications
        </router-link>

        

    </div>


    <div class="flex-grow-1">

        <nav class="navbar navbar-light bg-white shadow-sm px-4">

            <h4>Admin Dashboard</h4>

            <button
                class="btn btn-danger"
                @click="logout">

                Logout

            </button>

        </nav>

        <div class="container py-4">

            <router-view/>

        </div>

    </div>

</div>

</template>

<script>

export default{

methods:{

async logout(){

await fetch(
`${this.$apiBase}/logout`,
{
credentials:"include"
})

this.$router.push("/login")

}

}

}

</script>