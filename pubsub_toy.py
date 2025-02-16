"""
WebSocket PubSub Example Server

This example demonstrates a simple pub/sub server using FastAPI and WebSockets.
Clients can:
1. Connect via WebSocket to subscribe to channels
2. Publish messages via WebSocket or HTTP endpoint
3. Receive messages from other clients in real-time

Usage:
    Run the server: python pubsub_toy.py
    Connect clients to: ws://localhost:8080/ws/pubsub
"""

from fastapi import FastAPI, WebSocket
from fastapi.routing import APIRouter
from fastapi_websocket_pubsub import PubSubEndpoint

app = FastAPI()
router = APIRouter()

# Initialize PubSub endpoint
pubsub = PubSubEndpoint()


@router.websocket("/pubsub")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint handling pub/sub communications"""
    await pubsub.main_loop(websocket)


# Mount the WebSocket router
app.include_router(router, prefix="/ws")


@app.post("/publish")
async def publish_message(payload: dict):
    """HTTP endpoint for publishing messages (testing purposes)"""
    await pubsub.publish(["broadcast"], payload)
    return {"status": "published"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("pubsub_toy:app", port=6666)
