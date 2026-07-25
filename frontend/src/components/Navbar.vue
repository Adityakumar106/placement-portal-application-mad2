<template>

<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

<div class="container">

<router-link
class="navbar-brand fw-bold"
to="/">

Placement Portal

</router-link>

<button
class="navbar-toggler"
data-bs-toggle="collapse"
data-bs-target="#nav">

<span class="navbar-toggler-icon"></span>

</button>

<div
id="nav"
class="collapse navbar-collapse">

<ul class="navbar-nav ms-auto">

<li class="nav-item">

<router-link
to="/"
class="nav-link">

Home

</router-link>

</li>

<li class="nav-item">

<router-link
to="/login"
class="nav-link">

Login

</router-link>

</li>

<li class="nav-item">

<router-link
to="/register"
class="nav-link">

Register

</router-link>

</li>

</ul>

</div>

</div>

</nav>

</template>

<script>

export default{

name:"Navbar"

}

</script>