<script setup>
import { defineProps } from 'vue';

// Define the props for this component
const props = defineProps({
  result: {
    type: String,
    default: () => ""
  }
});

</script>

<template>
  <li :key="result">{{ result }}</li>
</template>

<style scoped>

</style>