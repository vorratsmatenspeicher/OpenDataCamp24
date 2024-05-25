class AudioRecorder {
  private mediaRecorder: MediaRecorder;
  private chunks: Blob[] = [];

  constructor() {
    // Initialize the media recorder
    //this.mediaRecorder = new MediaRecorder();

    // Event listener for data available
    // this.mediaRecorder.addEventListener('dataavailable', (event) => {
    //   this.chunks.push(event.data);
    // });
  }

  startRecording() {
    return navigator.mediaDevices.getUserMedia({ audio: true }/*of type MediaStreamConstraints*/)
    // Start recording audio
    // this.mediaRecorder.start();
  }

  stopRecording() {
    // Stop recording audio
    this.mediaRecorder.stop();
  }

  getAudioBlob() {
    // Get the recorded audio as a Blob
    return new Blob(this.chunks, { type: this.mediaRecorder.mimeType });
  }
}

export default AudioRecorder