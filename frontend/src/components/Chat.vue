<template>
  <h1>Chat with GPT</h1>
  <div style="width: 100%; height: 250px; display: flex">
    <deep-chat
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

</template>

<script>
import "deep-chat";
import {ref} from "vue";

const chatRef = ref(null)

// {url: 'http://localhost:5000/openai-chat-stream'}


export default {
  name: "App",

  setup() {


    return {
      chatRef,
    };
  },

  data() {
    return {
      initialMessages: [
        {role: "ai", text: "I am your AI historian. How can I help you?."},
      ],
      request: {url: 'http://localhost:5000/openai-chat'},
    };
  },

  mounted() {
    console.log(chatRef)
    chatRef.value.requestInterceptor = async (requestDetails) => {
      console.log(requestDetails); // printed above
      // const otherTask = await fetch('http://localhost:8080/other-task');
      // if (!otherTask.ok) {
      //   return {error: 'Error in other task'};
      // }
      return requestDetails;
    };

    chatRef.value.onNewMessage = (response) => {
      console.log(response, 'onNewMessage');
      response.message.text = 'hello owlrd'
    };

    chatRef.value.responseInterceptor = async (responseDetails) => {

      console.log(responseDetails, 'dsfsjdhflsdf'); // printed above
      responseDetails.text = 'hello world---------'
      return responseDetails;
    };

    console.log('response')
    // chatRef.value.request = {
    //   handler: (body, signals) => {
    //     try {
    //       // this is PSEUDO CODE for creating a stream
    //       fetchEventSource('custom-url', {
    //         async onopen(response) {
    //           if (response.ok) {
    //             signals.onOpen(); // stops the loading bubble
    //           } else {
    //             signals.onResponse({error: 'error'}); // displays an error message
    //           }
    //         },
    //         onmessage(message) {
    //           signals.onResponse({text: message}); // adds text into the message bubble
    //         },
    //         onerror(message) {
    //           signals.onResponse({error: message}); // displays an error message
    //         },
    //         onclose() {
    //           signals.onClose(); // The stop button will be changed back to submit button
    //         },
    //       });
    //       // triggered when the user clicks the stop button
    //       signals.stopClicked.listener = () => {
    //         // logic to stop your stream, such as creating an abortController
    //       };
    //     } catch (e) {
    //       signals.onResponse({error: 'error'}); // displays an error message
    //     }
    //   },
    // };


  }
};


</script>

<style>
div {
  font-family: sans-serif;
  text-align: center;
  justify-content: center;
  display: grid;
}
</style>
