
<script lang="ts" setup>
import { ref, type Ref, onMounted } from 'vue';

import WebSocketService from '../services/socket';

const socket: Ref<WebSocketService|null> = ref(null);

const chatMessagesEle = ref()
const message = ref('');
const messages = ref<{ owner: 'bot'|'self', message: any }[]>([]);
const sendMessage = () => {
  socket.value?.send(message.value);

  messages.value.push({ owner: 'self', message: message.value });

  message.value = ''
};

function handleOpenMessage() {
  messages.value.push({ owner: 'bot', message: 'Sie wünschen?' });
}

function handleMessageSend(event: MessageEvent) {
  console.log('event', event.data);
  messages.value.push({ owner: 'bot', message: event.data });
}

onMounted(() => {
  socket.value = new WebSocketService('ws://localhost:5002', {
    onopen: handleOpenMessage,
    onmessage: handleMessageSend
  })

  // if(!socket.value || (socket.value && !socket.value.socket)) {
  //   console.error('Failed to connect to the server');
  //   return;
  // }

  // (socket.value.socket as WebSocket).onopen = handleOpenMessage
  // (socket.value.socket as WebSocket).onmessage = handleMessageSend
});
</script>

<template>
  <div class="chat">
    <div class="chat-messages" ref="chatMessagesEle">
      <!-- Display chat messages here -->
      <div
        :class="{
            'chat-message--self': msg.owner === 'self',
            'chat-message--bot': msg.owner === 'bot'
          }"
        v-for="(msg, index) in messages"
        :key="index"
      >
        <span
          class="chat-message"
        >{{ msg.message }}</span>
    </div>
    </div>

    <div class="chat-input">
      <input type="text" v-model="message" @keyup.enter="sendMessage" placeholder="Type your message...">
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<style lang="postcss" scoped>
.chat {
  border: solid 1px #ccc;
  border-radius: .25rem;
  max-width: 300px;
  /* Add your styles here */
}

.chat-messages {
  overflow: scroll;
  display: flex;
  flex-flow: column;
  height: 300px;
  padding: .5rem;
  gap: .5rem;
}

.chat-message--bot {
  text-align: right;

  span {
    color: #333;
    background: #f9f9f9;
  }
}

.chat-message {
  display: inline-block;
  padding: .5rem;
  color: #f9f9f9;
  background: #007bff;
  border-radius: .5rem;
}

.chat-input {
  display: flex;

  input {
    flex: 1;
    color: #333;
    padding: .5rem;
    background: #f9f9f9;
  }

  button {
    background: #007bff;
    color: white;
    border: none;
    padding: .5rem 1rem;
    cursor: pointer;
  }
}
</style>