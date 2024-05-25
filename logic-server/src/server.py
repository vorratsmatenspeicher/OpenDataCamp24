import logging
import sys

import session

import asyncio
from websockets.server import serve


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


async def chat(websocket):
    s = session.create_session()

    for token in s.get_response("Begrüße einen neuen Benutzer.", "system"):
        if token:
            await asyncio.sleep(0.05)
            await websocket.send(token)
    await websocket.send("")

    async for message in websocket:
        print(f"Received message: {message!r}")
        for token in s.get_response(message):
            if token:
                await asyncio.sleep(0.05)
                await websocket.send(token)

        await websocket.send("")


async def main():
    print("Server started")
    async with serve(chat, "0.0.0.0", 5000):
        await asyncio.Future()  # run forever


asyncio.run(main())
