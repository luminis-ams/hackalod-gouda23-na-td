<script setup>

import ActionItem from "@/components/ActionItem.vue";
import { defineProps } from 'vue';

// Define the props for this component
const props = defineProps({
  person: {
    type: Object,
    default: () => {}
  }
});

const changeActiveItem = (item) => {
  console.log(item);
  emit('active-item', item);
}

const emit = defineEmits();
</script>

<template>
  <div class="vertical-bar-inside">
    <ActionItem @click="changeActiveItem('my-face')">
      <template #image>
        <img src="/01_Nav_pos1.png" alt="Logo" />
      </template>
    </ActionItem>
    <ActionItem @click="changeActiveItem('my-events')">
      <template #image>
        <img src="/01_Nav_pos2.png" alt="Logo" />
      </template>
    </ActionItem>
    <ActionItem @click="changeActiveItem('my-picts')">
      <template #image>
        <img src="/01_Nav_pos3.png" alt="Logo" />
      </template>
    </ActionItem>
    <ActionItem @click="changeActiveItem('my-routes')">
      <template #image>
        <img src="/01_Nav_pos4.png" alt="Logo" />
      </template>
    </ActionItem>
    <ActionItem @click="changeActiveItem('my-story')">
      <template #image>
        <img src="/01_Nav_pos5.png" alt="Logo" />
      </template>
    </ActionItem>
    <ActionItem @click="changeActiveItem('my-chat')">
      <template #image>
        <img src="/01_Nav_pos6.png" alt="Logo" />
      </template>
    </ActionItem>
  </div>
</template>

<style scoped>
.vertical-bar-inside img {
  width: 100px;
  object-fit: contain;
}
</style>