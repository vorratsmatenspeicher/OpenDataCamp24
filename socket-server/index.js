const WebSocket = require('ws');

// Create a WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

// Event listener for new connections
wss.on('connection', (ws) => {

	fetch('http://logic:5000/create_session').then((res) => {
		res.json().then((data) => {
			console.log('Session created', data);
			ws.send(JSON.stringify({
				type: 'session',
				data: data.session_id
			}));
		});
	})

	// Event listener for incoming messages
	ws.on('message', (data) => {
		const { session_id, prompt } = JSON.parse(data.toString())

		fetch(`http://logic:5000/get_response?prompt=${ prompt }&session_id=${ session_id }`).then((res) => {
			res.json().then((body) => {
				console.log('Response received', body);
				ws.send(JSON.stringify({
					type: 'message',
					data: body.response
				}));
			});
		})

		// Send a response back to the client
		// ws.send(JSON.stringify({
		// 	type: 'message',
		// 	data: 'Hello from the server!'
		// }));
	});

	ws.on('open', () => {
		console.log('Client connected');
	});

	// Event listener for connection close
	ws.on('close', () => {
		console.log('Client disconnected');
	});
});

console.log('WebSocket server is running on port 8080');