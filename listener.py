import asyncio
import websockets
import json
from solathon import PublicKey

SOLANA_WS_URL = 'wss://api.mainnet-beta.solana.com'

PUBLIC_KEY = 'PUBLIC_KEY'

async def listen_to_transactions():
    async with websockets.connect(SOLANA_WS_URL) as websocket:
        subscription_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "accountSubscribe",
            "params": [
                str(PublicKey(PUBLIC_KEY)),
                {"encoding": "jsonParsed"}
            ]
        }
        await websocket.send(json.dumps(subscription_request))
        print("Subscribed to account changes.")

        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)

                print("Received data:", data)
            except Exception as e:
                print(f"Error: {e}")

asyncio.get_event_loop().run_until_complete(listen_to_transactions())