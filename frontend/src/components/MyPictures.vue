<script setup>
import {computed, onMounted, ref, watch} from "vue";
import axios from "axios";

const images = ref([]);

const props = defineProps({
  person: {
    type: Object,
    required: true,
  }
});

const fullName = computed(() => {
  return `${props.person.person.name_first} ${props.person.person.surname}`
})

const executeSearch = async (full_name) => {
  try {
    console.log('Before the request ' + fullName);
    const requestBody = {
      search_for: full_name.toString(),
    };
    console.log('Before the request')
    const response = await axios.post('http://localhost:5000/search_image', requestBody);
    console.log('After the request')
    images.value = response.data;
  } catch (error) {
    console.error('Search error:', error);
  }
};

onMounted(() => {
  executeSearch(fullName)
})

watch(() => props.person.person.surname + props.person.person.name_first, async (newQuestion, oldQuestion) => {
  if (newQuestion !== oldQuestion) {
    console.log('new question', newQuestion)
    await executeSearch(`${props.person.person.name_first} ${props.person.person.surname}`)
  }
})

</script>

<template>
  <div class="my-images">
    <h3>Images for {{fullName}}</h3>
    <img v-for="aImage in images" :key="aImage" :src="aImage['imageOriginal']"
         style=" object-fit: contain; flex: 1; max-width: 350px; max-height: 350px"/>
  </div>
</template>

<style scoped>
.my-images {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  background-color: #fff;
  color: #000;
}
</style>