<script setup>

import {computed} from "vue";

const props = defineProps({
  person_name: {
    type: String,
    required: true,
  },
  startDate: String,
  endDate: String,
});

const person_picture = computed(() => {
  console.log(props.person_name);
  return props.person_name + '.png';
});

</script>

<template>
  <div class="medallion">
        <img :src="person_picture" alt="Descriptive text for accessibility">
  </div>
</template>

<style scoped>
.medallion {
  position: relative;
  margin: 105px 2px 150px 2px;
  height: 400px;
  background-color: #fff;
  flex: 1;
  padding: 50px;
}

.medallion img {
  width: 500px;
  object-fit: contain;
}
</style>