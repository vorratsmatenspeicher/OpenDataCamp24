<script setup lang="ts">
import { ref } from 'vue'

import PhoneIcon from './components/Icons/Phone.vue'
import Chat from './components/Chat.vue'

const openCall = ref(false)
</script>

<template>
  <header>
  </header>

  <main>
    <div v-if="!openCall">
      <button class="button" @click="openCall = true">
        <PhoneIcon class="icon" />
      </button>
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
</style>
