<script setup>

</script>

<template>
  <div class="item">
    <span class="image">
      <slot name="image"></slot>
    </span>
  </div>
</template>

<style scoped>
.item {
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>