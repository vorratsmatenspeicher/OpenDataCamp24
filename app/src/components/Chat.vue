
<script lang="ts" setup>
import { ref, type Ref, onMounted, nextTick } from 'vue';
import { marked } from 'marked';

import SendIcon from './Icons/Send.vue'

import AudioRecorder from './AudioRecorder.vue';
import WebSocketService from '../services/socket';

const socket: Ref<WebSocketService|null> = ref(null);

const session = ref('');

const chatMessagesEleScroll = ref()
const chatMessagesEleInner = ref()
const inProgress = ref(true);
const message = ref('');
const messages = ref<{ owner: 'bot'|'self', message: any }[]>([]);
const sendMessage = () => {
  socket.value?.send(JSON.stringify({
    session_id: session.value,
    prompt: message.value
  }));

  messages.value.push({ owner: 'self', message: marked.parseInline(message.value, { breaks: true }) });

  inProgress.value = true;

  nextTick(() => {
    chatMessagesEleScroll.value.scrollTop = chatMessagesEleInner.value.scrollHeight;
  })

  message.value = ''
};

function handleOpenMessage() {
  // messages.value.push({ owner: 'bot', message: 'Ist dir kalt?' });

  inProgress.value = false;
}

function handleMessageSend(event: MessageEvent) {
  const socketMsg = JSON.parse(event.data);

  inProgress.value = false;

  if(socketMsg.type === 'message') {
    if(!socketMsg.data) return;
    if(!messages.value.length || messages.value[messages.value.length - 1].owner === 'self') {
      messages.value.push({ owner: 'bot', message: marked.parseInline(socketMsg.data, { breaks: true }) });
    } else {
      messages.value[messages.value.length - 1].message = marked.parseInline(messages.value[messages.value.length - 1].message + socketMsg.data, { breaks: true });
    }

    nextTick(() => {
      chatMessagesEleScroll.value.scrollTop = chatMessagesEleInner.value.scrollHeight;
    })
  }

  if(socketMsg.type === 'session') {
    // session.value = socketMsg.data;
    return;
  }
  console.log('event', event.data);
  // messages.value.push({ owner: 'bot', message: event.data });
}

function handleSpeechToText(text: string) {
  console.log('Speech to text', text);

  message.value = text;
  // sendMessage();
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
    <div class="chat-messages" ref="chatMessagesEleScroll">
      <div class="chat-messages__inner" ref="chatMessagesEleInner">
        <!-- Display chat messages here -->
        <div
          class="chat-message"
          :class="{
              'chat-message--self': msg.owner === 'self',
              'chat-message--bot': msg.owner === 'bot'
            }"
          v-for="(msg, index) in messages"
          :key="index"
        >
          <span class="chat-message__inner" v-html="msg.message"></span>
        </div>

        <div class="chat-message chat-message--bot loading" v-if="inProgress">
          <span class="chat-message__inner">
            <div class="loader"></div>
          </span>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <div class="chat-input__text">
        <input type="text" v-model="message" @keyup.enter="sendMessage" placeholder="Type your message...">
        <button class="button-submit" @click="sendMessage">
          <SendIcon class="icon" />
        </button>
      </div>
      <div class="chat-input__audio">
        <audio-recorder @onRecording="handleSpeechToText" />
      </div>
    </div>
  </div>
</template>

<style lang="postcss" scoped>
.chat {
  width: 500px;
  overflow: hidden;
  /* Add your styles here */
}

.border-left {
  border-left: solid 1px #ccc;
}

.chat-messages {
  font-family: "Dosis", monospace;
  overflow: scroll;
  height: 400px;
  padding: 1rem 2rem;
  background: #F5F5F5;
  border: solid 1px #040404;
  border-radius: .5rem;
  margin-bottom: 1.5rem;
}

.chat-messages__inner {
  display: flex;
  flex-flow: column;
  gap: 1rem;
}

.chat-message--self {
  text-align: right;
}

.chat-message--bot {
  text-align: left;

  span {
    color: #080D21;
    background: #26A697;
  }
}

.chat-message__inner {
  display: inline-block;
  text-align: left;
  font-weight: 500;
  font-size: 1.25rem;
  width: 90%;
  padding: .5rem 1rem;
  color: #080D21;
  background: #37D2C0;
  border-radius: .5rem;
}

.chat-message :deep(strong) {
  font-weight: 600;
}

.chat-message.loading .chat-message__inner {
  text-align: center;
}

.chat-input {
  display: flex;
  gap: 1rem;
  padding-left: .5rem;
  padding-right: .5rem;

  input {
    flex: 1;
    color: #333;
    padding: .75rem .5rem;
    font-size: 1.125rem;
    background: #F5F5F5;
  }

  .button-submit {
    transition: background 0.3s ease-in-out;
    background: #26A697;
    color: white;
    border: none;
    padding: .5rem 1rem;
    cursor: pointer;

    .icon {
      display: block;
      width: 1.5rem;
      height: 1.5rem;
    }
  }

  .button-submit:hover {
    background: #1E8579;
  }
}

.chat-input__text {
  flex: 1;
  display: flex;
  border-radius: .5rem;
  overflow: hidden;
}

.chat-input__audio {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* HTML: <div class="loader"></div> */
.loader {
  display: inline-grid;
}
.loader:before,
.loader:after {
  content: "";
  grid-area: 1/1;
  height: 1rem;
  aspect-ratio: 6;
  --c: #0000 64%,#000 66% 98%,#0000 101%;
  background:
    radial-gradient(35% 146% at 50% 159%,var(--c)) 0 0,
    radial-gradient(35% 146% at 50% -59%,var(--c)) 25% 100%;
  background-size: calc(100%/3) 50%;
  background-repeat: repeat-x;
  -webkit-mask: repeating-linear-gradient(90deg,#000 0 15%,#0000 0 50%) 0 0/200%;
  animation: l8 .8s infinite linear;
}
.loader:after {
  scale: -1;
}
@keyframes l8{
  to {-webkit-mask-position:-100% 0}
}
</style>