<template>

<div class="card shadow">

<div class="card-body text-center">

<h6>{{title}}</h6>

<h2>{{count}}</h2>

</div>

</div>

</template>

<script>

export default{

props:[

"title",
"count"

]

}

</script>