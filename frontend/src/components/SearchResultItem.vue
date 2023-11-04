<script setup>
import { defineProps } from 'vue';

// Define the props for this component
const props = defineProps({
  result: {
    type: Object,
    default: () => {}
  }
});

</script>

<template>
  <li :key="result"><img :src="result.imageOriginal" alt="Descriptive text for accessibility">{{ result.beschrijving }}</li>
<!--  <li :key="result">{{ result }}</li>-->
</template>

<style scoped>

</style>