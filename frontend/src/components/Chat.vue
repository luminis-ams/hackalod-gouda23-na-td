<template>
  <h1 style="color: #181818; font-size: 30px">Chat with the Crewman</h1>
  <div style="flex: 1">
    <div style="width: 100%; flex-grow: 1; display: flex">

      <div v-if="loading">
        <h2>Loading!</h2>
      </div>

      <deep-chat
          v-if="!loading"
          ref="chatRef"
          :style="{ width: '100%', height: '100%'}"
          :demo="false"
          :textInput="{ placeholder: { text: 'Welcome to the demo!' } }"
          :initialMessages="initialMessages"
          :request="{url: 'http://localhost:5000/chat'}"
          :stream="false"
          :avatars="true"
          :names="true"
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
import {ref, onMounted, nextTick, defineProps} from 'vue';
import axios from "axios";

const props = defineProps({
  person: {
    type: Object,
    required: true,
  },
});


const images = ref([])
const messages = ref([])
const chatRef = ref(null)
const loading = ref(true);
const loadingExtra = ref(false);
const initialMessages = ref([])

// {url: 'http://localhost:5000/openai-chat-stream'}

const initialInformation = {
  "person": {
    "surname": "A. Buijs",
    "name_first": "Antoon",
    "father": "Martinus",
    "mother": "Philomena Pauwels",
    "birth_place": "Burght /Belgie/",
    "birth_data": "13 Juni 1877",
    "place_of_residence": "Burght",
    "length": "1.57 Meter",
    "face": "ovaal",
    "forehead": "gewoon",
    "eyes": "blauw",
    "nose": "gewoon",
    "mouth": "idem",
    "chin": "rond",
    "hair": "bruin",
    "eyebrow": "id",
    "features_particular": "getu toueerd aan beide ar men en rechterhand"
  },
  "events": [
    {"event_date": "1900-03-11", "description": "d bij o Monsieur le présent"},
    {"event_date": "1900-03-09", "description": "Van verlof achtergebleven"},
    {
      "event_date": "1901-11-21",
      "description": "Als deserteur afgevoerd. Heeft zich den 24e Juli 1901 vrijwillig aangemeld. Bij vonnis van den krygsraad in het 3e Militaire Arron dissement dd: 14 Augustus 1901, ingegaan den 23e Augustus das vervordeeld tot drie maanden militaire detentie, te zake van eerste desertie in tijd van vrede, door zonder ver lof langer dan twee dager van zijn korps afwe nig te zijn gebleven, zonder de reden zijner afwezigheid te genoegen des rechters te bewijzen, niet t of gevolgd door vrijwillige te rugkeer binnen vier weken weder in de sterkte gebracht, zie N=o 4457"
    },
    {
      "event_date": "1901-11-22",
      "description": "Vrijwillig geëngageerd als soldaat ('elve tamboer) voor zes jaren bij het leger zooveel in als buiten Europa met ƒ300-premie, waarvan ƒ50- uitbetaald en f 250 - in Rijkspostspaarbank ingelegd is. Ingevolge beschikking van het D v. C. dd 18 November 1901, Afd Pers n:o 10 To oldaat"
    },
    {
      "event_date": "1902-09-30",
      "description": "Geditacheerd naar Oost-Indië en op dato te Amsterdam overgegaan aan boord 2/4 S.S. Teins Hendrik\""
    },
    {"event_date": "1902-10-25", "description": "Overgegaar bij het 1 Bat=on Inf"},
    {"event_date": "1902-12-01", "description": "Garn. Batn. van Palemburg"},
    {"event_date": "1903-03-29", "description": "R.H. 15. Bat-m Infin."},
    {
      "event_date": "1903-04-23",
      "description": "4: 12: 18: Bestemd van uiterlijk 2 maanden voor het eindige vier dienst verbintenis naar Nederland te worden opgezoorden"
    },
    {
      "event_date": "1904-07-30",
      "description": "Is niet genegen zich te zier gogeere, zou des verkeerende tot een zesjarig reengagement zijn toegelaten"
    },
    {"event_date": "1904-12-24", "description": "derwaarts vertrokken met het P. Koningin Wilhelmina"},
    {"event_date": "1906-06-28", "description": "Ontscheept te Amsterdam en op dato terug in de sterkte Jh Corf"}
  ]
}


onMounted(() => {
  console.log(chatRef)

  fetchInitialMessage()

})

const fetchInitialMessage = async () => {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [
        {
          story_page_data: initialInformation
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
      story_page_data: initialInformation
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
    requestDetails.body.initial_information = initialInformation

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
