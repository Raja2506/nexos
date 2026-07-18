from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.orchestration.graph_builder import build_graph

router = APIRouter()


@router.websocket("/ws/agent-run")
async def agent_run_websocket(websocket: WebSocket):
    """
    Client connects here, sends a goal, and receives a live message
    every time an agent (node) finishes running - instead of waiting
    silently for the whole pipeline to complete.
    """
    await websocket.accept()

    try:
        data = await websocket.receive_json()
        goal = data["goal"]

        graph = build_graph()
        initial_state = {"goal": goal}

        async for update in graph.astream(initial_state, stream_mode="updates"):
            for node_name, node_output in update.items():
                await websocket.send_json({
                    "type": "agent_finished",
                    "agent": node_name,
                    "output_keys": list(node_output.keys()),
                })

        await websocket.send_json({"type": "done"})

    except WebSocketDisconnect:
        print("Client disconnected from agent-run websocket")
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})