<template>

<div class="d-flex">

<div
class="bg-success text-white vh-100 p-3"
style="width:250px"
>

<h3 class="text-center mb-4">

Student

</h3>

<router-link
class="nav-link text-white mb-2"
to="/student/dashboard"
>

Dashboard

</router-link>

<router-link
class="nav-link text-white mb-2"
to="/student/profile"
>

Profile

</router-link>

<router-link
class="nav-link text-white mb-2"
to="/student/applications"
>

Applications

</router-link>

<router-link
class="nav-link text-white mb-2"
to="/student/history"
>

History

</router-link>

</div>

<div class="flex-grow-1">

<nav class="navbar navbar-light bg-light shadow-sm px-4">

<h4>

Student Dashboard

</h4>

<button
class="btn btn-danger"
@click="logout"
>

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