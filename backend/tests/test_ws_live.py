import asyncio
import json
import websockets


async def test_websocket():
    uri = "ws://localhost:8000/ws/agent-run"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"goal": "How many tasks are there in total?"}))

        while True:
            message = await ws.recv()
            data = json.loads(message)
            print(f"[{data['type']}]", data)
            if data["type"] in ("done", "error"):
                break


if __name__ == "__main__":
    asyncio.run(test_websocket())