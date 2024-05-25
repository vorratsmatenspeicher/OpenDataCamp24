<script setup lang="ts">
import { ref } from 'vue'

import ChatbotIcon from './components/Icons/Chatbot.vue'
import Chat from './components/Chat.vue'

const openCall = ref(false)
</script>

<template>
  <header>
  </header>

  <main>
    <div v-if="!openCall">
      <transition name="fade" appear>
        <button class="button" @click="openCall = true">
          <ChatbotIcon class="icon" />
        </button>
      </transition>
    </div>
    <div v-else>
      <Chat />
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.button {
  border: solid 2px #ccc;
  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
}

.icon {
  color: white;
  width: 2rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
