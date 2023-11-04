<template>
  <div style="display: flex; flex-direction: row">
    <div style="flex-grow: 1"></div>
    <h1 style="color: #181818; font-size: 30px; flex: 1">Chat with {{ fullName }}</h1>
    <img :src="avatar" style="width: 80px; height: 80px;">
    <div style="flex-grow: 1"></div>
  </div>
  <div style="flex: 1">
    <div style="width: 100%; max-height: 600px; flex-grow: 1; display: flex">

      <div v-if="loading">
        <h2>Loading!</h2>
      </div>

      <deep-chat
          v-if="!loading"
          ref="chatRef"
          :style="{ width: '100%', height: '100%'}"
          :demo="false"
          :textInput="{ placeholder: { text: 'PLease continue your story!' } }"
          :initialMessages="initialMessages"
          :request="{url: 'http://localhost:5000/chat'}"
          :stream="false"
      />
    </div>
  </div>
  <div style="max-height: 300px; flex: 1; overflow: auto; display: flex">
    <div v-if="loadingExtra" style="flex: 1;">
      <h2>Loading extra content. Be patient please!</h2>
    </div>
    <div v-else style="flex: 1; display: flex; flex-wrap: wrap">
      <img v-for="image in images" :key="image" :src="image['imageOriginal']"
           style=" object-fit: contain; flex: 1; max-width: 350px; max-height: 350px"/>
    </div>
  </div>
</template>

<script setup>
import "deep-chat";
import {ref, onMounted, nextTick, defineProps, computed, watch} from 'vue';
import axios from "axios";

const props = defineProps({
  person: {
    type: Object,
    required: true,
  },
  person_name: {
    type: String,
    required: true,
  },
});


const images = ref([])
const messages = ref([])
const chatRef = ref(null)
const loading = ref(true);
const loadingExtra = ref(false);
const initialMessages = ref([])


const fullName = computed(() => {
  return `${props.person.person.name_first} ${props.person.person.surname}`
})

const avatar = computed(() => {
  return props.person_name + '.png'
})


// {url: 'http://localhost:5000/openai-chat-stream'}


onMounted(() => {
  console.log(chatRef)

  console.log('promps', props.person.person)


  fetchInitialMessage(props.person)

})

watch(() => props.person.person.surname + props.person.person.name_first, async (newQuestion, oldQuestion) => {
  if (newQuestion !== oldQuestion) {
    console.log('new question', newQuestion)
    await fetchInitialMessage(props.person)
  }
})


const fetchInitialMessage = async (person) => {
  loading.value = true;

  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [
        {
          story_page_data: person
        }
      ]
    })
  });

  const data = await response.json();
  initialMessages.value = [
    {role: "ai", text: data.text},
  ];
  messages.value = [
    {
      role: "ai", text: data.text,
      story_page_data: person
    },
  ]
  loading.value = false;

  extractRelevantImages(data.text)

  await nextTick(() => {
    hookOnChat()
  })
}


const extractRelevantImages = async (text) => {
  loadingExtra.value = true;
  // Call post to backend
  const response = await axios.post('http://localhost:5000/extract_images', {passage: text});

  images.value = response.data['images'];
  loadingExtra.value = false;
  console.log('Response from backend:', response.data);
}

const hookOnChat = () => {
  chatRef.value.requestInterceptor = async (requestDetails) => {
    requestDetails.body.story_page_data = props.person

    messages.value.push({
      role: "user", text: requestDetails.body.messages[0].text
    });

    requestDetails.body.messages = messages.value

    console.log('Requesting ', requestDetails);
    return requestDetails;
  };

  chatRef.value.responseInterceptor = async (responseDetails) => {
    messages.value.push({
      role: "ai", text: responseDetails.text
    });

    // responseDetails.html = '<b>hello world---------</b>'
    // responseDetails.textz = responseDetails.text
    // responseDetails.text = undefined
    console.log('Response ', responseDetails);

    extractRelevantImages(responseDetails.text)

    return responseDetails;
  };


  chatRef.value.onNewMessage = (response) => {
    console.log(response, 'onNewMessage');
  };
}


</script>

<style>
div {
  font-family: sans-serif;
  text-align: center;
  justify-content: center;
  display: grid;
}
</style>
