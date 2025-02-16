from typing import Literal

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.models import BitEvent, WordEvent
from app.api.ws_handler import WebSocketHandler
from app.config.settings import settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WebSocket handler
ws_handler = WebSocketHandler()


@app.get("/")
async def home():
    return RedirectResponse(url="/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming events to web client"""
    await ws_handler.handle_connection(websocket)


print(f"BCI App Server Active on {settings.ENV} 🚀")
