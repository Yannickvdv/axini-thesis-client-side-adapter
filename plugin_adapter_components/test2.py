import asyncio
import websockets

########################
# Handling socket data #
########################

# Define a callback to handle incoming messages from the browser
async def handle_browser_data(websocket, path):
    async for message in websocket:
        # Process the incoming data (mutation information) here
        print(f"Received message from browser: {message}")

# Start the WebSocket server
start_server = websockets.serve(handle_browser_data, "localhost", 8765)

async def main():
    await start_server

# Run the WebSocket server
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()



