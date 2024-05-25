<script lang="ts" setup>
import { ref, onMounted } from 'vue';

import RecorderIcon from './Icons/Recorder.vue';

// import AudioRecorder from './../services/audio';

const recorder = ref()
const isRecording = ref(false);
const audioEle = ref<HTMLAudioElement>();

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream: any) => {
    recorder.value = new MediaRecorder(stream);

    recorder.value.ondataavailable = (event: any) => {
      const audioBlob = new Blob([event.data], { type: 'audio/wav' });
      const audioUrl = URL.createObjectURL(audioBlob);

      if(!audioEle.value) return console.error('No audio element found')

      const formData = new FormData();

      formData.append('audio', audioBlob);

      fetch('http://localhost:5003/send-audio', {
        method: 'POST',
        body: formData
      }).then((response: any) => {
        console.log('Response', response);
      }).catch((error: any) => {
        console.error('Error', error);
      })

      audioEle.value.src = audioUrl;
    }

    recorder.value.start();
    isRecording.value = true;
  }).catch((error: any) => {
    console.error('Error', error);
  })
}

function stopRecording() {
  if(!recorder.value) return console.error('No recorder found');

  recorder.value.stop();
  isRecording.value = false;
}

function toggleRecording() {
  if(isRecording.value) {
    stopRecording();
    return;
  }

  startRecording();
  // const recorder = new AudioRecorder();

  // if(isRecording.value) {
  //   recorder.stopRecording();
  //   isRecording.value = false;
  //   return;
  // }

  // recorder.startRecording().then((stream: any) => {
  //   if(!audioEle.value) return console.error('No audio element found')

  //   isRecording.value = true

  //   console.log('Stream', stream);
  //   audioEle.value.srcObject = stream;
  // }).catch((error: any) => {
  //   console.error('Error', error);
  // })
  // console.log('Start Recording', navigator.mediaDevices, navigator.mediaDevices.getUserMedia);
}
</script>

<template>
  <div class="audio-recorder">
    <button
      class="audio-recorder__button"
      @click="toggleRecording"
    >
      <RecorderIcon class="icon" />
    </button>
    <audio
      class="audio-recorder__audio"
      ref="audioEle"
      controls
    ></audio>
  </div>
</template>

<style scoped>

.audio-recorder {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  width: 3rem;
  height: 3rem;
  overflow: hidden;
  background: #F5F5F5;
}

.icon {
  display: block;
  color: #721A30;
  width: 1.75rem;
  height: 1.75rem;
}
</style>