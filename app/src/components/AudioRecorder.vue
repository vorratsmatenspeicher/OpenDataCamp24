<script lang="ts" setup>
import { ref, onMounted } from 'vue';

import AudioRecorder from './../services/audio';

const audioEle = ref<HTMLAudioElement>();

function startRecording() {
  const recorder = new AudioRecorder();

  recorder.startRecording().then((stream: any) => {
    if(!audioEle.value) return console.error('No audio element found')

    console.log('Stream', stream);
    audioEle.value.srcObject = stream;
  });
  console.log('Start Recording', navigator.mediaDevices, navigator.mediaDevices.getUserMedia);
}

function stopRecording() {
  console.log('Stop Recording');
}
</script>

<template>
  <div class="audio-recorder">
    <button
      class="audio-recorder__button"
      @click="startRecording"
    >
      Start Recording
    </button>
    <audio
      class="audio-recorder__audio"
      ref="audioEle"
      controls
    ></audio>
  </div>
</template>