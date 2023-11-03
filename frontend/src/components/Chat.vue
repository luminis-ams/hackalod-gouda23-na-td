<template>
  <h1>Chat with GPT</h1>
  <div style="width: 100%; height: 500px; display: flex">
    <deep-chat
        :style="{ width: '100%', height: '100%'}"
        :demo="false"
        :textInput="{ placeholder: { text: 'Welcome to the demo!' } }"
        :initialMessages="initialMessages"
        :request="{url: 'http://localhost:5000/openai-chat-stream'}"
        :stream="true"
    />
  </div>

</template>

<script>
import "deep-chat";

export default {
  name: "App",
  data() {
    return {
      initialMessages: [
        {role: "ai", text: "I am your AI historian. How can I help you?."},
      ],
      request: {url: 'http://localhost:5000/openai-chat'},
    };
  },
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
