<script setup>
import { ref } from "vue";

const query = ref("");
const executeSearch = () => {
  console.log("executeSearch");
  // Simulating a search operation
  const results = ["Result 1", "Result 2"]; // This would typically come from an API call or similar.
  emit('searched', results);
};

const emit = defineEmits();
</script>

<template>
  <div>
    <input v-model="query" placeholder="Enter search term..." />
    <button @click="executeSearch">Search</button>
  </div>
</template>

<style scoped>

</style>