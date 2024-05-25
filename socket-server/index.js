const WebSocket = require('ws');
const express = require('express')
const multer = require('multer')
const cors = require('cors')

const OpenAI = require('openai');
const fs = require('fs');
const streamifier = require('streamifier');

const app = express()
const upload = multer({ dest: 'uploads/' })
const port = 8080

app.use(cors())

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

app.post('/send-audio', upload.single('audio'), (req, res) => {
	// console.log(streamifier.createReadStream(req.file.buffer));
  openai.audio.transcriptions.create({
		file: streamifier.createReadStream(req.file.buffer),
		model: 'whisper-1',
	}).then((response) => {
		console.log('Response', response);

		res.json(response);
	}).catch((error) => {
		console.error('Error', error);
	})
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

// Create a WebSocket server
const wss = new WebSocket.Server({ port: 5000 });

// const socketClient = socketIOClient.io('ws://141.56.56.77:5000/chat')

// socketClient.on('connect', () => {
// 	console.log('Connected to socket service');
// })

// Event listener for new connections
wss.on('connection', (ws) => {
	const socketService = new WebSocket('ws://logic:5000')

	socketService.onopen = () => {
		console.log('Connected to socket service');

		ws.send(JSON.stringify({
			type: 'session'
		}));
	}

	socketService.onmessage = (message) => {
		console.log('Connected to socket service', message.data);

		ws.send(JSON.stringify({
			type: 'message',
			data: message.data
		}));
	}

	// fetch('http://logic:5000/create_session').then((res) => {
	// 	res.json().then((data) => {
	// 		console.log('Session created', data);
	// 		ws.send(JSON.stringify({
	// 			type: 'session',
	// 			data: data.session_id
	// 		}));
	// 	});
	// })

	// Event listener for incoming messages
	ws.on('message', (data) => {
		const { session_id, prompt } = JSON.parse(data.toString())

		socketService.send(prompt)

		// fetch(`http://logic:5000/get_response?prompt=${ prompt }&session_id=${ session_id }`).then((res) => {
		// 	res.json().then((body) => {
		// 		console.log('Response received', body);
		// 		ws.send(JSON.stringify({
		// 			type: 'message',
		// 			data: body.response
		// 		}));
		// 	});
		// })

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

console.log('WebSocket server is running on port 5000');