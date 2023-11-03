<script setup>
import {ref} from "vue";
import axios from "axios";

const query = ref("");
const searchResults = ref([]);

const executeSearch = async () => {
  console.log("executeSearch");

// Method to call the backend with the search query
  try {
    const requestBody = {
      search_for: query.value,
    };
    const response = await axios.post('http://localhost:5000/search_image', requestBody);
    searchResults.value = response.data;
    emit('searched', searchResults.value);
  } catch (error) {
    console.error('Search error:', error);
  }
};

const emit = defineEmits();
</script>

<template>
  <div>
    <input v-model="query" placeholder="Enter search term..."/>
    <button @click="executeSearch">Search</button>
  </div>
</template>

<style scoped>

</style>