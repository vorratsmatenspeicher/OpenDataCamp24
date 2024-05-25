const WebSocket = require('ws');

// Create a WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

// Event listener for new connections
wss.on('connection', (ws) => {
	// Event listener for incoming messages
	ws.on('message', (message) => {
		console.log('Received message:', message);

		// Send a response back to the client
		ws.send('Hello from the server!');
	});

	// Event listener for connection close
	ws.on('close', () => {
		console.log('Client disconnected');
	});
});

console.log('WebSocket server is running on port 8080');