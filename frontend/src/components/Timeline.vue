<script setup>
import { defineProps, defineEmits, ref, computed } from 'vue';
import { differenceInCalendarDays, parseISO } from 'date-fns';
import {eventBus} from "@/components/eventBus";


const props = defineProps({
  person: {
    type: Object,
    required: true,
  },
  startDate: String,
  endDate: String,
});


const emitMoment = (moment) => {
  eventBus.emit('moment-clicked', moment);
};

const totalDays = computed(() => {
  return differenceInCalendarDays(parseISO(props.endDate), parseISO(props.startDate));
});

const getPosition = (time) => {
  const daysFromStart = differenceInCalendarDays(parseISO(time), parseISO(props.startDate));
  return (daysFromStart / totalDays.value) * 100;
};
</script>

<template>
  <div class="timeline-container">
    <!-- Timeline -->
    <div class="timeline-line"></div>
    <!-- Timeline moments -->
    <div v-for="(moment, index) in person.events" :key="index" class="timeline-moment" @click="() => emitMoment(moment)" :style="{ left: getPosition(moment.event_date) + '%' }">
      <!-- Circle on the timeline -->
      <div class="timeline-circle"></div>
      <!-- Content for the moment -->
      <div class="content">
        <!-- Conditionally display image or text based on the moment's content -->
        <img v-if="moment.image" :src="moment.image" :alt="moment.description">
        <span v-else>{{ moment.description }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.timeline-container {
  position: relative;
  margin: 20px;
  height: 200px;
}

.timeline-line {
  position: absolute;
  height: 4px;
  width: 100%;
  background-color: #333;
  top: 20px; /* Adjust to align with the center of circles */
}

.timeline-moment {
  position: absolute;
  cursor: pointer;
}

.timeline-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #555;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.content {
  margin-top: 60px;
  text-align: center;
}

.content img {
  max-width: 100px;
  border-radius: 50%;
}

.content span {
  display: block;
}
</style>
