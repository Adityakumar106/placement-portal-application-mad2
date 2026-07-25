<template>

<div class="d-flex">

<div
class="bg-primary text-white vh-100 p-3"
style="width:250px"
>

<h3 class="text-center mb-4">

Company

</h3>

<router-link
class="nav-link text-white mb-2"
to="/company/dashboard"
>

Dashboard

</router-link>

<router-link
class="nav-link text-white mb-2"
to="/company/profile"
>

Profile

</router-link>

<router-link
class="nav-link text-white mb-2"
to="/company/drives"
>

My Drives

</router-link>

<router-link
class="nav-link text-white mb-2"
to="/company/create-drive"
>

Create Drive

</router-link>



</div>

<div class="flex-grow-1">

<nav class="navbar navbar-light bg-light shadow-sm px-4">

<h4>

Company Dashboard

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