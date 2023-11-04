<script setup>
import ActionBar from "@/components/ActionBar.vue";
import InvisibleItem from "@/components/InvisibleItem.vue";
import {ref} from "vue";
import axios from "axios";
import Timeline from "@/components/Timeline.vue";
import Chat from "@/components/Chat.vue";

const activeItem = ref('')
const activePerson = ref({})
const activeAction = ref('')

const activateContent = (item) => {
  activeItem.value = item;
  console.log("Toggling content:" + activeItem.value);
  executeSearchPerson();
}

const executeSearchPerson = async () => {
  console.log("executeSearch");

  try {
    const requestBody = {
      person_name: activeItem.value,
    };
    const response = await axios.post('http://localhost:5000/search_person', requestBody);
    activePerson.value = response.data;
  } catch (error) {
    console.error('Search error:', error);
  }
};

const selectActiveItem = (active_item) => {
  console.log("active action: " + active_item);
  activeAction.value = active_item;
}


</script>

<template>
  <div class="container">
    <div class="invisible-bar" >
      <InvisibleItem @click="activateContent('one')">
        <template #image>
          <img src="/02_Naam1_ON.png" alt="Logo" :class="activeItem=='one' ? 'active':''"/>
        </template>
      </InvisibleItem>
      <InvisibleItem @click="activateContent('two')">
        <template #image>
          <img src="/02_Naam2_ON.png" alt="Logo" :class="activeItem=='two' ? 'active':''"/>
        </template>
      </InvisibleItem>
      <InvisibleItem @click="activateContent('three')">
        <template #image>
          <img src="/02_Naam3_ON.png" alt="Logo" :class="activeItem=='three' ? 'active':''"/>
        </template>
      </InvisibleItem>
      <InvisibleItem @click="activateContent('four')">
        <template #image>
          <img src="/02_Naam4_ON.png" alt="Logo" :class="activeItem=='four' ? 'active':''"/>
        </template>
      </InvisibleItem>
    </div>
    <div class="vertical-bar">
      <ActionBar :person="activePerson" @active-item="selectActiveItem"/>
    </div>
    <div class="main-content">
      <Timeline :person="activePerson" :start-date="'1890-01-01'" :end-date="'1910-12-31'" v-if="activeAction=='my-events'"/>
      <Chat  :person="activePerson" v-if="activeAction=='my-chat'"/>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  height: 100vh; /* Use full viewport height */
  width: 100vw; /* Use full viewport width */
  background-image: url('/03_Background_DARK.png'); /* Set a background image */
  background-size: initial;
  background-repeat: no-repeat;
}

.invisible-bar {
  padding-top: 165px;
  padding-left: 220px;
  flex-basis: 300px; /* Set the width of the invisible bar */
  cursor: pointer;
  display: block;
}

.vertical-bar {
  flex-basis: 100px; /* Set the width of the vertical bar */
  //display: flex;
  display: block;
  flex-direction: column;
  align-items: center;
}

.invisible-bar img {
  height: 170px;
  object-fit: contain;
  opacity: 0;
}

.invisible-bar img.active {
  opacity: 1;
}


.main-content {
  flex-grow: 1; /* Use remaining space */
  padding: 20px;
  display: flex;
  flex-direction: column;
}
</style>
