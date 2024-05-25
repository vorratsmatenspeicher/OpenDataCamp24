class WebSocketService {
  public socket: WebSocket;

  constructor(url: string, { onopen, onmessage }: { onopen: () => void, onmessage: (data: any) => void }) {
    this.socket = new WebSocket(url);

    this.socket.onopen = onopen
    this.socket.onmessage = onmessage
    this.socket.onclose = this.onClose.bind(this);
    this.socket.onerror = this.onError.bind(this);
  }

  private onOpen() {
    console.log('WebSocket connection opened');
    // Perform any necessary initialization or send initial messages
  }

  private onMessage(data: any) {
    const message = data
    console.log('Received message:', message);
    // Handle the received message
  }

  private onClose() {
    console.log('WebSocket connection closed');
    // Perform any necessary cleanup or reconnection logic
  }

  private onError(error: any) {
    console.error('WebSocket error:', error);
    // Handle the error
  }

  public send(message: string) {
    this.socket.send(message);
    console.log('Sent message:', message);
  }

  public close() {
    this.socket.close();
  }
}

export default WebSocketService;