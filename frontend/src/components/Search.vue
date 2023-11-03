<script setup>

import SearchInput from "@/components/SearchInput.vue";
import SearchResults from "@/components/SearchResults.vue";
import { ref } from 'vue';

const searchResults = ref([]);

const updateResults = (results) => {
  searchResults.value = results;
}
</script>

<template>
  <div class="search">
    <SearchInput @searched="updateResults" />

    <SearchResults  :results="searchResults"/>
  </div>
</template>

<style scoped>

</style>