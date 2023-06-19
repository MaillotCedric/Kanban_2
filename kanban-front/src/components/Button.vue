<template>
    <button :class="type"><slot /></button>
</template>
<script lang="ts">
    export default {
        name: 'Button',
        props: [ 'type' ]
    }
</script>
