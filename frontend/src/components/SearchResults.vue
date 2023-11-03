<script setup>
import { defineProps } from 'vue';
import SearchResultItem from "@/components/SearchResultItem.vue";

// Define the props for this component
const props = defineProps({
  results: {
    type: Array,
    default: () => []
  }
});
</script>

<template>
  <div>
    <ul v-if="results.length">
      <SearchResultItem v-for="result in results" :result="result"/>
    </ul>
    <p v-else>No results found.</p>
  </div>
</template>

<style scoped>

</style>