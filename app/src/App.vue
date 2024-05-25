<script setup lang="ts">
import { ref } from 'vue'

import ArrowCurvedIcon from './components/Icons/ArrowCurved.vue'
import PhoneIcon from './components/Icons/Phone.vue'
import ChatIcon from './components/Icons/Chat.vue'
import ChatbotIcon from './components/Icons/Chatbot.vue'
import Chat from './components/Chat.vue'

const openCall = ref(false)
</script>

<template>
  <header>
    <div class="container">
      <h1 class="headline">DIGITALER WETTERASSISTENT</h1>
    </div>
  </header>

  <main>
    <transition name="fade">
      <div v-if="!openCall">
        <div class="coming-soon">
          <h2 class="claim">Coming soon</h2>
          <ArrowCurvedIcon class="icon arrow-left" />
          <ArrowCurvedIcon class="icon arrow-right" />
        </div>
        <div class="button-group">
          <button class="button button--chat">
            <ChatIcon class="icon" />
          </button>
          <button class="button button--chatbot" @click="openCall = true">
            <ChatbotIcon class="icon" />
          </button>
          <button class="button button--phone">
            <PhoneIcon class="icon" />
          </button>
        </div>
      </div>
      <div v-else>
        <Chat />
      </div>
    </transition>
  </main>
</template>

<style lang="postcss" scoped>
main {
  flex: 1;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.headline {
  font-family: "Dosis", monospace;
  font-weight: 700;
  text-align: center;
  width: 80%;
  font-size: 4rem;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.2;
  color: #1A7268;
}

.claim {
  font-family: "Shadows Into Light", monospace;
  font-weight: 700;
  text-align: center;
  width: 80%;
  font-size: 2rem;
  margin: 0 auto;
}

.button-group {
  position: relative;
  display: flex;
  /* gap: 1rem; */

  animation: appear 2s forwards;
}

.button {
  transition: transform 0.5s ease-out;
  cursor: pointer;
  background: var(--color-background);
  border: solid 2px #ccc;
  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;
  width: 6rem;
  height: 6rem;
}
.button--chatbot {
  transition: border-color 0.25s ease-out;
  z-index: 10;
  position: relative;
  animation: appear-center 2.4s ease-out forwards;

  .icon {
    transition: color 0.25s ease-out;
  }
}

.button--chatbot:hover {
  border-color: #26A697;

  .icon {
    color: #26A697;
  }
}

.button--phone,
.button--chat {
  opacity: 0;
  border-color: #333;
  .icon {
    opacity: 0;
    color: #333;
    animation: appear 1s 1s ease-out forwards;
  }
}

.button--phone {
  transform: translateX(-100%);
  animation: appear-left .75s 1s ease-out forwards;
}

.button--chat {
  transform: translateX(100%);
  animation: appear-right .75s 1s ease-out forwards;
}

.icon {
  color: white;
  width: 3rem;
}

.coming-soon {
  transform: rotate(-5deg);
  position: relative;
  margin-bottom: 3rem;
  opacity: 0;
  animation: appear 2s 1.7s forwards;

  .icon {
    position: absolute;
    top: 1.5rem;
    width: 3rem;
    color: #ccc;
  }
  .arrow-left {
    transform: scale(-1, 1) rotate(69deg);
    left: 1rem;
  }

  .arrow-right {
    transform: rotate(79deg);
    top: 2rem;
    right: 1rem;
  }
}

.fade-enter-active,
.fade-leave-active {
  position: absolute;
  transition: opacity 0.5s;
}

.fade-enter,
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes appear-center {
  0% {
    opacity: 0;
  }

  40%, 50% {
    transform: scale(1);
    opacity: 1;
  }

  80%,
  100% {
    transform: scale(1.2);
    opacity: 1;
  }
}

@keyframes appear-left {
  0% {
    opacity: 0;
  }

  20% {
    transform: translateX(-100%);
    /* opacity: 0; */
  }

  100% {
    opacity: 1;
    transform: translateX(20%);
  }
}

@keyframes appear-right {
  0% {
    opacity: 0;
    transform: translateX(100%);
  }

  20% {
    opacity: 0;
  }

  100% {
    opacity: 1;
    transform: translateX(-20%);
  }
}

@keyframes appear {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>
